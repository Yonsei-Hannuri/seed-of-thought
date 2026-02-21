import json
import os
from datetime import date

from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from ppanzziri.models import (
    BalanceCertification,
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
)
from ppanzziri.serializers import (
    BalanceCertificationSerializer,
    BudgetRecordSerializer,
)
from ppanzziri.storage import delete_photo, upload_photo


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
    segments = _parse_effective_segments(
        _extract_json_field(request.data, 'effective_segments', 'effectiveSegments'),
        transaction_date,
        amount,
    )
    tags = _parse_record_tags(_extract_json_field(request.data, 'tags', 'recordTags'), amount)

    photo_file = request.FILES.get('photo')
    photo_url = ''
    if photo_file:
        photo_url = upload_photo(photo_file, 'records')

    with transaction.atomic():
        record = BudgetRecord.objects.create(
            type=record_type,
            transaction_date=transaction_date,
            amount=amount,
            photo_url=photo_url,
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
    certifications = BalanceCertification.objects.all()

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
            'certifications': BalanceCertificationSerializer(certifications, many=True).data,
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
    delete_photo(record.photo_url)
    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def budget_tags(request):
    rows = (
        BudgetRecordTag.objects
        .values('name')
        .annotate(amount=Sum('amount'))
        .order_by('-amount', 'name')
    )
    return Response(list(rows), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def budget_certifications(request):
    if request.method == 'GET':
        queryset = BalanceCertification.objects.all()
        serializer = BalanceCertificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    certification_date = _parse_date(request.data.get('date'), 'date')
    photo_file = request.FILES.get('photo')
    if photo_file is None:
        return Response({'photo': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_photo_url = upload_photo(photo_file, 'certifications')
    except RuntimeError as exc:
        return Response({'detail': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    with transaction.atomic():
        certification, created = BalanceCertification.objects.get_or_create(
            date=certification_date,
            defaults={'photo_url': new_photo_url},
        )
        if not created:
            old_photo_url = certification.photo_url
            certification.photo_url = new_photo_url
            certification.save(update_fields=['photo_url'])
            delete_photo(old_photo_url)

    serializer = BalanceCertificationSerializer(certification)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
    )


@api_view(['DELETE'])
def budget_certification_detail(request, certification_date):
    auth_error = _get_admin_password_error_response(request)
    if auth_error is not None:
        return auth_error

    parsed_date = _parse_date(certification_date, 'date')
    certification = get_object_or_404(BalanceCertification, date=parsed_date)
    delete_photo(certification.photo_url)
    certification.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
