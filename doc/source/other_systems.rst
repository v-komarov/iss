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


.. index:: mail_sibttk_ru
mail_sibttk_ru
--------------

Получение сообщения с почтового адреса. Добавляется в "Оперативный журнал" как событие.

 ::

    */10 *	* * * cd /srv/django/iss;/usr/bin/python manage.py mail_sibttk_ru


.. index:: send_reports_accident
send_reports_accident
---------------------

Обмен данными с системой подготовки статистических отчетов через api.
Реализован функционал создания в reports записи об аварии, обновления, удаления.
Механизм изменения кодов справочника реализован только для красноярского региона и для других случаев работать не будет.

 ::

    */5 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_reports_accident


.. index:: get_iss_drp
get_iss_drp
-----------

Опрос системы ИСС и наполенние аварии сообщениями ДРП.

 ::

    */2 *	* * * cd /srv/django/iss;/usr/bin/python manage.py get_iss_drp


.. index:: send_iss_accident
send_iss_accident
-----------------

Обмен данными с ИСС. Создание работ на стороне ИСС. Получение id работ, открытие интерфейса ИИС работ из интерфейса "Оперативный журнал".

 ::

    */1 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_iss_accident


.. index:: send_email_message
send_email_message
------------------

Отправка подготовленных сообщений email в МСС об начале и завершении аварии.

 ::

    */2 *	* * * cd /srv/django/iss;/usr/bin/python manage.py send_email_message




.. index:: get_radiuslog
get_radiuslog
-------------
.. |date| date:: %d.%m.%Y
Загрузка предварительно подготовленной информации логины, mac адреса, circuit-tag (если есть) в таблицу модели **client_login_log**
Информация предварительно готовится на сервере 10.6.0.88 (на |date| опрос только radius сервера красноярского региона 10.6.0.104)

 ::

    30 2   * * 2 cd /srv/django/iss;/usr/bin/python manage.py get_radiuslog


.. index:: get_dogcode_by_login
get_dogcode_by_login
--------------------

Для случайных 100 логинов поиск номера договора в Onyma и запись в таблицу модели **client_login_log**.
Определение номера порта комутатора доступа по таблице модели **client_mac_log**

 ::

    8  *    * * * cd /srv/django/iss;/usr/bin/python manage.py get_dogcode_by_login

.. index:: device_port_on
device_port_on
--------------

Для 100 случайно выбранных портов привязка к договору Onyma по данным таблицы модели **client_login_log**.


.. index:: geo_data
geo_data
--------

Для 100 случайер выбранных адресов домов определение гео координат и запись в json поле **geo** таблицы модели **address_house**

 ::

    50 *    * * * cd /srv/django/iss;/usr/bin/python manage.py geo_data




.. index:: zenoss_krsk
zenoss_krsk
-----------

Получение данных из zenoss Красноярска через api

Реализовано через самозацикленный скрипт:

 ::

    root@iss:~# cat /srv/django/iss/reget_zenoss_data.sh
    #!/bin/sh


    while true
    do

    cd /srv/django/iss
    /usr/bin/python manage.py zenoss_krsk

    sleep 1

    done



Запуск через rc.local

 ::

    /usr/bin/screen -dmS zenoss /srv/django/iss/reget_zenoss_data.sh &


.. index:: zenoss_irk
zenoss_irk
----------

Получение данных из zenoss Иркутска через api

Реализовано через самозацикленный скрипт:

 ::

    root@iss:/srv/django/iss# cat reget_zenoss_irk_data.sh
    #!/bin/sh


    while true
    do

    cd /srv/django/iss
    /usr/bin/python manage.py zenoss_irk

    sleep 1

    done


Запуск через rc.local

 ::

    /usr/bin/screen -dmS irk /srv/django/iss/reget_zenoss_irk_data.sh &


.. index:: zenoss_chi
zenoss_chi
----------

Получение данных из zenoss Читы через api

Реализовано через самозацикленный скрипт:

 ::

    root@iss:/srv/django/iss# cat reget_zenoss_chi_data.sh
    #!/bin/sh


    while true
    do

    cd /srv/django/iss
    /usr/bin/python manage.py zenoss_chi

    sleep 1

    done

Запуск через rc.local

 ::

    /usr/bin/screen -dmS chi /srv/django/iss/reget_zenoss_chi_data.sh &



.. |date| date:: %d.%m.%Y

.. attention:: В настоящее время данные с zenoss Читы в корректном виде не поступают.



Команды выполняемые вручную
---------------------------

device_use_port
~~~~~~~~~~~~~~~

Установка статуса портов используется пользователями или нет на основании данных csv файла.


device_tech_port
~~~~~~~~~~~~~~~~

Установка технологических портов на основании данных csv файла.


Загрузка данных через api
-------------------------


Загрузка даных в таблицу модели **client_mac_address**
:ref:`api-client-mac-log`: