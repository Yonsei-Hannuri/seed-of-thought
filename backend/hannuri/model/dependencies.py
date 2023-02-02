from django.db import models
from lib import googleDriveAPI
import requests
import json
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

googleFolderId = os.environ.get('GOOGLE_DRIVE_ROOT_FOLDER')