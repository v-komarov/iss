.. contents:: Оглавление
    :depth: 2



Описание API
============


Список агрегаторов
------------------

http://10.6.0.22:8000/equipment/devices/apidata/?action=get_agregators

Формат вывода json

Пример вывода

 ::

    {"domen": "zenoss_krsk", "mac": "1c:7e:e5:85:46:00", "location": "g.Zelenogorsk, Naberezhnaya, 28, gate 1 (--1)", "descr": "DGS-3620-28SC Gigabit Ethernet Switch", "serial": "PVXE1B7000812", "ipaddress": "10.41.116.1", "uplink_ports": [25], "name": "ZLG41-116#1"}

uplink_ports - список uplink портов



Данные lldp
-----------

http://10.6.0.22:8000/equipment/devices/apidata/?action=get_lldpdata

Формат вывода json

Пример вывода

 ::

    {"domen": "zenoss_krsk", "lldp": {"ports": [{"mac": "34:08:04:47:fa:00", "port": 26}, {"mac": "ec:22:80:2d:8b:20", "port": 25}]}, "mac": "ec:22:80:2d:84:00", "location": "g.Achinsk, Druzhbyi Narodov, 6, gate 2 (---2)", "descr": "DES-3200-28/C1 Fast Ethernet Switch", "serial": "R3DZ1E6003594", "ipaddress": "10.246.172.81", "name": "46-72.8.2gt2#81"}

ports - список портов , mac адресов "соседей".




Запросы к Onyma
---------------

url http://10.6.0.22:8000/onyma/apidata


Получение баланса (в валюте лицевого счета) на лицевом счете на текущую дату
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Запрос **GET**

Параметры:

#. action=get_balans_ls
#. ls=<лицевой счет>

Вывод : json формат


Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata/?action=get_balans_ls&ls=2178523


Пример ответ:

 ::

    {"result": "-69.001151"}

