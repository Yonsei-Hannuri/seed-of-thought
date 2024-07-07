from rest_framework import serializers
from cowriter.models import *

class SubjectKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectKeyword
        fields = ['keyword']

class SubjectSerializer(serializers.ModelSerializer):
    # custom 필드를 read only로 하려면 아래 처럼 선언시에 read_only 값을 설정해줘야함
    # https://stackoverflow.com/questions/75980386/django-declaring-a-read-only-field-on-serializer
    keywords = SubjectKeywordSerializer(many=True, read_only=True)
    class Meta:
        model = Subject
        fields = ['source', 'purpose','content', 'keywords']
        # 시리얼라이즈를 통해서 Read작업과 Create작업에 필요한 인수를 구분하기
        # https://stackoverflow.com/questions/31675803/should-i-write-two-different-serializers-for-requests-post-and-get
        read_only_fields = [ 'keywords' ]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'

class EssaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Essay
        fields = '__all__'

class TopciSentenceKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopciSentenceKeyword
        fields = ['keyword']

class TopicSentenceSerializer(serializers.ModelSerializer):
    keywords = TopciSentenceKeywordSerializer(many=True)
    class Meta:
        model = TopicSentence
        fields = ['essay', 'content','order', 'keywords']

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = '__all__'