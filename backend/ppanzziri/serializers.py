from rest_framework import serializers

from ppanzziri.models import (
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
    WritingManuscriptPhoto,
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


class WritingManuscriptPhotoSerializer(serializers.ModelSerializer):
    photo_url = serializers.CharField(source='photo_url_original', read_only=True)

    class Meta:
        model = WritingManuscriptPhoto
        fields = [
            'id',
            'photo_url',
            'photo_url_original',
            'photo_url_compressed',
            'photo_url_resized',
            'order',
        ]


class WritingRecordSerializer(serializers.ModelSerializer):
    submitted_at = serializers.SerializerMethodField()
    analyzed_at = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    manuscript_photos = WritingManuscriptPhotoSerializer(many=True, read_only=True)

    def get_submitted_at(self, obj):
        if not obj.submitted_at:
            return ''
        return obj.submitted_at.strftime('%Y-%m-%dT%H:%M:%S')

    def get_analyzed_at(self, obj):
        if not obj.analyzed_at:
            return ''
        return obj.analyzed_at.strftime('%Y-%m-%dT%H:%M:%S')

    def get_start_time(self, obj):
        if not obj.start_time:
            return ''
        return obj.start_time.strftime('%H:%M')

    def get_end_time(self, obj):
        if not obj.end_time:
            return ''
        return obj.end_time.strftime('%H:%M')

    class Meta:
        model = WritingRecord
        fields = [
            'id',
            'date',
            'start_time',
            'end_time',
            'timelapse_video_url',
            'topics',
            'char_count',
            'manuscript_photos',
            'submitted_at',
            'analysis_status',
            'summary',
            'keywords',
            'analyzed_at',
        ]


