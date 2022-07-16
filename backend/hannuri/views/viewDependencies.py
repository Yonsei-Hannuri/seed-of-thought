import json
from rest_framework import viewsets
from hannuri.serializer import *
from hannuri.models import *

from hannuri.permissions import IsOwnerOrReadOnly, AlwaysReadOnly, AppendOnly
from rest_framework.permissions import IsAuthenticated

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