from django.db import models
from lib import googleDriveAPI
import requests
import json
import os
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin