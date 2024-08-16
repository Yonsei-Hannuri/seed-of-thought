from rest_framework import serializers
from cowriter.models import *

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

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
    keyword_1nm = serializers.ReadOnlyField(source='keyword1.keyword_nm')
    keyword_2nm = serializers.ReadOnlyField(source='keyword2.keyword_nm')
    class Meta:
        model = EssayMindmap
        fields = ['essay_id', 'keyword1', 'keyword2', 'keyword_1nm', 'keyword_2nm']

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'

class ParagraphHistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphHist
        fields = '__all__'