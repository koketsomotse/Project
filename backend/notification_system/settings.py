"""
Django settings for notification_system project.

This file contains all the configuration settings for the Django project:
- Database configuration
- Authentication settings
- Third-party app configurations
- WebSocket and real-time settings
- Security settings
"""

from pathlib import Path
from decouple import config
import dj_database_url
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
# List of all Django apps, third-party apps, and local apps used in the project
INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin interface
    'django.contrib.auth',           # Authentication framework
    'django.contrib.contenttypes',   # Content type system
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file management
    # Third party apps
    'rest_framework',               # Django REST framework for API
    'rest_framework.authtoken',     # Token authentication
    'channels',                     # Channels for WebSocket support
    'corsheaders',                  # CORS headers for cross-origin requests
    # Local apps
    'notifications',                # Our notifications app
    'accounts',                     # Our accounts app
]

# Middleware configuration
# Order is important - these are processed from top to bottom for requests
# and from bottom to top for responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notification_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application path for traditional HTTP requests
WSGI_APPLICATION = 'notification_system.wsgi.application'

# ASGI application path for WebSocket support
ASGI_APPLICATION = 'notification_system.asgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_MLGywjFVmrqDpXsFf-r',
        'HOST': 'pg-2f9aeda3-koketsomotse92-18ca.e.aivencloud.com',
        'PORT': '25499',
        'TEST': {
            'NAME': 'test_defaultdb',
        },
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Password validation settings
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

# Internationalization settings
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = config('TIME_ZONE', default='UTC')
USE_I18N = config('USE_I18N', default=True, cast=bool)
USE_TZ = config('USE_TZ', default=True, cast=bool)

# CORS settings for development
# WARNING: Don't use CORS_ALLOW_ALL_ORIGINS=True in production!
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)  # For development only
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)

# Channels configuration for WebSocket support
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': config('CHANNEL_LAYERS_BACKEND', default='channels.layers.InMemoryChannelLayer')  # For development only
        # For production, use Redis:
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    }
}

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Static files configuration
STATIC_URL = config('STATIC_URL', default='static/')

# Default primary key field type
DEFAULT_AUTO_FIELD = config('DEFAULT_AUTO_FIELD', default='django.db.models.BigAutoField')
