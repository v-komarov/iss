.. contents:: Оглавление
    :depth: 2



Взаимодействие с другими системами
==================================


crontab
-------

 ::

    # m h  dom mon dow   command
    */1 * * * * cd /srv/django/iss;/usr/bin/python manage.py zenoss_krsk
    */10 * * * * cd /srv/django/iss;/usr/bin/python manage.py mail_sibttk_ru
    10 14 * * * cd /srv/django/iss;/usr/bin/python manage.py zenoss_krsk all
    10 9 * * * cd /srv/django/iss;/usr/bin/python manage.py snmp_devices zenoss_krsk
    21 20 * * * cd /srv/django/iss;/usr/bin/python manage.py get_issdata
    */5 * * * * cd /srv/django/iss;/usr/bin/python manage.py send_reports_accident
    */1 * * * * cd /srv/django/iss;/usr/bin/python manage.py send_iss_accident


zenoss_krsk
-----------

Получение данных из zenoss Красноярска через api


mail_sibttk_ru
--------------

Получение сообщения с почтового адреса.


snmp_devices
------------

snmp сканирование сетевых устройств


get_issdata
-----------

Получение данных из ИСС по используемым портам на оборудовании.


send_reports_accident
---------------------

Обмен данными с системой подготовки статистических отчетов через api.
Реализован функционал создания в reports записи об аварии, обновления, удаления.


send_iss_accident
-----------------

Обмен данными с ИСС. Создание работ на стороне ИСС. Получение id работ, открытие интерфейса ИИС работ из интерфейса "Оперативный журнал".


