from django.db import models
from lib import googleDriveAPI
import requests
import json
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
with open('./config/googleDrive/folderId.json') as json_file:
    googleFolderId = json.load(json_file)