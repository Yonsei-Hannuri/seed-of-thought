import json
from rest_framework import viewsets
from hannuri.serializer import *
from hannuri.models import *
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import copy
import datetime
import os
from django.conf import settings
from collections import defaultdict

from lib import googleDriveAPI, wordcount, validate

#custom permission
from hannuri.permissions import IsOwnerOrReadOnly, AlwaysReadOnly, AppendOnly
from rest_framework.permissions import IsAuthenticated

#인증 커스텀, 여기서 리턴 해주면 세션이 생김 ? 
# 내가 response에 따로 넣어주지도 않는데 
# 어떻게 쿠키를 자동으로 보내는 거지 (set-cookie라는 걸 설정해 주는 듯 )
from django.contrib.auth import login, logout
from django.shortcuts import redirect
import requests
import google_auth_oauthlib.flow

from lib.utils import filter_dict


# load config data
with open('./config/googleDrive/folderId.json') as json_file:
    googleFolderId = json.load(json_file)

with open('./config/address.json') as json_file:
    address = json.load(json_file)


##SSL disregards in development environment
if(settings.DEBUG==True):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def LogEverything(request):
    data = json.loads(request.body.decode('utf-8'))
    now = datetime.datetime.now()
    fileName = './log/everything/{}'.format(str(now.year)+'-'+str(now.month))
    is_existed = os.path.exists(fileName)
    with open(fileName, "a" if is_existed else "w") as log:
        log.write(str(now.day)+'일, '+str(now.hour)+'시\n')
        log.write('{} \n'.format(data))
        log.write('\n==================================================== \n')
        log.close()
    return HttpResponse('')


def Login(request):
    #google 에서 code 받고 그 code로 token을 받아서 그 token에 해당하는 email 받기
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        './config/googleDrive/client_secret.json',
        scopes = 'openid https://www.googleapis.com/auth/userinfo.email'
        )
    flow.redirect_uri = address['back'] + '/login'
    flow.fetch_token(code=request.GET.get('code'))
    credentials = flow.credentials
    token = credentials.token
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(token))
    email = response.json()['email']

    #받은 이메일을 통해서 로그인 시켜주기
    try: 
        user = User.objects.get(email=email)
        login(request, user)
        response = redirect(address['front'])
        response.set_cookie('isLogin', 'true', domain=address['common'], max_age=60*60*4)
        return response
    except:
        return redirect(address['front']+'?login=error')
    return redirect(address['front']+'?login=error')

def Signin(request):
    #google 에서 code 받고 그 code로 token을 받아서 그 token에 해당하는 email 받기
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        './config/googleDrive/client_secret.json',
        scopes = 'openid https://www.googleapis.com/auth/userinfo.email'
        )
    flow.redirect_uri = address['back'] + '/signin'
    flow.fetch_token(code=request.GET.get('code'))
    credentials = flow.credentials
    token = credentials.token
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(token))
    email = response.json()['email']
    
    #받은 이메일을 저장하기
    try: 
        user = User.objects.create(email=email)
        state_ = request.GET['state']
        state = json.loads(state_)
        name = state['name']
        generation = state['generation']

        user.name = name
        user.generation = generation
        user.save()

        return redirect(address['front']+'?type=signinSuccess')
        
    except:
        return redirect(address['front']+'?type=signinError')

def Logout(request):
    logout(request)
    response = redirect(address['front'])
    response.set_cookie('isLogin', 'false', domain=address['common'])
    return response

def ProfileColor(request):
    if request.user:
        request.user.color = request.POST['color']
        request.user.save()
        return HttpResponse('true')

    return HttpResponse('false')

def WordList(request, type, sessionId):
    if not(request.user):
        return HttpResponse('')
    if type=='mypage':
        wordList = []
        for detgori in request.user.detgori.all():
            wordList.append(detgori.words)
        return HttpResponse(json.dumps({'wordList':wordList}))
    elif type=='session':
        wordList = []
        session = Session.objects.get(pk=sessionId)
        session_detgori = session.detgori.all()
        for detgori in session_detgori:
            wordList.append(detgori.words)
        return HttpResponse(json.dumps({'wordList':wordList})) 
    return HttpResponse('')

def my_detgori_infos(userId, currentSeason):
        my_detgori_infos = list()
        currentSessions = currentSeason.session.all()
        currentDetgoris = Detgori.objects.filter(author=userId, parentSession__in=currentSessions)
        my_detgori_infos.append(currentSeason.title)
        for i in range(len(currentDetgoris)):
            my_detgori_infos.append({
                'detgoriId': currentDetgoris[i].id,
                'sessionTitle': currentDetgoris[i].parentSession.title,
                'detgoriTitle': currentDetgoris[i].title,
                'googleId': currentDetgoris[i].googleId,
            })
        return my_detgori_infos

def MypageInfo(request):
    if not(request.user):
        return HttpResponse('')
    else:
        try:
            season_id =  request.GET['seasonId'] 
        except:
            season_id = None
        if season_id:
            requested_season = Season.objects.get(id=season_id)
            season_detgori_infos = my_detgori_infos(request.user.id, requested_season)
            response_data = dict()
            response_data['seasonDetgoris'] = season_detgori_infos
            return HttpResponse(json.dumps(response_data)) 
        
        user_seasons = [season for season in request.user.act_seasons.order_by('-id')]
        current_infos = []
        if len(user_seasons) != 0 :
            current_infos = my_detgori_infos(request.user.id,  user_seasons[0])

        seasons = list()
        for season in user_seasons:
            season_info = {
                'id' : season.id,
                'year' : season.year,
                'semester' : season.semester
            }
            seasons.append(season_info)
        response_data = dict()
        response_data['seasonDetgoris'] = current_infos
        response_data['seasons'] = seasons
        response_data['name'] = request.user.name
        response_data['color'] = request.user.color
        response_data['generation'] = request.user.generation
        response_data['is_staff'] = request.user.is_staff

        return HttpResponse(json.dumps(response_data)) 

def FrontError(request):
    try:
        if request.user:
            data = json.loads(request.body.decode('utf-8'))
            error_log = data['errorMessage']['message']
            error_componet = data['from']
            now = datetime.datetime.now()
            fileName = './log/error-front/{}'.format(str(now.year)+'-'+str(now.month))
            is_existed = os.path.exists(fileName)
            with open(fileName, "a" if is_existed else "w") as log:
                log.write(str(now.day)+'일, '+str(now.hour)+'시\n')
                log.write('{} \n'.format(error_componet))
                log.write('{} \n'.format(error_log))
                try: log.write('{}님 이용중 발생 \n'.format(request.user.name))
                except: pass
                log.write('\n==================================================== \n')
                log.close()
    except: pass
    return HttpResponse('')

def ArchiveView(request):
    if not(request.user):
        return HttpResponse('')
    if 'target' in request.GET.keys(): target = request.GET['target']
    if 'id' in request.GET.keys(): target_id = request.GET['id']
    if 'id2' in request.GET.keys(): target_id_2 = request.GET['id2']
    word_count = defaultdict(int)
    if target == 'hannuri':
        seasons = Season.objects.filter(is_current=False)
        for season in seasons:
            season_words = json.loads(season.words)
            for key, val in season_words.items():
                word_count[key] += val
    elif target == 'season':
        season = Season.objects.filter(id=int(target_id))
        word_count = json.loads(season[0].words)
    elif target == 'author':
        season_sessions = Session.objects.filter(season=int(target_id_2))
        author_season_detgori = \
            Detgori.objects.filter(author=int(target_id), parentSession__in=season_sessions)
        for detgori in author_season_detgori:
            detgori_word = json.loads(detgori.words)
            for key, val in detgori_word.items():
                word_count[key] += val

    word_number = 80
    words_ranked = sorted(word_count.items(), key=lambda x: -x[1])
    if len(words_ranked) > word_number : keys_ranked = [key for key, val in words_ranked[0:word_number]]
    else: keys_ranked = [key for key, val in words_ranked]
    word_count_ranked = filter_dict(word_count, lambda item: item[0] in keys_ranked)

    return HttpResponse(json.dumps(word_count_ranked))

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

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.order_by('-id')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

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
        parentFolderId = parentSession.googleFolderId
        fileName = '댓거리' + str(parentSession.week) + '주차_'+ self.request.user.name + '.pdf'

        try: # if deep copy not working (this happens when pdf file is too big)
            PDF = copy.deepcopy(self.request.FILES['pdf'])
            text = wordcount.read_pdf(PDF.file)
            words = wordcount.tokenizer(text)  
        except:
            text = ''
            words = '{ }'
        googleId = googleDriveAPI.savePDF(fileName, parentFolderId, self.request.FILES['pdf'])
        self.request.FILES['pdf'].name = googleId+'.pdf'
        serializer.save(googleId=googleId, pureText=text, author=self.request.user, words=words, pdf=self.request.FILES['pdf'])

        #check users acting season, if first detgori add current season as his acting season.
        act_seasons = [season.id for season in self.request.user.act_seasons.all()]
        current_season = Season.objects.get(is_current=True).pk
        if not current_season in act_seasons:
            self.request.user.act_seasons.add(current_season)
        self.request.user.save()

    def perform_destroy(self, instance):
        try:
            googleDriveAPI.deletePDF(instance.googleId)
        except:
            pass
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

            season = self.request.query_params.get('season', None)
            author = self.request.query_params.get('author', None)
            if season != None and author != None:
                queryset = queryset.filter(author=int(author), season=int(season))
            return queryset

class FreeNoteViewSet(viewsets.ModelViewSet):
    queryset = FreeNote.objects.order_by('-id')
    serializer_class = FreeNoteSerializer
    permission_classes = [IsAuthenticated, AppendOnly]

    def get_queryset(self):
        queryset = self.queryset

        notePage = self.request.query_params.get('notePage', None)
        recentNotePage = self.request.query_params.get("recentNotePage", None)
        if notePage:
            queryset = queryset.filter(page=notePage)
        elif recentNotePage:
            if len(queryset) != 0:
                recentNote = queryset[0]
                queryset = queryset.filter(page=recentNote.page)

        return queryset

