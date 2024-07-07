from rest_framework import viewsets
from cowriter.serializer import *
from cowriter.models import *

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.order_by('-id')
    serializer_class = SubjectSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.order_by('-id')
    serializer_class = KeywordSerializer

class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.order_by('-id')
    serializer_class = EdgeSerializer

class EssayViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.order_by('-id')
    serializer_class = EssaySerializer

class TopicSentenceViewSet(viewsets.ModelViewSet):
    queryset = TopicSentence.objects.order_by('-id')
    serializer_class = TopicSentenceSerializer

class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.order_by('-id')
    serializer_class = PhaseSerializer



