"""
Django settings for cfehome project.

"""

from pathlib import Path
from dotenv import load_dotenv
import datetime
import os

curr_time = datetime.datetime.now()
t_stamp = curr_time.timestamp()

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-&111f(t6pjb_)zi-8x*o^$j!ujh0#ttgk$-)i^joh%0nv$n!o*'
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.128','192.168.1.63', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'products',
    'django_crontab',
    
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

ROOT_URLCONF = 'cfehome.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/home/jesse/Projects/DRF/backend/cfehome/products/templates',],
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

WSGI_APPLICATION = 'cfehome.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.mysql',
        'NAME':    os.getenv('MYSQL_DATABASE'), #'cfehomeproj',
        'USER':    os.getenv('MYSQL_USER'), #'cfehomeuser',
        'PASSWORD':os.getenv('MYSQL_PASSWORD'), #'wskky',
        'HOST':    'localhost',
        'PORT':    '',
    }
}

# Password validation

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

# STATIC_ROOT = "/home/jesse/Projects/DRF/backend/cfehome/static"
# STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     "/home/jesse/DRF/backend/cfehome/products/static",
# ]

#Production Settings for static locations
STATIC_ROOT = '/var/www/static'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    '/home/jesse/DRF/backend/cfehome/products/static',
]

# Media files settings
MEDIA_ROOT = '/var/www/media'
MEDIA_URL  = '/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'    
    ],
}

# Django-Crontab Cronjobs
CRONJOBS = [
    ('*/10 * * * *', 'products.cron.fetch_and_save_inmates'),
    ('10 1 * * *', 'products.cron.get_sex_offenders'),
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "/home/jesse/DRF/debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
