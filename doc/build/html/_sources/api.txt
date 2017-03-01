.. contents:: Оглавление
    :depth: 3



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


.. index:: Onyma

Запросы к Onyma
---------------



Получение баланса (в валюте лицевого счета) на лицевом счете на текущую дату по номеру лицевого счета
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata

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




Тест
~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=test

Вывод : text
1

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=test


Пример ответ:

 ::

    1



Получение баланса (в валюте лицевого счета) на лицевом счете на текущую дату по номеру договора
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_balans_dognum
#. dognum=<Номер договора>

Вывод : text
<Название значения>:<Значение>;

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_balans_dognum&dognum=241100300


Пример ответ:

 ::

    balans:-81.501151;




Получение справочника групп (городов)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_groups

Вывод : text
<Название группы>:<Значение>,<id группы>:<Значение>;
<Название группы>:<Значение>,<id группы>:<Значение>;
<Название группы>:<Значение>,<id группы>:<Значение>;
<Название группы>:<Значение>,<id группы>:<Значение>;
<Название группы>:<Значение>,<id группы>:<Значение>;
<Название группы>:<Значение>,<id группы>:<Значение>;
...

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_groups


Пример ответ:

 ::

    name:WiMax_Канск,id:22570;name:Кошурниково,id:32292;name:Уяр,id:32251;name:Абакан,id:23648;name:Филиал Сибирь,id:20832;name:КЦ КТТК,id:18290;name:МР Сибирь,id:28331;name:Сибирь (Сиблинк),id:39011;name:МР-Сибирь (Взлетка),id:29171;name:Аскиз,id:32295;name:Бородино,id:32296;name:Лесосибирск,id:32311;name:Мариинск,id:32294;name:МР-Сибирь (Северо-Западный район),id:29173;name:root,id:1;name:Зеленогорск,id:23650;name:Назарово,id:23654;name:Регион Красноярск,id:23653;name:МР-Сибирь (Правый Берег),id:29172;name:Новоенисейск,id:35311;name:Минусинск,id:32313;name:Овсянка,id:32411;name:WiMax_Сибирь,id:21818;name:Иланская,id:32252;name:ТТК-Красноярск,id:28995;name:Саянская,id:32291;name:Боготол,id:32293;name:Заозерный,id:23651;name:Красноярск-ADSL,id:23652;name:Черногорск,id:23655;name:WiMax_Ачинск,id:21832;name:Ачинск,id:23649;name:Решоты,id:32271;name:Регион Сибирь,id:31671;name:Дивногорск,id:32312;name:ТТК Сибирь,id:28332;



Создание договора
~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=dog_create
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. pgid=<id группы (города)>
#. dogcode=<Номер договора>

Вывод : text id созданного договора

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_create&pgid=28995&dogcode=8888888888&username=iss2&password=111111


Пример ответ:

 ::

    2381970


Установка даты договора
~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_dogdate
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. dogid=<id договора>
#. dogdate=<Дата договора в виде строки "день.месяц.год">

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_date&dogid=2381953&dogdate=15.02.2017&username=iss2&password=111111



Установка ФИО договора
~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_fio
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. dogid=<id договора>
#. lastname=<Фамилия> кодировка utf-8
#. firstname=<Имя> кодировка utf-8
#. secondname=<Отчество> кодировка utf-8

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_fio&dogid=2381953&username=iss2&password=111111&lastname=Иванов&firstname=Иван&secondname=Иванович




Установка телефона договора
~~~~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_phone
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. dogid=<id договора>
#. phone=<Номер телефона> кодировка utf-8

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_phone&dogid=2381953&username=iss2&password=111111&phone=8-905-222-8888




Установка адреса договора
~~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_address
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. dogid=<id договора>
#. city=<Город> кодировка utf-8
#. street=<Улица> кодировка utf-8
#. house=<Дом> кодировка utf-8
#. room=<Квартира> кодировка utf-8

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_address&dogid=2381953&username=iss2&password=111111&city=Красноярск&street=Совсем Любая&house=5 а&room=100



Установка номера договора
~~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_dognum
#. username=<логин для onyma>
#. password=<пароль для onyma>
#. dogid=<id договора>
#. dognum=<Номер договора> кодировка utf-8

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_dognum&dogid=2381953&username=iss2&password=111111&dognum=9999999999





Получение учетного имени, тарифного плана, ресурса, логина, даты начала
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_user_services_dognum
#. dognum=<Номер договора>

Вывод : text
srv:<Значение>;start_date:<Значение>;login:<Значение>;tarif:<Значение>;sitename:<Значение>;

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_user_services_dognum&dognum=241115694


Пример ответ:

 ::

    srv:[ТТК] Подключение ШПД;start_date:2016-11-28T21:00:00.000Z;login:241115694;tarif:Сибирь вТТКайся 290р 60000К Красноярск, Минусинск 2016;sitename:i.241115694;
    srv:[ТТК] Доступ в личный кабинет;start_date:2016-11-28T21:00:00.000Z;login:241115694;tarif:Technological;sitename:lc.241115694;
    srv:[ТТК] Доп.услуги Интернет;start_date:2016-11-30T21:00:00.000Z;login:ttk_dop;tarif:[Сибирь] Wi-Fi роутер(в рассрочку на 18 мес.);sitename:du.241115694;



Получение id договора по номеру договора
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_dogid
#. dognum=<Номер договора>

Вывод : text
<id договора>


Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_dogid&dognum=241115694


Пример ответ:

 ::

    2319030
