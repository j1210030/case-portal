"""
Django settings for dev_support project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import time
import socket
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

SETTINGS_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir ,'dev_support')
#PROJECT_PATH = os.path.abspath(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nvwd^)y1$rfck&ekqp07a%8^h6q^=^l9cng1r9$14-%v3ihe#@'

HOSTNAME = socket.gethostname()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
    #join(BASE_DIR,  'templates'),
    (TEMPLATE_PATH),
    ##'/srv/www/goragaku/goragaku/templates'
)

ALLOWED_HOSTS = ['35.196.214.31','35.190.153.225', 'localhost', '127.0.0.1']

UPLOAD_PATH = '/srv/www/gcase_tok/dev_support' #os.path.join(PROJECT_PATH, 'upload')
MEDIA_ROOT = "%s/upload/" % PROJECT_PATH
MEDIA_URL = '/upload/'

LOGIN_URL = '/user/login/'

LOGIN_EXEMPT_URLS = (
 r'^user/login/$',
 r'^user/logout/$',
 r'^admin/$'
)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gcase',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dev_support.login_required_middleware.LoginRequiredMiddleware'
]


#TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
 #   'django.template.context_processors.debug',
  #  'django.template.context_processors.request',
   # 'django.contrib.auth.context_processors.auth',
    #'django.contrib.messages.context_processors.messages',
#)

ROOT_URLCONF = 'dev_support.urls'
DATE_INPUT_FORMATS = ('%d/%m/%Y')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(TEMPLATE_PATH),],
        'OPTIONS': {
           'debug':DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]




WSGI_APPLICATION = 'dev_support.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
#'USER': 'school_db_user',
#'PASSWORD': 'nU6E7RE3',
#'HOST': '54.248.218.27',

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gcase',
        'USER': 'gcase_tok_user',
        'PASSWORD': 'nU6E7RE3',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_PATH = os.path.join(PROJECT_PATH,'gcase/static')
#STATIC_ROOT = '/Users/suhasg/Devel/python.proj/dev_support/gcase/static'
STATIC_ROOT = '/srv/www/gcase_tok/dev_support/gcase/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = (('%s/gcase/assets' % PROJECT_PATH),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


U_LOGFILE_SIZE = 1 * 1024 * 1024
U_LOGFILE_COUNT = 2
U_LOGFILE_APP1 = 'gcase'

#log_file_dir = '/Users/suhasg/Devel/python.proj/dev_support/logs/' #os.path.join(os.path.dirname(PROJECT_PATH),'logs')
log_file_dir = os.path.join(os.path.dirname(PROJECT_PATH),'logs/')
if not os.path.exists(log_file_dir):
    os.makedirs(log_file_dir)
log_file = log_file_dir + "gcase.log"
sql_log_file = log_file_dir + "gcase_sql.log"
console_log_file = log_file_dir + "gcase_console.log"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': log_file, #"/logs/admin_%d.log",
            #'filename': PROJECT_PATH + "/logs/admin.log",
            'maxBytes': U_LOGFILE_SIZE,
            'backupCount': U_LOGFILE_COUNT,
            'formatter': 'standard',
        },
        'logfile4sql': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': sql_log_file,
            'maxBytes': U_LOGFILE_SIZE,
            'backupCount': U_LOGFILE_COUNT,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },

        #'console':{
         #   'level':'INFO',
          #  'class':'logging.handlers.RotatingFileHandler',
           # 'filename': console_log_file,
            #'maxBytes': U_LOGFILE_SIZE,
            #'backupCount': U_LOGFILE_COUNT,
            #'formatter': 'standard',
        #},
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['logfile4sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'gcase': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

from .conf.constants import *
