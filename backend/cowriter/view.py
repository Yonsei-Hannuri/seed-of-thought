from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from cowriter.serializer import *
from cowriter.models import *

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.order_by('-id')
    serializer_class = SubjectSerializer

    # POST는 제공하지 않는다. 
    # GET만 제공

class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.order_by('-id')
    serializer_class = KeywordSerializer

    # 왜 create를 오버라이딩 하고 get_serializer(data=keywords, many=True)를 하면 필드가 없어도 에러를 내지 않을까? 그냥 빈 문자열 처리..?
    def create(self, request):
        keywords = request.data
        
        if not isinstance(keywords, list):
            return Response({"error": "Expected a list of items"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=keywords, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EssayViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.order_by('-id')
    serializer_class = EssaySerializer

class EssayMindmapViewSet(viewsets.ModelViewSet):
    queryset = EssayMindmap.objects.order_by('-id')
    serializer_class = EssayMindmapSerializer

class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.order_by('-id')
    serializer_class = PhaseSerializer

    # 사용자 요청에 따라 Phase를 생성해 저장하고, 전달한다.
    