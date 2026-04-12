import json
import os
from datetime import date
from urllib.parse import urlparse

from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from ppanzziri.models import (
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
    Social,
)
from ppanzziri.serializers import (
    BudgetRecordSerializer,
)
from ppanzziri.storage import delete_photos, upload_photos


def _get_admin_password_error_response(request):
    expected_password = os.getenv('PPANZZIRI_ADMIN_PASSWORD', '').strip()
    if not expected_password:
        return None

    provided_password = (
        request.headers.get('X-Admin-Password')
        or request.data.get('adminPassword')
        or request.data.get('admin_password')
        or ''
    )

    if provided_password != expected_password:
        return Response({'detail': 'Invalid admin password'}, status=status.HTTP_401_UNAUTHORIZED)
    return None


def _parse_date(value, field_name):
    if isinstance(value, date):
        return value
    if not value:
        raise ValidationError({field_name: 'This field is required.'})

    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValidationError({field_name: 'Use YYYY-MM-DD format.'}) from exc


def _parse_positive_int(value, field_name):
    if value is None or value == '':
        raise ValidationError({field_name: 'This field is required.'})

    try:
        parsed_value = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError({field_name: 'Must be an integer.'}) from exc

    if parsed_value <= 0:
        raise ValidationError({field_name: 'Must be greater than 0.'})
    return parsed_value


def _normalize_record_type(raw_type):
    if not raw_type:
        raise ValidationError({'type': 'This field is required.'})

    mapping = {
        'expense': BudgetRecord.TYPE_EXPENSE,
        'income': BudgetRecord.TYPE_INCOME,
        'EXPENSE': BudgetRecord.TYPE_EXPENSE,
        'INCOME': BudgetRecord.TYPE_INCOME,
        '지출': BudgetRecord.TYPE_EXPENSE,
        '수입': BudgetRecord.TYPE_INCOME,
    }
    normalized_type = mapping.get(str(raw_type), mapping.get(str(raw_type).lower()))
    if not normalized_type:
        raise ValidationError({'type': 'Supported values are EXPENSE/INCOME.'})
    return normalized_type


def _extract_json_field(data, snake_key, camel_key):
    raw_value = data.get(snake_key, data.get(camel_key))
    if raw_value in (None, ''):
        return None
    if isinstance(raw_value, (list, dict)):
        return raw_value

    try:
        return json.loads(raw_value)
    except (TypeError, ValueError) as exc:
        raise ValidationError({snake_key: 'Must be valid JSON.'}) from exc


def _serialize_social(social):
    return {
        'youtube_embed_url': social.youtube_embed_url,
        'instagram_post_url': social.instagram_post_url,
        'instagram_profile_url': social.instagram_profile_url,
        'extra_links': social.extra_links,
    }



def _get_or_create_social():
    social = Social.objects.order_by('id').first()
    if social:
        return social
    return Social.objects.create()


def _parse_https_url(value, field_name):
    if value is None:
        return ''
    if not isinstance(value, str):
        raise ValidationError({field_name: 'Must be a string.'})

    normalized = value.strip()
    if normalized == '':
        return ''

    parsed = urlparse(normalized)
    if parsed.scheme.lower() != 'https' or not parsed.netloc:
        raise ValidationError({field_name: 'Only valid https URL is allowed.'})
    return parsed


def _normalize_youtube_embed_url(value):
    parsed = _parse_https_url(value, 'youtube_embed_url')
    if parsed == '':
        return ''

    if parsed.netloc.lower() != 'www.youtube.com':
        raise ValidationError({'youtube_embed_url': 'Only https://www.youtube.com/embed/... is allowed.'})

    paths = [part for part in parsed.path.split('/') if part]
    if len(paths) != 2 or paths[0] != 'embed':
        raise ValidationError({'youtube_embed_url': 'Only https://www.youtube.com/embed/... is allowed.'})

    return f'https://www.youtube.com/embed/{paths[1]}'


def _normalize_instagram_post_url(value):
    parsed = _parse_https_url(value, 'instagram_post_url')
    if parsed == '':
        return ''

    if parsed.netloc.lower() != 'www.instagram.com':
        raise ValidationError({'instagram_post_url': 'Only https://www.instagram.com/p/... is allowed.'})

    paths = [part for part in parsed.path.split('/') if part]
    if len(paths) != 2 or paths[0] != 'p':
        raise ValidationError({'instagram_post_url': 'Only https://www.instagram.com/p/... is allowed.'})

    return f'https://www.instagram.com/p/{paths[1]}/'


def _normalize_instagram_profile_url(value):
    parsed = _parse_https_url(value, 'instagram_profile_url')
    if parsed == '':
        return ''

    if parsed.netloc.lower() != 'www.instagram.com':
        raise ValidationError({'instagram_profile_url': 'Only https://www.instagram.com/... is allowed.'})

    paths = [part for part in parsed.path.split('/') if part]
    if len(paths) != 1 or paths[0] == 'p':
        raise ValidationError({'instagram_profile_url': 'Only profile URL is allowed.'})

    return f'https://www.instagram.com/{paths[0]}/'


def _normalize_extra_links(raw_value):
    if raw_value in (None, ''):
        return []
    if not isinstance(raw_value, list):
        raise ValidationError({'extra_links': 'Must be a list.'})

    normalized = []
    for idx, item in enumerate(raw_value):
        if not isinstance(item, dict):
            raise ValidationError({'extra_links': f'Item {idx} must be an object.'})

        label = item.get('label', '')
        href = item.get('href', '')
        label = str(label).strip() if label is not None else ''
        href = str(href).strip() if href is not None else ''

        # Remove empty items after trim.
        if label == '' or href == '':
            continue

        if len(label) > 30:
            raise ValidationError({'extra_links': f'Item {idx} label must be <= 30 chars.'})
        if len(href) > 500:
            raise ValidationError({'extra_links': f'Item {idx} href must be <= 500 chars.'})

        parsed = _parse_https_url(href, f'extra_links[{idx}].href')
        normalized_href = f'https://{parsed.netloc.lower()}{parsed.path}'
        if parsed.query:
            normalized_href = f'{normalized_href}?{parsed.query}'

        normalized.append(
            {
                'label': label,
                'href': normalized_href,
            }
        )

    if len(normalized) > 6:
        raise ValidationError({'extra_links': 'Maximum 6 non-empty items are allowed.'})
    return normalized


def _parse_effective_segments(raw_segments, transaction_date, amount):
    if not raw_segments:
        return [
            {
                'effective_from': transaction_date,
                'effective_to': transaction_date,
                'segment_amount': amount,
            }
        ]

    if not isinstance(raw_segments, list):
        raise ValidationError({'effective_segments': 'Must be a list.'})

    parsed_segments = []
    segment_sum = 0
    for idx, segment in enumerate(raw_segments):
        if not isinstance(segment, dict):
            raise ValidationError({'effective_segments': f'Item {idx} must be an object.'})

        effective_from = _parse_date(segment.get('effective_from', segment.get('effectiveFrom')), 'effective_from')
        effective_to = _parse_date(segment.get('effective_to', segment.get('effectiveTo')), 'effective_to')
        segment_amount = _parse_positive_int(
            segment.get('segment_amount', segment.get('segmentAmount')),
            'segment_amount',
        )

        if effective_from > effective_to:
            raise ValidationError({'effective_segments': f'Item {idx} has invalid date range.'})

        parsed_segments.append(
            {
                'effective_from': effective_from,
                'effective_to': effective_to,
                'segment_amount': segment_amount,
            }
        )
        segment_sum += segment_amount

    if segment_sum != amount:
        raise ValidationError({'effective_segments': 'Sum of segment_amount must equal amount.'})

    return parsed_segments


def _split_evenly(total_amount, count):
    base = total_amount // count
    remainder = total_amount % count
    return [base + (1 if index < remainder else 0) for index in range(count)]


def _parse_record_tags(raw_tags, amount):
    if not raw_tags:
        return []

    if not isinstance(raw_tags, list):
        raise ValidationError({'tags': 'Must be a list.'})

    parsed_tags = []
    has_amount_for_all = True
    has_any_amount = False

    for idx, tag in enumerate(raw_tags):
        if isinstance(tag, str):
            name = tag.strip()
            tag_amount = None
        elif isinstance(tag, dict):
            name = str(tag.get('name', tag.get('tag', ''))).strip()
            tag_amount = tag.get('amount')
        else:
            raise ValidationError({'tags': f'Item {idx} must be string or object.'})

        if not name:
            raise ValidationError({'tags': f'Item {idx} has empty name.'})

        if tag_amount in (None, ''):
            has_amount_for_all = False
        else:
            has_any_amount = True
            tag_amount = _parse_positive_int(tag_amount, f'tags[{idx}].amount')

        parsed_tags.append({'name': name, 'amount': tag_amount})

    if has_any_amount and has_amount_for_all:
        provided_sum = sum(tag['amount'] for tag in parsed_tags)
        if provided_sum != amount:
            raise ValidationError({'tags': 'Sum of tag amounts must equal amount.'})
        return parsed_tags

    distributed_amounts = _split_evenly(amount, len(parsed_tags))
    for index, tag in enumerate(parsed_tags):
        tag['amount'] = distributed_amounts[index]

    return parsed_tags


def _create_budget_record(request):
    record_type = _normalize_record_type(request.data.get('type'))
    transaction_date = _parse_date(request.data.get('transaction_date', request.data.get('transactionDate')), 'transaction_date')
    amount = _parse_positive_int(request.data.get('amount'), 'amount')
    memo = request.data.get('memo', '')
    if memo is None:
        memo = ''
    segments = _parse_effective_segments(
        _extract_json_field(request.data, 'effective_segments', 'effectiveSegments'),
        transaction_date,
        amount,
    )
    tags = _parse_record_tags(_extract_json_field(request.data, 'tags', 'recordTags'), amount)

    photo_file = request.FILES.get('photo')
    photo_urls = {'original': '', 'compressed': '', 'resized': ''}
    if photo_file:
        photo_urls = upload_photos(photo_file, 'records')

    with transaction.atomic():
        record = BudgetRecord.objects.create(
            type=record_type,
            transaction_date=transaction_date,
            amount=amount,
            memo=str(memo),
            photo_url_original=photo_urls['original'],
            photo_url_compressed=photo_urls['compressed'],
            photo_url_resized=photo_urls['resized'],
        )
        BudgetEffectiveSegment.objects.bulk_create(
            [
                BudgetEffectiveSegment(
                    record=record,
                    effective_from=segment['effective_from'],
                    effective_to=segment['effective_to'],
                    segment_amount=segment['segment_amount'],
                )
                for segment in segments
            ]
        )
        BudgetRecordTag.objects.bulk_create(
            [
                BudgetRecordTag(
                    record=record,
                    name=tag['name'],
                    amount=tag['amount'],
                )
                for tag in tags
            ]
        )

    return record


@api_view(['GET'])
def dashboard(request):
    records = BudgetRecord.objects.prefetch_related('effective_segments', 'tags').all()
    social = _get_or_create_social()

    start_capital = int(os.getenv('PPANZZIRI_START_CAPITAL', '30000000'))
    total_income = BudgetRecord.objects.filter(type=BudgetRecord.TYPE_INCOME).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = BudgetRecord.objects.filter(type=BudgetRecord.TYPE_EXPENSE).aggregate(total=Sum('amount'))['total'] or 0

    return Response(
        {
            'startCapital': start_capital,
            'totalIncome': total_income,
            'totalExpense': total_expense,
            'currentBalance': start_capital + total_income - total_expense,
            'records': BudgetRecordSerializer(records, many=True).data,
            'social': _serialize_social(social),
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def budget_records(request):
    if request.method == 'GET':
        queryset = BudgetRecord.objects.prefetch_related('effective_segments', 'tags').all()
        return Response(BudgetRecordSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    try:
        record = _create_budget_record(request)
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
    except RuntimeError as exc:
        return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = BudgetRecordSerializer(record)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def budget_record_detail(request, record_id):
    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    record = get_object_or_404(BudgetRecord, pk=record_id)
    delete_photos(record.photo_url_original, record.photo_url_compressed, record.photo_url_resized)
    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def budget_tags(request):
    rows = (
        BudgetRecordTag.objects
        .values('name', 'record__type')
        .annotate(amount=Sum('amount'))
        .order_by('-amount', 'name', 'record__type')
    )

    response_rows = [
        {
            'name': row['name'],
            'amount': row['amount'] or 0,
            'recordType': row['record__type'],
        }
        for row in rows
    ]
    return Response(response_rows, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@parser_classes([JSONParser, FormParser])
def social(request):
    if request.method == 'GET':
        return Response(_serialize_social(_get_or_create_social()), status=status.HTTP_200_OK)

    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    try:
        youtube_embed_url = _normalize_youtube_embed_url(request.data.get('youtube_embed_url', ''))
        instagram_post_url = _normalize_instagram_post_url(request.data.get('instagram_post_url', ''))
        instagram_profile_url = _normalize_instagram_profile_url(request.data.get('instagram_profile_url', ''))
        extra_links = _normalize_extra_links(_extract_json_field(request.data, 'extra_links', 'extraLinks') or [])
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    social_obj = _get_or_create_social()
    social_obj.youtube_embed_url = youtube_embed_url
    social_obj.instagram_post_url = instagram_post_url
    social_obj.instagram_profile_url = instagram_profile_url
    social_obj.extra_links = extra_links
    social_obj.save(
        update_fields=[
            'youtube_embed_url',
            'instagram_post_url',
            'instagram_profile_url',
            'extra_links',
            'updated_at',
        ]
    )
    return Response({'ok': True}, status=status.HTTP_200_OK)


