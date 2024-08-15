from rest_framework import serializers
from cowriter.models import *

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['source', 'purpose','content']

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        # 기존의 유효성 검사를 먼저 수행합니다.
        valid = super().is_valid(raise_exception=raise_exception)

        if not valid:
            return False
        
        keyword_name = self.validated_data.get('name')
        
        if keyword_name == '':
            self.add_error('name', '키워드는 빈 문자열일 수 없습니다.')
            valid = False

        return True

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

class EssayMindmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssayMindmap
        fields = '__all__'

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = '__all__'

class PhaseHistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhaseHist
        fields = '__all__'