from pathlib import Path
import os
import environ
import logging

ENV = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

ALLOWED_HOSTS = [ENV('FRONT_DOMAIN'), ENV('API_DOMAIN'), ENV('COWRITER_DOMAIN')]
SECRET_KEY = ENV('DJANGO_SECRET_KEY')

HANNURI_URL = 'https://' + ENV('FRONT_DOMAIN')
COWRITER_URL = 'https://' + ENV('COWRITER_DOMAIN')
API_URL = 'https://' + ENV('API_DOMAIN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV('DEBUG')
if DEBUG:
    ALLOWED_HOSTS = ["*"]
    HANNURI_URL = 'http://' + ENV('FRONT_DOMAIN')
    COWRITER_URL = 'http://' + ENV('COWRITER_DOMAIN')
    API_URL = 'http://' + ENV('API_DOMAIN')
    ##SSL disregards in development environment
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'hannuri.apps.HannuriConfig',
    'cowriter.apps.CowriterConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware', #CORS 관련
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'social_django.context_processors.backends',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Logging
LOGGING = {
    'version': 1,  # the dictConfig format version
    'disable_existing_loggers': False, 
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'log/warning.log',
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'common': {
            'handlers': ['console', 'file']
        }
    }
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / './db/db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'hannuri.User'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/uploads/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
    )
}


SESSION_COOKIE_AGE = 60 * 60 * 4

if DEBUG == True:
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        HANNURI_URL,
        COWRITER_URL,
        "http://localhost:6006", # storybook
    ]

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_COOKIE_DOMAIN = ENV("DOMAIN")

CSRF_TRUSTED_ORIGINS = [
    HANNURI_URL,
    COWRITER_URL,
    API_URL
]
