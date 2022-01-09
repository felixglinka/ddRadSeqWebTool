"""
Django settings for backend backend.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the backend like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-a_jqm*7+$wqd2$2zscx&5m6%imgu4doc_(0%7=#x)bbj&etlfb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ddgrader.haifa.ac.il', '132.75.251.57']


# Application definition

INSTALLED_APPS = [
    'api',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chunked_upload'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'resources')
STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(os.path.dirname(__file__), 'resources').replace('\\','/'),
# )
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "api/static"),
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CHUNKED_UPLOAD_PATH_BASE = 'home/felix/ddRadSeqWebTool/chunked_uploads/'
CHUNKED_UPLOAD_PATH = CHUNKED_UPLOAD_PATH_BASE + '%Y/%m/%d'

SEQUENCING_YIELD_MULTIPLIER = 1000000
MAX_NUMBER_SELECTFIELDS = 100*2+1
MAX_BINNING_LIMIT = 1000
BINNING_STEPS = 10
MAX_GRAPH_VIEW = 100
MAX_GRAPH_RANGE = MAX_GRAPH_VIEW * BINNING_STEPS
PAIRED_END_ENDING = 'paired end'
SINGLE_END_ENDING = 'single end'
ILLUMINA_100 = 100
ILLUMINA_150 = 150
ADAPTORCONTAMINATIONSLOPE = 0.4508
OVERLAPSLOPE =  0.35333
POLYMORPHISM_MODIFIER = 1000
DENSITY_MODIFIER = 100000
MAX_RECOMMENDATION_NUMBER = 5

COMMONLYUSEDRARECUTTERS=['EcoRI', 'PstI', 'SbfI', 'SphI']
COMMONLYUSEDECORIFREQUENTCUTTERS=['MseI', 'MspI', 'SphI', 'SbfI','NlaIII']
COMMONLYUSEDPSTIFREQUENTCUTTERS=['MspI', 'SphI', 'MseI', 'HhaI']
COMMONLYUSEDSBFIFREQUENTCUTTERS=['EcoRI', 'MseI', 'MspI', 'SphI']
COMMONLYUSEDSPHIFREQUENTCUTTERS=['MluCI']
