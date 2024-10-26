from rest_framework import serializers
from cowriter.models import *
from cowriter.utils import is_valid_sentence

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

    def validate_keyword_nm(self, name):        
        if name.strip() == '':
            raise serializers.ValidationError('키워드는 빈 문자열일 수 없습니다.')

        return name

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

    def validate_paragraph_content(self, content):
        if not is_valid_sentence(content):
            raise serializers.ValidationError("하나의 완성된 문장을 입력해주세요.")
        return content

class ParagraphHistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphHist
        fields = '__all__'