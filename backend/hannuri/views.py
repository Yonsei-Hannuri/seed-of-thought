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

import googleDriveAPI
import wordcloud

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


# load config data
with open('./config/googleDrive/folderId.json') as json_file:
    googleFolderId = json.load(json_file)

with open('./config/address.json') as json_file:
    address = json.load(json_file)


##SSL disregards in development environment
if(settings.DEBUG==True):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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
        return redirect(address['front'])
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
    return redirect(address['front'])

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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        
        is_userInfo_requested = self.request.query_params.get('userInfo', None)
        if is_userInfo_requested == 'true':
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Season.objects.order_by('-id')
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        
        current = self.request.query_params.get('current', None)
        if current:
            queryset = queryset.filter(is_current=True)

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
        if current:
            queryset = queryset.filter(is_current=True)

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
        except:
            return Response('', status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer): # Detgori 관련 create가 발생했을 때 호출되는 메쏘드의 일부분 custom
        parentSession = Session.objects.get(pk=self.request.POST['parentSession'])
        parentFolderId = parentSession.googleFolderId
        fileName = '댓거리' + str(parentSession.week) + '주차_'+ self.request.user.name + '.pdf'

        PDF = False
        try: # if deep copy not working (this happens when pdf file is too big)
            PDF = copy.deepcopy(self.request.FILES['pdf'])
        except:
            words = '{ }'
           
        if PDF != False:
            text = wordcloud.read_pdf(PDF.file)
            words = wordcloud.tokenizer(text)  

        googleId = googleDriveAPI.savePDF(fileName, parentFolderId, self.request.FILES['pdf'])
        PDF.name = googleId+'.pdf'
        serializer.save(googleId=googleId, author=self.request.user, words=words, pdf=PDF)
    
    def perform_destroy(self, instance):
        try:
            googleDriveAPI.deletePDF(instance.googleId)
        except:
            pass
        
        if os.path.exists('uploads/detgori/'+instance.googleId+'.pdf'):
            os.remove('uploads/detgori/'+instance.googleId+'.pdf')
        
        instance.delete()


class DetgoriCommentViewSet(viewsets.ModelViewSet):
    queryset = DetgoriComment.objects.order_by('-id')
    serializer_class = DetgoriCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class DetgoriCommentReplyViewSet(viewsets.ModelViewSet):
    queryset = DetgoriCommentReply.objects.order_by('-id')
    serializer_class = DetgoriCommentReplySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class SocialActivityViewSet(viewsets.ModelViewSet):
    queryset = SocialActivity.objects.order_by('-id')
    serializer_class = SocialActivitySerializer
    permission_classes = [IsAuthenticated, AlwaysReadOnly]

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
            recentNote = queryset[0]
            queryset = queryset.filter(page=recentNote.page)

        return queryset

