.. contents:: Оглавление
    :depth: 2

.. index:: commands

Команды
=======

.. epigraph::

   Система пользовательских команд


Приложение equipment
--------------------

.. epigraph::

   Расположение команд iss/equipment/management/commands


.. index:: device_list


device_list
~~~~~~~~~~~

Выводит список устройств в *csv* файл из модели *inventory/devices*. Передаваемый параметр команды - имя файла. Файл записсывается в каталог iss/equipment/csv. Формат строки файла: ip;serial;model;address

 Пример:
 ::

   python manage.py device_list test.csv



.. index:: geo_data

geo_data
~~~~~~~~

Для 100 случайер выбранных адресов домов определение гео координат и запись в json поле **geo** таблицы модели **address_house**




.. index:: geo_city

geo_city
~~~~~~~~

Заполнение координат для городов и населенных пунктов



.. index:: data_to_es

data_to_es
~~~~~~~~~~

Заполнение базы **ElasticSearch** из справочников. Передаваемые параметры: **device** - заполнение моделей сетевых устройств, **city** - заполнение из справочника городов, **street** - заполнение из справочника улиц



Приложение localdicts
---------------------


.. epigraph::

   Расположение команд iss/localdicts/management/commands


.. index:: check_full_address



check_full_address
~~~~~~~~~~~~~~~~~~

Проверяет наличие общих адресов: т.е. только город (без улицы) или город и только улица (без номера дома). Если таких общих адресов нет - адрес создается.


 Пример:
 ::

   python manage.py check_full_address


Приложение monitor
------------------


.. epigraph::

   Расположение команд iss/monitor/management/commands


.. index:: get_asterisk_log

get_asterisk_log
~~~~~~~~~~~~~~~~

Принимает построчно данные CDR с астериска (в составе сервиса xinetd)




.. index:: get_avaya_log

get_avaya_log
~~~~~~~~~~~~~

Принимает построчно данные CDR с AVAYA (в составе сервиса xinetd)



.. index:: zenoss_chi

zenoss_chi
~~~~~~~~~~

Обеспечивает формирование json запроса к zenoss Читы. Добавляет информацию в таблицу событий.


.. index:: zenoss_irk

zenoss_irk
~~~~~~~~~~

Обеспечивает формирование json запроса к zenoss Иркутска. Добавляет информацию в таблицу событий.



.. index:: zenoss_krsk

zenoss_krsk
~~~~~~~~~~~

Обеспечивает формирование json запроса к zenoss Красноярска. Добавляет информацию в таблицу событий.



.. index:: mail_sibttk_ru

mail_sibttk_ru
~~~~~~~~~~~~~~

Получение сообщения с почтового адреса. Добавляется в "Оперативный журнал" как событие.

 Пример:
 ::

    */10 *	* * * cd /srv/django/iss;/usr/bin/python manage.py mail_sibttk_ru


Приложение regions
------------------

.. index:: clear_stores

clear_stores
~~~~~~~~~~~~

Удаляет записи по скадам, а именно из моделей  : store_rest, store_in, store_out, store_rest_log, store_carry, store_list

