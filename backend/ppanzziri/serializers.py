from rest_framework import serializers

from ppanzziri.models import (
    BalanceCertification,
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
)


class BudgetEffectiveSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetEffectiveSegment
        fields = ['id', 'effective_from', 'effective_to', 'segment_amount']


class BudgetRecordTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetRecordTag
        fields = ['id', 'name', 'amount']


class BudgetRecordSerializer(serializers.ModelSerializer):
    effective_segments = BudgetEffectiveSegmentSerializer(many=True, read_only=True)
    tags = BudgetRecordTagSerializer(many=True, read_only=True)

    class Meta:
        model = BudgetRecord
        fields = [
            'id',
            'type',
            'transaction_date',
            'amount',
            'memo',
            'photo_url',
            'created_at',
            'effective_segments',
            'tags',
        ]


class BalanceCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceCertification
        fields = ['id', 'date', 'photo_url', 'created_at']
