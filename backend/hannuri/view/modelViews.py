import json
from rest_framework import viewsets
from hannuri.serializer import *
from hannuri.models import *
from hannuri.permissions import IsOwnerOrReadOnly, AlwaysReadOnly, AppendOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import copy
import os
from lib import validate
from hannuri.permissions import IsOwnerOrReadOnly, AlwaysReadOnly, AppendOnly
from rest_framework.permissions import IsAuthenticated
from hannuri.component import pdfTextExtracter, koreanWordAnalyzer, wordCounter 
import uuid

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


    def perform_create(self, serializer): # Detgori 관련 create가 발생했을 때 호출되는 메쏘드의 일부분 custom

        if not validate.is_PDF(self.request.FILES['pdf'].name): 
            raise Exception('pdf 파일이 아닙니다.')

        #parse nouns of a detgori and upload on the google drive
        parentSession = Session.objects.get(pk=self.request.POST['parentSession'])
        fileName = '댓거리' + str(parentSession.week) + '주차_'+ self.request.user.name + '.pdf'
        
        text = ''
        words = '{ }'
        try: # if deep copy not working (this happens when pdf file is too big)
            PDF = copy.deepcopy(self.request.FILES['pdf'])
            text = pdfTextExtracter.extract_text(PDF.file)
            nouns = koreanWordAnalyzer.extract_nouns(text)  
            word_count = wordCounter.count(nouns)
        except:
            pass

        googleId = str(uuid.uuid4())
        self.request.FILES['pdf'].name = googleId+'.pdf'
        serializer.save(googleId=googleId, pureText=text, author=self.request.user, words=json.dumps(word_count), pdf=self.request.FILES['pdf'])
        #check users acting season, if first detgori add current season as his acting season.
        act_seasons = [season.id for season in self.request.user.act_seasons.all()]
        current_season = Season.objects.get(is_current=True).pk
        if not current_season in act_seasons:
            self.request.user.act_seasons.add(current_season)
        self.request.user.save()

    def perform_destroy(self, instance):
        #check whether was a detgori was the only detgori of the season
        #if so erase this acting season.
        user_detgoris = Detgori.objects.filter(author=self.request.user)
        user_detgori_seasons = [detgori.parentSession.season.pk for detgori in user_detgoris]
        removing_detgori_season = instance.parentSession.season.pk
        if user_detgori_seasons.count(removing_detgori_season) == 1:
            self.request.user.act_seasons.remove(removing_detgori_season)
            self.request.user.save()

        if os.path.exists('uploads/detgori/'+instance.googleId+'.pdf'):
            os.remove('uploads/detgori/'+instance.googleId+'.pdf')
        
        instance.delete()

    def get_queryset(self):
        queryset = self.queryset

        season = self.request.query_params.get('season', None)
        author = self.request.query_params.get('author', None)
        if season != None and author != None:
            queryset = queryset.filter(author=int(author), season=int(season))
        return queryset


class DetgoriReadTimeViewSet(viewsets.ModelViewSet):
    queryset = DetgoriReadTime.objects.order_by('-id')
    serializer_class = DetgoriReadTimeSerializer
    permission_classes = [IsAuthenticated, AppendOnly]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs): 
        request.data['reader'] = request.user.id
        return super().create(request, *args, **kwargs)
       