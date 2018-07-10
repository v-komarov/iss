.. contents:: Оглавление
    :depth: 2



Взаимодействие с другими системами
==================================


.. index:: crontab
crontab -l
----------

 ::

    */10 *	* * * cd /srv/django/iss;/usr/bin/python manage.py mail_sibttk_ru
    */5 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_reports_accident
    */1 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_iss_accident
    */2 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_email_message
    0 4	* * * /srv/django/iss/tools/backup/backup-db
    5 4	* * * /srv/django/iss/tools/backup/backup-dir
    */2 *	* * * cd /srv/django/iss;/usr/bin/python manage.py get_iss_drp
    10 21   * * * cd /srv/django/iss/log;>events.log
    30 2   * * 2 cd /srv/django/iss;/usr/bin/python manage.py get_radiuslog
    8  *    * * * cd /srv/django/iss;/usr/bin/python manage.py get_dogcode_by_login
    35 *    * * * cd /srv/django/iss;/usr/bin/python manage.py device_port_on
    50 *    * * * cd /srv/django/iss;/usr/bin/python manage.py geo_data



.. index:: get_dogcode_by_login
get_dogcode_by_login
--------------------

Для случайных 100 логинов поиск номера договора в Onyma и запись в таблицу модели **client_login_log**.
Определение номера порта комутатора доступа по таблице модели **client_mac_log**

 ::

    8  *    * * * cd /srv/django/iss;/usr/bin/python manage.py get_dogcode_by_login
