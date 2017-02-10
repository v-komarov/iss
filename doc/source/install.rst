.. contents:: Оглавление
    :depth: 3



Протокол восстановления (установки)
===================================

.. index:: install

Стандартный путь расположения приложения
----------------------------------------

**/srv/django/iss**

Структура каталогов проекта на 10.02.2017

 ::

        ├── iss
        │   ├── begin
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── forms.py
        │   │   ├── forms.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── migrations
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── context_processors.py
        │   ├── context_processors.pyc
        │   ├── dbconn.py
        │   ├── dbconn.pyc
        │   ├── equipment
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apidata.py
        │   │   ├── apidata.pyc
        │   │   ├── apps.py
        │   │   ├── apps.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── management
        │   │   │   ├── commands
        │   │   │   │   ├── _add_devices2scan.py
        │   │   │   │   ├── device_list_catv.py
        │   │   │   │   ├── device_list_catv.pyc
        │   │   │   │   ├── device_list.py
        │   │   │   │   ├── device_list.pyc
        │   │   │   │   ├── device_tools.py
        │   │   │   │   ├── device_tools.pyc
        │   │   │   │   ├── device_tools_test.py
        │   │   │   │   ├── device_tools_test.pyc
        │   │   │   │   ├── get_issdata.py
        │   │   │   │   ├── get_issdata.pyc
        │   │   │   │   ├── get_issdata.py.orig
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── __init__.pyc
        │   │   │   │   ├── make_graph.py
        │   │   │   │   ├── make_graph.pyc
        │   │   │   │   ├── snmp_devices.py
        │   │   │   │   └── snmp_devices.pyc
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── __init__.py
        │   ├── __init__.pyc
        │   ├── inventory
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── localdicts
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── apps.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   └── views.py
        │   ├── log
        │   ├── monitor
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── filedata.py
        │   │   ├── filedata.pyc
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── jsondata.py
        │   │   ├── jsondata.pyc
        │   │   ├── management
        │   │   │   ├── commands
        │   │   │   │   ├── get_iss_drp.py
        │   │   │   │   ├── get_iss_drp.pyc
        │   │   │   │   ├── __init__.py
        │   │   │   │   ├── __init__.pyc
        │   │   │   │   ├── mail_sibttk_ru.py
        │   │   │   │   ├── mail_sibttk_ru.pyc
        │   │   │   │   ├── send_email_message.py
        │   │   │   │   ├── send_email_message.pyc
        │   │   │   │   ├── send_iss_accident.py
        │   │   │   │   ├── send_iss_accident.pyc
        │   │   │   │   ├── send_reports_accident.py
        │   │   │   │   ├── send_reports_accident.pyc
        │   │   │   │   ├── zenoss_krsk.py
        │   │   │   │   └── zenoss_krsk.pyc
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── othersources.py
        │   │   ├── othersources.pyc
        │   │   ├── templatetags
        │   │   │   ├── __init__.py
        │   │   │   ├── __init__.pyc
        │   │   │   ├── monitor_extras.py
        │   │   │   └── monitor_extras.pyc
        │   │   ├── tests.py
        │   │   ├── tools.py
        │   │   ├── tools.pyc
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── mydecorators.py
        │   ├── mydecorators.pyc
        │   ├── onyma
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apidata.py
        │   │   ├── apidata.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── soap
        │   │   │   ├── dognum_get_balans.php
        │   │   │   ├── ls_get_balans.php
        │   │   │   └── service.htms
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   └── views.py
        │   ├── settings.py
        │   ├── settings.pyc
        │   ├── urls.py
        │   ├── urls.pyc
        │   ├── working
        │   │   ├── admin.py
        │   │   ├── admin.pyc
        │   │   ├── apps.py
        │   │   ├── __init__.py
        │   │   ├── __init__.pyc
        │   │   ├── migrations
        │   │   │   ├── __init__.py
        │   │   │   └── __init__.pyc
        │   │   ├── models.py
        │   │   ├── models.pyc
        │   │   ├── tests.py
        │   │   ├── urls.py
        │   │   ├── urls.pyc
        │   │   ├── views.py
        │   │   └── views.pyc
        │   ├── wsgi.py
        │   └── wsgi.pyc
        ├── json_api.sh
        ├── manage.py
        ├── static
        │   ├── css
        │   │   ├── bootstrap.css
        │   │   ├── bootstrap.css.map
        │   │   ├── bootstrap-datetimepicker.css
        │   │   ├── bootstrap-datetimepicker.min.css
        │   │   ├── bootstrap.min.css
        │   │   ├── bootstrap.min.css.map
        │   │   ├── bootstrap-theme.css
        │   │   ├── bootstrap-theme.css.map
        │   │   ├── bootstrap-theme.min.css
        │   │   ├── bootstrap-theme.min.css.map
        │   │   ├── images
        │   │   │   ├── ui-icons_444444_256x240.png
        │   │   │   ├── ui-icons_555555_256x240.png
        │   │   │   ├── ui-icons_777620_256x240.png
        │   │   │   ├── ui-icons_777777_256x240.png
        │   │   │   ├── ui-icons_cc0000_256x240.png
        │   │   │   └── ui-icons_ffffff_256x240.png
        │   │   ├── jquery.multiselect.css
        │   │   ├── jquery-ui.css
        │   │   ├── jquery-ui.structure.css
        │   │   ├── jquery-ui.structure.min.css
        │   │   ├── jquery-ui.theme.css
        │   │   └── jquery-ui.theme.min.css
        │   ├── equipment
        │   │   ├── agregators.css
        │   │   ├── agregators.js
        │   │   ├── devices.css
        │   │   ├── devices.js
        │   │   ├── footnode.css
        │   │   ├── footnode.js
        │   │   ├── topology.css
        │   │   └── topology.js
        │   ├── favicon.ico
        │   ├── fonts
        │   │   ├── glyphicons-halflings-regular.eot
        │   │   ├── glyphicons-halflings-regular.svg
        │   │   ├── glyphicons-halflings-regular.ttf
        │   │   ├── glyphicons-halflings-regular.woff
        │   │   └── glyphicons-halflings-regular.woff2
        │   ├── inventory
        │   │   ├── devicescheme.css
        │   │   └── devicescheme.js
        │   ├── js
        │   │   ├── bootstrap-datetimepicker.min.js
        │   │   ├── bootstrap.js
        │   │   ├── bootstrap.min.js
        │   │   ├── datepicker-ru.js
        │   │   ├── jquery-2.2.4.js
        │   │   ├── jquery-3.1.0.min.js
        │   │   ├── jquery.json.js
        │   │   ├── jquery-migrate-1.4.1.min.js
        │   │   ├── jquery-migrate-3.0.0.js
        │   │   ├── jquery.multiselect.filter.js
        │   │   ├── jquery.multiselect.filter.ru.js
        │   │   ├── jquery.multiselect.js
        │   │   ├── jquery-ui.js
        │   │   ├── jquery-ui.min.js
        │   │   ├── jquery.validate.js
        │   │   ├── messages_ru.js
        │   │   └── npm.js
        │   ├── monitor
        │   │   ├── accidents.css
        │   │   ├── accidents.js
        │   │   ├── columns_filter.js
        │   │   ├── dialogs.js
        │   │   ├── dragtable.js
        │   │   ├── facefix.js
        │   │   ├── headfilter.js
        │   │   ├── jquery.tablescroll.js
        │   │   ├── messages.css
        │   │   ├── monitor.css
        │   │   ├── monitor.js
        │   │   └── user-settings.js
        │   └── working
        │       ├── working.css
        │       └── working.js
        ├── templates
        │   ├── begin.html
        │   ├── equipment
        │   │   ├── agregators_list.html
        │   │   ├── devices_list.html
        │   │   ├── footnode_list.html
        │   │   ├── form2.html
        │   │   ├── form3.html
        │   │   ├── form.html
        │   │   └── topology.html
        │   ├── footer.html
        │   ├── header.html
        │   ├── index.html
        │   ├── inventory
        │   │   ├── devicescheme_list.html
        │   │   └── schemeform.html
        │   ├── mainmenu.html
        │   ├── menu.html
        │   ├── monitor
        │   │   ├── accidentform2.html
        │   │   ├── accidentform.html
        │   │   ├── accident_list.html
        │   │   ├── containergroup.html
        │   │   ├── drplist.html
        │   │   ├── eventform.html
        │   │   ├── event_list.html
        │   │   ├── event_menu.html
        │   │   ├── mailform2.html
        │   │   ├── mailform.html
        │   │   ├── message_list.html
        │   │   ├── message_mss.html
        │   │   ├── tablehead.html
        │   │   ├── tablerowdata.html
        │   │   ├── usersettings.html
        │   │   └── zkllist.html
        │   └── working
        │       └── work_list.html
        ├── tools
        │   ├── backup
        │   │   ├── backup-db
        │   │   └── backup-dir
        │   └── zenapitool
        │       ├── config.py
        │       ├── config.pyc
        │       ├── device_list.txt
        │       ├── exception.py
        │       ├── exception.pyc
        │       ├── external.py
        │       ├── external.pyc
        │       ├── getdeviceip.sh
        │       ├── LICENSE
        │       ├── README.md
        │       ├── zenapitool.conf
        │       ├── zenapitool.log
        │       ├── zenapitool.py
        │       ├── zenoss.py
        │       └── zenoss.pyc



Версии установленого основного программного обеспечения
-------------------------------------------------------

python
~~~~~~

 ::

        >>> import platform
        >>> platform.python_version()
        '2.7.12'
        >>>


django
~~~~~~

 ::

    root@iss:/srv/django/iss# python manage.py shell
    Python 2.7.12 (default, Nov 19 2016, 06:48:10)
    Type "copyright", "credits" or "license" for more information.

    In [1]: import django

    In [2]: django.VERSION
    Out[2]: (1, 9, 6, 'final', 0)


postgresql
~~~~~~~~~~

 ::

    root@iss:/srv/django/iss# python manage.py dbshell
    Pager is always used.
    psql (9.5.5)
    Type "help" for help.

    iss=> select version();
                                                         version
    -----------------------------------------------------------------------------------------------------------------
     PostgreSQL 9.5.5 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.2) 5.4.0 20160609, 64-bit
    (1 row)


Список и версии python пакетов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django и прочие пакеты python следует устанвливать утилитой **pip** с указанием версий.

Не все пакеты из списка ниже необходимы для базовых функций проекта.

 ::

    root@iss:/srv/django/iss# pip list
    alabaster (0.7.9)
    Babel (2.3.4)
    decorator (4.0.10)
    Django (1.9.6)
    docutils (0.12)
    easysnmp (0.2.4)
    gunicorn (19.4.5)
    imagesize (0.7.1)
    ipython (2.4.1)
    Jinja2 (2.8)
    lorem-ipsum-generator (0.3)
    MarkupSafe (0.23)
    MySQL-python (1.2.5)
    mysqlclient (1.3.7)
    netsnmp-python (1.0a1)
    networkx (1.11)
    pexpect (4.0.1)
    pip (9.0.1)
    ply (3.9)
    psycopg2 (2.6.2)
    ptyprocess (0.5)
    pyasn1 (0.1.9)
    pycrypto (2.6.1)
    Pygments (2.1.3)
    pymssql (2.1.3)
    pysmi (0.0.7)
    pysnmp (4.3.2)
    pysnmp-mibs (0.1.6)
    pytz (2016.6.1)
    requests (2.11.1)
    setuptools (20.7.0)
    simplegeneric (0.8.1)
    six (1.10.0)
    snowballstemmer (1.2.1)
    Sphinx (1.4.6)
    tabulate (0.7.7)
    transliterate (1.8.1)
    wheel (0.29.0)
    yolk (0.4.3)



Настройка статики
-----------------

Файл settings.py
~~~~~~~~~~~~~~~~

 ::

    STATIC_URL = 'http://10.6.0.22:10000/static/admin/'

    ROOT_URL = '/'

    MY_STATIC_URL = 'http://10.6.0.22:10000/'


nginx файл /etc/nginx/iss
~~~~~~~~~~~~~~~~~~~~~~~~~

 ::

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



Подключение к базам данных (файл dbconn.py)
-------------------------------------------

 ::

    DATABASES = {

        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'iss',
            'USER': 'iss',
            'PASSWORD':'*******',
        },

        'zenoss_krsk' : {
            'ENGINE':'django.db.backends.mysql',
            'NAME':'zenoss_zep',
            'USER':'iss',
            'PASSWORD':'*******',
            'HOST':'10.6.0.129',
            'PORT':'',
        },


    }



    ONYMA_USERNAME = 'iss2'
    ONYMA_PASSWORD = '********'


    ISS_MSSQL_USERNAME = "django"
    ISS_MSSQL_PASSWORD = "*********"


    ZENOSS_API_USERNAME = "vkomarov"
    ZENOSS_API_PASSWORD = "********"



Создание структуры данных
-------------------------

 ::

    cd /srv/django/iss
    python manage.py makemigrations
    python manage.py migrate


Перенос данных
~~~~~~~~~~~~~~

#. Способ : используя штатные средства создания резервных копий и загрузки сервера баз данных
#. Способ : использую штатные средства django - dumpdata и loaddata


Запуск проекта в режиме использования собственного сервера
----------------------------------------------------------

 ::

    cd /srv/django/iss
    python manage.py runserver
