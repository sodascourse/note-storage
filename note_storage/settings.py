import json
import os

import dj_database_url
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.join(BASE_DIR, ".env")
if load_dotenv and os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = int(os.environ.get('DEBUG', '0')) == 1

ALLOWED_HOSTS = json.loads(os.environ.get('ALLOWED_HOSTS', '[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'auth_api',
    'simple_note',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'note_storage.urls'

WSGI_APPLICATION = 'note_storage.wsgi.application'


# Database

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600),
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    )
}
