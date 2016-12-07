.. contents:: Оглавление
    :depth: 2



Примеры конфигов
================



nginx
-----


.. code-block:: sh

 upstream iss {
     server unix:/run/uwsgi/app/iss.socket;
 }




 server {
         listen        10000;
         server_name   10.6.0.22;

         root /srv/django/iss/static;
         index index.html;

         location / {
         add_header Access-Control-Allow-Origin *;
         autoindex on;
         }

         location /static/admin {
         alias /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/;
         autoindex on;
         }

 }


 server {

         listen        8080;
         server_name   10.6.0.22;


         location / {

         include uwsgi_params;
         uwsgi_pass iss;
         }

 }
 
 
 
 
uwsgi
-----
 
 
.. code-block:: sh

 
 cd /etc/uwsgi-emperor/
 ls
 emperor.ini  vassals
 cat emperor.ini
 
 [uwsgi]
 plugins-dir=/usr/lib/uwsgi/plugins/
 autoload = true
 master = true
 workers = 5
 no-orphans = true
 log-date = true
 emperor = /etc/uwsgi-emperor/vassals

 cd /vassals
 ls
 iss.ini  README
 
 cat iss.ini
 
 [uwsgi]
 plugins = python27
 chdir=/srv/django/iss
 module=iss.wsgi:application
 master=True
 pidfile=/run/uwsgi/app/iss.pid
 vacuum=True
 max-requests=5000
 daemonize=/var/log/uwsgi/app/iss.log
 uid=www-data
 gid=www-data
 socket=/run/uwsgi/app/iss.socket



django
------

.. code-block:: python

 import os

 BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

 SECRET_KEY = '@@s5y_4qru2$7zpj_g0#@lq2m!z2@t13g)3wbi=n2scgs^pd1e'

 DEBUG = True

 ALLOWED_HOSTS = []


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


 DATABASES = iss.dbconn.DATABASES


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


 LANGUAGE_CODE = 'ru-ru'

 TIME_ZONE = 'UTC'

 USE_I18N = True

 USE_L10N = True

 USE_TZ = True

 STATIC_URL = 'http://10.6.0.22:10000/static/admin/'

 ROOT_URL = '/'

 MY_STATIC_URL = 'http://10.6.0.22:10000/'

 SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
