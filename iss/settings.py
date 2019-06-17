"""
Django settings for iss project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import iss.dbconn

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@@s5y_4qru2$7zpj_g0#@lq2m!z2@t13g)3wbi=n2scgs^pd1e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_PORT = 25
EMAIL_HOST = '10.6.0.7'
EMAIL_HOST_USER = 'gamma@baikal-ttk.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER






# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'iss.localdicts',
    'iss.begin',
    'iss.monitor',
    'iss.equipment',
    'iss.working',
    'iss.inventory',
    'iss.onyma',
    'iss.maps',
    'iss.regions',
    'iss.exams',
    'iss.blocks',
    'iss.electro',
    'mptt',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'iss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf',
                'django.template.context_processors.static',
                'iss.context_processors.my_static_url',
                'iss.context_processors.user_tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'iss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = iss.dbconn.DATABASES


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

ROOT_URL = 'http://127.0.0.1:10000/'

MY_STATIC_URL = 'http://127.0.0.1:10000/'
MY_STATIC_URL2 = 'http://127.0.0.1:10000/'

EXAM_IP = '127.0.0.1'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'users': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/log/monitor.log',
            'formatter':'users',
        },
        'file_inventory': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/log/inventory.log',
            'formatter':'users',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/debugging.log',
            'formatter':'verbose',
        },
        'events_json': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/events.log',
            'formatter': 'verbose',
        },
        'load_data': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/loaddata.log',
            'formatter': 'verbose',
        },
        'projects': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/projects.log',
            'formatter': 'users',
        },
        'devices': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/devices.log',
            'formatter': 'users',
        },
    },
    'loggers': {
        'monitor': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'events': {
            'handlers': ['events_json'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'inventory': {
            'handlers': ['file_inventory'],
            'level': 'INFO',
            'propagate': True,
        },
        'debugging': {
            'handlers': ['file_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'loadding': {
            'handlers': ['load_data'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'projects': {
            'handlers': ['projects'],
            'level': 'INFO',
            'propagate': True,
        },
        'devices': {
            'handlers': ['devices'],
            'level': 'INFO',
            'propagate': True,
        },

    },
}





CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '10.6.0.88:11211',
        'TIMEOUT':360000,
        'OPTIONS': {
            'MAX_ENTRIES':10000000,
        }
    }
}



DATE_FORMAT = "%d.%m.%Y"