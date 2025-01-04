from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count

from hannuri.serializer import *
from hannuri.models import *
from hannuri.permissions import IsOwnerOrReadOnly, AlwaysReadOnly, AppendOnly
from hannuri.component import objectStorage
from hannuri.job import detgoriDerivedDataJob
import copy
from lib import validate
import uuid
from datetime import datetime

import logging
logger = logging.getLogger('common')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        
        is_userInfo_requested = self.request.query_params.get('userInfo', None)
        if is_userInfo_requested == 'true':
            queryset = queryset.filter(id=self.request.user.id)

        season_active_user = self.request.query_params.get('seasonActiveUser', None)
        if season_active_user != None:
            queryset = queryset.filter(act_seasons__in=[int(season_active_user)])

        return queryset

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.order_by('-id')
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        
        current = self.request.query_params.get('current', None)
        condition = self.request.query_params.get('condition', None)
        if current:
            queryset = queryset.filter(is_current=True)
        if condition == 'no_current':
            queryset = queryset.filter(is_current=False)
        return queryset

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.order_by('-id')
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        
        current = self.request.query_params.get('current', None)
        seasonSessionInfos = self.request.query_params.get('seasonSessionInfos', None)
        if current:
            queryset = queryset.filter(is_current=True)
        elif seasonSessionInfos:
            try:
                current_season = Season.objects.get(is_current=True)
                if current_season:
                    queryset = queryset.filter(season=current_season).order_by('id')
            except:
                pass
        return queryset


class SessionReadfileViewSet(viewsets.ModelViewSet):
    queryset = SessionReadfile.objects.order_by('-id')
    serializer_class = SessionReadfileSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]


class DetgoriViewSet(viewsets.ModelViewSet):
    queryset = Detgori.objects.order_by('-id')
    serializer_class = DetgoriSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 

        try: 
            self.perform_create(serializer) 
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Detgori 관련 create가 발생했을 때 호출되는 메쏘드의 일부분 
    def perform_create(self, serializer):
        if not validate.is_PDF(self.request.FILES['pdf'].name): 
            raise Exception('pdf 파일이 아닙니다.')        
        # OLTP
        ## generate file id
        session = Session.objects.get(pk=self.request.POST['parentSession'])
        season = session.season
        short_uuid = str(uuid.uuid4()).split("-")[0]
        fileName = f'{season.year}/{season.semester}학기/{session.week}주차/댓거리/{self.request.user.name}-{short_uuid}.pdf'

        pdf_bytes = copy.deepcopy(self.request.FILES['pdf'])
        objectStorage.save(pdf_bytes, fileName, 'application/pdf')
        detgori = serializer.save(googleId=fileName, author=self.request.user)

        ## check users acting season, if first detgori add current season as his acting season.
        act_seasons = [season.id for season in self.request.user.act_seasons.all()]
        current_season = Season.objects.get(is_current=True).pk
        if not current_season in act_seasons:
            self.request.user.act_seasons.add(current_season)
        self.request.user.save()

        detgoriDerivedDataJob.create_derived_async(copy.deepcopy(self.request.FILES['pdf']), detgori.pk)


    def perform_destroy(self, instance):
        #check whether was a detgori was the only detgori of the season
        #if so erase this acting season.
        user_detgoris = Detgori.objects.filter(author=self.request.user)
        user_detgori_seasons = [detgori.parentSession.season.pk for detgori in user_detgoris]
        removing_detgori_season = instance.parentSession.season.pk
        if user_detgori_seasons.count(removing_detgori_season) == 1:
            self.request.user.act_seasons.remove(removing_detgori_season)
            self.request.user.save()
        
        detgori_id = instance.pk
        detgoriDerivedDataJob.remove_derived(detgori_id)
        instance.delete()


    def get_queryset(self):
        queryset = self.queryset

        season = self.request.query_params.get('season', None)
        author = self.request.query_params.get('author', None)
        if season != None and author != None:
            queryset = queryset.filter(author=int(author), season=int(season))
        return queryset

class SentencePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SentenceViewSet(viewsets.ModelViewSet):
    queryset = Sentence.objects.order_by('-id')
    serializer_class = SentenceSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]
    pagination_class = SentencePagination

    def get_queryset(self):
        queryset = self.queryset

        tokens = self.request.query_params.get('tokens', None) 
        if tokens is None:
            return queryset

        # 토큰에 해당하는 단어를 가진 문장을 반환한다. (여러 토큰이 있는 경우 모든 토큰을 포함하는 문장만 선택)
        tokens = [token.strip() for token in tokens.split(',')]
        words = Word.objects.filter(word__in=tokens)

        targets = SentenceWord.objects\
            .filter(word__in=words)\
            .values('sentence')\
            .annotate(wc=Count('word'))\
            .filter(wc=len(words))
        
        # 조회 순서를 매주 변경한다.현재 연도와 주차 정보를 조합하여 시드 생성
        year, week, _ = datetime.now().isocalendar()
        week_seed = year * 100 + week  # 예: 2024년 10주차 -> 202410
        
        queryset = queryset.filter(id__in=targets.values('sentence'))\
            .extra(
                select={'ordering': f'ABS(id * {week_seed} %% 1000000)'},
                order_by=['ordering']
            )

        return queryset

class DetgoriReadTimeViewSet(viewsets.ModelViewSet):
    queryset = DetgoriReadTime.objects.order_by('-id')
    serializer_class = DetgoriReadTimeSerializer
    permission_classes = [IsAuthenticated, AppendOnly]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs): 
        request.data['reader'] = request.user.id
        return super().create(request, *args, **kwargs)
       