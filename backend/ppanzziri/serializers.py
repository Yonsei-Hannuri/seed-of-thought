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
    created_at = serializers.SerializerMethodField()
    photo_url = serializers.CharField(source='photo_url_original', read_only=True)

    def get_created_at(self, obj):
        # Keep created_at format stable for frontend parsing.
        if not obj.created_at:
            return ''
        return obj.created_at.strftime('%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = BudgetRecord
        fields = [
            'id',
            'type',
            'transaction_date',
            'amount',
            'memo',
            'photo_url',
            'photo_url_original',
            'photo_url_compressed',
            'photo_url_resized',
            'created_at',
            'effective_segments',
            'tags',
        ]


class BalanceCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceCertification
        fields = ['id', 'date', 'photo_url', 'created_at']
