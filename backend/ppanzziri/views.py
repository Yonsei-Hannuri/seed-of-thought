import json
import os
from datetime import date, timedelta
from urllib.parse import urlparse

from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from ppanzziri.job import WritingAnalysisJob
from ppanzziri.models import (
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
    Social,
    WritingManuscriptPhoto,
    WritingRecord,
)
from ppanzziri.serializers import (
    BudgetRecordSerializer,
    WritingRecordSerializer,
)
from ppanzziri.storage import delete_photo, delete_photos, extract_video_location, upload_photos, upload_writing_photos, upload_writing_video


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


def _calculate_days_to_goal(total_expense, goal):
    today = date.today()
    ninety_days_ago = today - timedelta(days=90)
    expense_last_90 = (
        BudgetRecord.objects
        .filter(type=BudgetRecord.TYPE_EXPENSE, transaction_date__gte=ninety_days_ago, transaction_date__lte=today)
        .aggregate(total=Sum('amount'))['total'] or 0
    )
    avg_daily = expense_last_90 / 90
    if avg_daily <= 0:
        return None
    remaining = goal - total_expense
    if remaining <= 0:
        return 0
    return int(remaining / avg_daily)


@api_view(['GET'])
def dashboard(request):
    records = BudgetRecord.objects.prefetch_related('effective_segments', 'tags').all()
    social = _get_or_create_social()

    goal = int(os.getenv('PPANZZIRI_START_CAPITAL', '30000000'))
    total_expense = BudgetRecord.objects.filter(type=BudgetRecord.TYPE_EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    days_to_goal = _calculate_days_to_goal(total_expense, goal)

    return Response(
        {
            'goal': goal,
            'totalExpense': total_expense,
            'daysToGoal': days_to_goal,
            'records': BudgetRecordSerializer(records, many=True).data,
            'social': _serialize_social(social),
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def budget_records(request):
    if request.method == 'GET':
        queryset = BudgetRecord.objects.prefetch_related('effective_segments', 'tags').filter(type=BudgetRecord.TYPE_EXPENSE)
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


@api_view(['PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def budget_record_detail(request, record_id):
    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    record = get_object_or_404(BudgetRecord, pk=record_id)

    if request.method == 'DELETE':
        delete_photos(record.photo_url_original, record.photo_url_compressed, record.photo_url_resized)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT: update record
    try:
        record_type = _normalize_record_type(request.data.get('type', record.type))
        transaction_date = _parse_date(
            request.data.get('transaction_date', request.data.get('transactionDate', str(record.transaction_date))),
            'transaction_date',
        )
        amount = _parse_positive_int(request.data.get('amount', record.amount), 'amount')
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    memo = request.data.get('memo', record.memo)
    if memo is None:
        memo = ''

    # Handle photo
    photo_file = request.FILES.get('photo')
    if photo_file:
        delete_photos(record.photo_url_original, record.photo_url_compressed, record.photo_url_resized)
        try:
            photo_urls = upload_photos(photo_file, 'records')
        except RuntimeError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        record.photo_url_original = photo_urls['original']
        record.photo_url_compressed = photo_urls['compressed']
        record.photo_url_resized = photo_urls['resized']

    record.type = record_type
    record.transaction_date = transaction_date
    record.amount = amount
    record.memo = str(memo)

    # Handle segments
    raw_segments = _extract_json_field(request.data, 'effective_segments', 'effectiveSegments')
    if raw_segments is not None:
        try:
            segments = _parse_effective_segments(raw_segments, transaction_date, amount)
        except ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        record.effective_segments.all().delete()
        BudgetEffectiveSegment.objects.bulk_create([
            BudgetEffectiveSegment(
                record=record,
                effective_from=seg['effective_from'],
                effective_to=seg['effective_to'],
                segment_amount=seg['segment_amount'],
            )
            for seg in segments
        ])

    # Handle tags
    raw_tags = _extract_json_field(request.data, 'tags', 'recordTags')
    if raw_tags is not None:
        try:
            tags = _parse_record_tags(raw_tags, amount)
        except ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)
        record.tags.all().delete()
        BudgetRecordTag.objects.bulk_create([
            BudgetRecordTag(record=record, name=tag['name'], amount=tag['amount'])
            for tag in tags
        ])

    record.save()
    record = BudgetRecord.objects.prefetch_related('effective_segments', 'tags').get(pk=record.pk)
    return Response(BudgetRecordSerializer(record).data, status=status.HTTP_200_OK)


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


def _parse_time(value, field_name):
    if value in (None, ''):
        return None
    from datetime import time as dt_time
    try:
        parts = str(value).split(':')
        return dt_time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError) as exc:
        raise ValidationError({field_name: 'Use HH:MM format.'}) from exc


def _parse_topics(value):
    if isinstance(value, list):
        return [str(t).strip() for t in value if str(t).strip()]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(t).strip() for t in parsed if str(t).strip()]
        except (json.JSONDecodeError, ValueError):
            pass
        stripped = value.strip()
        return [stripped] if stripped else []
    return []


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def writing_records(request):
    if request.method == 'GET':
        records = WritingRecord.objects.prefetch_related('manuscript_photos').all()
        daily_summary = (
            WritingRecord.objects
            .values('date')
            .annotate(total_char_count=Sum('char_count'), submission_count=Count('id'))
            .order_by('-date')
        )
        summary_data = [
            {
                'date': str(row['date']),
                'total_char_count': row['total_char_count'],
                'submission_count': row['submission_count'],
            }
            for row in daily_summary
        ]
        return Response(
            {
                'records': WritingRecordSerializer(records, many=True).data,
                'daily_summary': summary_data,
            },
            status=status.HTTP_200_OK,
        )

    # POST: create new writing record
    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error
    try:
        record_date = _parse_date(request.data.get('date'), 'date')
        start_time = _parse_time(request.data.get('start_time'), 'start_time')
        end_time = _parse_time(request.data.get('end_time'), 'end_time')
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    topics = _parse_topics(request.data.get('topics', []))
    place_name = str(request.data.get('place_name', '') or '').strip()[:100]

    # Upload timelapse video
    video_file = request.FILES.get('timelapse_video')
    video_url = ''
    latitude, longitude = None, None
    if video_file:
        latitude, longitude = extract_video_location(video_file)
        try:
            video_url = upload_writing_video(video_file)
        except RuntimeError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Upload manuscript photos
    photo_files = request.FILES.getlist('manuscript_photos')
    photo_results = []
    for photo_file in photo_files:
        try:
            urls = upload_writing_photos(photo_file)
            photo_results.append(urls)
        except RuntimeError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    raw_char_count = request.data.get('char_count')
    if raw_char_count not in (None, ''):
        try:
            char_count = int(raw_char_count)
        except (ValueError, TypeError):
            char_count = 0
    else:
        char_count = len(photo_results) * 400 if photo_results else 0

    with transaction.atomic():
        record = WritingRecord.objects.create(
            date=record_date,
            start_time=start_time,
            end_time=end_time,
            timelapse_video_url=video_url,
            topics=topics,
            char_count=char_count,
            latitude=latitude,
            longitude=longitude,
            place_name=place_name,
        )
        WritingManuscriptPhoto.objects.bulk_create([
            WritingManuscriptPhoto(
                record=record,
                photo_url_original=urls['original'],
                photo_url_compressed=urls['compressed'],
                photo_url_resized=urls['resized'],
                order=idx,
            )
            for idx, urls in enumerate(photo_results)
        ])

    record = WritingRecord.objects.prefetch_related('manuscript_photos').get(pk=record.pk)
    return Response(WritingRecordSerializer(record).data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def writing_record_detail(request, record_id):
    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    record = get_object_or_404(WritingRecord, pk=record_id)

    if request.method == 'DELETE':
        # Delete S3 files
        for photo in record.manuscript_photos.all():
            delete_photos(photo.photo_url_original, photo.photo_url_compressed, photo.photo_url_resized)
        if record.timelapse_video_url:
            delete_photo(record.timelapse_video_url)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT: update record
    try:
        record_date = _parse_date(request.data.get('date', str(record.date)), 'date')
        start_time = _parse_time(request.data.get('start_time'), 'start_time')
        end_time = _parse_time(request.data.get('end_time'), 'end_time')
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    topics = _parse_topics(request.data.get('topics', record.topics))

    raw_place_name = request.data.get('place_name')
    if raw_place_name is not None:
        record.place_name = str(raw_place_name).strip()[:100]

    record.date = record_date
    record.start_time = start_time
    record.end_time = end_time
    record.topics = topics

    # Handle new video if provided
    video_file = request.FILES.get('timelapse_video')
    if video_file:
        lat, lon = extract_video_location(video_file)
        record.latitude = lat
        record.longitude = lon
        if record.timelapse_video_url:
            delete_photo(record.timelapse_video_url)
        try:
            record.timelapse_video_url = upload_writing_video(video_file)
        except RuntimeError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Handle new photos if provided
    photo_files = request.FILES.getlist('manuscript_photos')
    if photo_files:
        # Delete old photos
        for photo in record.manuscript_photos.all():
            delete_photos(photo.photo_url_original, photo.photo_url_compressed, photo.photo_url_resized)
        record.manuscript_photos.all().delete()

        photo_results = []
        for photo_file in photo_files:
            try:
                urls = upload_writing_photos(photo_file)
                photo_results.append(urls)
            except RuntimeError as exc:
                return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        WritingManuscriptPhoto.objects.bulk_create([
            WritingManuscriptPhoto(
                record=record,
                photo_url_original=urls['original'],
                photo_url_compressed=urls['compressed'],
                photo_url_resized=urls['resized'],
                order=idx,
            )
            for idx, urls in enumerate(photo_results)
        ])
        record.char_count = len(photo_results) * 400

    raw_char_count = request.data.get('char_count')
    if raw_char_count not in (None, ''):
        try:
            record.char_count = int(raw_char_count)
        except (ValueError, TypeError):
            pass

    record.save()
    record = WritingRecord.objects.prefetch_related('manuscript_photos').get(pk=record.pk)
    return Response(WritingRecordSerializer(record).data, status=status.HTTP_200_OK)


def _parse_optional_date(value, field_name):
    if value in (None, ''):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValidationError({field_name: 'Use YYYY-MM-DD format.'}) from exc


@api_view(['GET'])
def writing_dashboard(request):
    try:
        from_date = _parse_optional_date(request.query_params.get('from'), 'from')
        to_date = _parse_optional_date(request.query_params.get('to'), 'to')
    except ValidationError as exc:
        return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)

    records_qs = WritingRecord.objects.all()
    if from_date is not None:
        records_qs = records_qs.filter(date__gte=from_date)
    if to_date is not None:
        records_qs = records_qs.filter(date__lte=to_date)

    daily_rows = (
        records_qs
        .values('date')
        .annotate(
            total_char_count=Sum('char_count'),
            submission_count=Count('id'),
        )
        .order_by('date')
    )

    # Collect topics by date as keywords
    topics_by_date = {}
    for record in records_qs:
        date_key = record.date.isoformat()
        topics_by_date.setdefault(date_key, []).extend(record.topics or [])

    daily = []
    all_keywords = []
    for row in daily_rows:
        date_key = row['date'].isoformat()
        day_keywords = topics_by_date.get(date_key, [])
        daily.append({
            'date': date_key,
            'char_count': row['total_char_count'] or 0,
            'submission_count': row['submission_count'] or 0,
            'keywords': day_keywords,
        })
        all_keywords.extend(day_keywords)

    keyword_ranking = _rank_keywords(all_keywords)

    return Response(
        {
            'daily': daily,
            'keyword_ranking': keyword_ranking,
        },
        status=status.HTTP_200_OK,
    )


def _rank_keywords(keywords):
    counts = {}
    for keyword in keywords:
        if not keyword:
            continue
        counts[keyword] = counts.get(keyword, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{'keyword': name, 'count': count} for name, count in ranked]


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


