from rest_framework import serializers

from ppanzziri.models import (
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
    PushSubscription,
    WritingGoal,
    WritingRecord,
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


class WritingRecordSerializer(serializers.ModelSerializer):
    submitted_at = serializers.SerializerMethodField()
    analyzed_at = serializers.SerializerMethodField()

    def get_submitted_at(self, obj):
        if not obj.submitted_at:
            return ''
        return obj.submitted_at.strftime('%Y-%m-%dT%H:%M:%S')

    def get_analyzed_at(self, obj):
        if not obj.analyzed_at:
            return ''
        return obj.analyzed_at.strftime('%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = WritingRecord
        fields = [
            'id',
            'content',
            'char_count',
            'submitted_at',
            'analysis_status',
            'summary',
            'keywords',
            'analyzed_at',
        ]


class PushSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushSubscription
        fields = ['id', 'endpoint', 'p256dh', 'auth', 'created_at']
        read_only_fields = ['id', 'created_at']


class WritingGoalSerializer(serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        if not obj.updated_at:
            return ''
        return obj.updated_at.strftime('%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = WritingGoal
        fields = ['id', 'target_chars', 'updated_at']
        read_only_fields = ['id', 'updated_at']
