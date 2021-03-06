.. contents:: Оглавление
    :depth: 3



Описание API
============





Проверка списка ЗКЛ
-------------------

http://10.6.0.22:8000/equipment/devices/apidata/?action=get_zkllist&ipaddress=55.33.3.13

Запрос **GET**

Параметры:

#. action=get_zkllist
#. ipaddress=<ip адрес коммутатора>


Формат вывода json

Пример вывода

 ::

    [{"sysname": "abk-3-sa1x52-13g5", "ip": "55.33.3.13", "port_reserv": 0, "port_use": 24, "address": "\u0433.\u0410\u0431\u0430\u043a\u0430\u043d \u0421\u043e\u0432\u0435\u0442\u0441\u043a\u0430\u044f 113", "port_tech": 2}]



.. _api-client-mac-log:




Вывод строки георгафических адресов
-----------------------------------

http://10.6.0.22:8000/equipment/devices/apidata/

Запрос **POST**

Параметры:

#. "action":"writeaddressstr" (JSON)
#. "iplist":[] (JSON)

 Пример запроса
 ::

    curl --header "Content-Type: application/json" -X POST --data '{"action":"writeaddressstr","iplist":['55.33.8.2','55.33.10.2']}' http://10.6.0.22:8000/equipment/devices/apidata/

 Пример ответа
 ::
 
    {"address": " \u0433.\u0410\u0431\u0430\u043a\u0430\u043d [\u0414\u0440\u0443\u0436\u0431\u044b \u041d\u0430\u0440\u043e\u0434\u043e\u0432] 16, [\u041f\u0443\u0448\u043a\u0438\u043d\u0430] 99, "}




Список сетевых элементов без ip адреса управления
-------------------------------------------------
http://10.6.0.22:8000/equipment/devices/apidata2/?action=get_netelemnotip

Запрос **GET**

Параметры:

#. action=get_netelemnotip

Формат вывода csv

Пример вывода


 ::

    NETELEMID;NETELEM;MODEL;STATUS;PORTS;COMBO;SLOTS;CITY;STREET;HOUSE;
    2;Название сетевого элемента;DES-3200-28/C1 Fast Ethernet Switch;Используется;24;2;2;г.Дивногорск;Наб. Ленина;27;
    2;Название сетевого элемента;DGS-3620-28SC Gigabit Ethernet Switch;Используется;0;4;24;г.Красноярск;Телевизорная;1 стр 1 к204;
    2;Название сетевого элемента;;;0;0;0;г.Красноярск;Ленина;62;
    2;Название сетевого элемента;DES-3200-10/C1 Fast Ethernet Switch;Используется;8;1;1;г.Красноярск;Куйбышева;95;
    2;Название сетевого элемента;DES-3200-26/C1;Используется;24;2;0;г.Красноярск;Крупской;36;
    3;Сетевой элемент;DES-3200-10/C1 Fast Ethernet Switch;Используется;8;1;1;г.Красноярск;Крайняя;2а;



Список устройств без связанных сетевых элементов
------------------------------------------------
http://10.6.0.22:8000/equipment/devices/apidata2/?action=get_devicesnotelement

Запрос **GET**

Параметры:

#. action=get_devicesnotelement

Формат вывода csv

Пример вывода


 ::

    DEVICEID;MODEL;SERIAL;STATUS;PORTS;COMBO;SLOTS;CITY;STREET;HOUSE;
    12124;DES-1210-10/ME;Используется;8;1;0;г.Красноярск;Железнодорожников;26а;
    12125;DGS-3612G Gigabit Ethernet Switch;Используется;0;4;8;г.Красноярск;Куйбышева;95;
    6560;;;0;0;0;г.Красноярск;Киренского;89;
    6552;;;0;0;0;г.Красноярск;Свободный;46;
    8762;;;0;0;0;г.Дивногорск;Шоссейная;1а;
    6653;;;0;0;0;г.Лесосибирск;Победы;31б;
    6658;;;0;0;0;ст.Чунояр;Дом связи;-;
    6719;;;0;0;0;г.Красноярск;Кутузова;74;
    9639;;;0;0;0;пос.Саянский;Школьная;13;
    11025;;;0;0;0;г.Красноярск;Свердловская;59а;
    8468;;;0;0;0;г.Абакан;Пушкина;78а;
    10446;;;0;0;0;г.Красноярск;Мира;156;
    11009;;;0;0;0;г.Красноярск;Светлогорская;27;
    9862;;;0;0;0;г.Ачинск;1-й Микрорайон;39а;
    11986;;;0;0;0;г.Красноярск;Северное шоссе;23д;
    6762;;;0;0;0;г.Абакан;Пушкина;78а;
    6825;;;0;0;0;г.Лесосибирск;Привокзальная;59а;
    6954;;;0;0;0;г.Красноярск;Батурина;10;
    7015;;;0;0;0;г.Лесосибирск;Привокзальная;59а;
    8763;;;0;0;0;г.Дивногорск;Заманская;подмостом;
    7019;;;0;0;0;г.Лесосибирск;5-й Микрорайон;6а;
    7035;;;0;0;0;г.Красноярск;Телевизорная;1 стр 1 к202;
    8766;;;0;0;0;г.Сосновоборск;Ленинского комсомола;2;
    11001;;;0;0;0;г.Ачинск;1-й Микрорайон;35;
    9863;;;0;0;0;г.Ачинск;3-й Привокзальный;14а;
    10453;;;0;0;0;г.Красноярск;Северное шоссе;23д;
    11472;;;0;0;0;г.Красноярск;Киренского;89;
    7187;;;0;0;0;пос.Кошурниково;Невского;1;
    11382;;;0;0;0;г.Красноярск;Светлогорская;19;
    11887;;;0;0;0;г.Красноярск;Весны;22;
    8764;;;0;0;0;г.Железногорск;Школьная;39а;
    11884;;;0;0;0;г.Красноярск;9 Мая;54;



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




Установка адреса договора 2
~~~~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2


Запрос **GET**

Параметры:

#. action=dog_set_address2
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

(Пробелы в адресе заменены символами подчеркивания)

Вывод : Нет

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=dog_set_address&dogid=2381953&username=iss2&password=111111&city=Красноярск&street=Совсем_Любая&house=5_а&room=100







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




Получение id тарифного плана по его названию
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_tmid
#. tmname=<Название тарифного плана> кодировка utf-8

Вывод : text
<id тарифного плана>


Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_tmid&tmname=Сибирь РП индивидуальный ЭВРЗ


Пример ответ:

 ::

    19268

Пример ответ при отсутствии результата:

 ::

    error





Получение учетного имени, тарифного плана, ресурса, логина, даты начала (по id договора)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_user_services_dogid
#. dognum=<Номер договора>

Вывод : text
Первой строкой баланс
srv:<Значение>;start_date:<Значение>;login:<Значение>;tarif:<Значение>;sitename:<Значение>;

Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_user_services_dogid&dogid=2319030


Пример ответ:

 ::

    balans:185.691798;
    srv:[ТТК] Подключение ШПД;start_date:2016-11-28T21:00:00.000Z;login:241115694;tarif:Сибирь вТТКайся 290р 60000К Красноярск, Минусинск 2016;sitename:i.241115694;
    srv:[ТТК] Доступ в личный кабинет;start_date:2016-11-28T21:00:00.000Z;login:241115694;tarif:Technological;sitename:lc.241115694;
    srv:[ТТК] Доп.услуги Интернет;start_date:2016-11-30T21:00:00.000Z;login:ttk_dop;tarif:[Сибирь] Wi-Fi роутер(в рассрочку на 18 мес.);sitename:du.241115694;



Получение списка доменов
~~~~~~~~~~~~~~~~~~~~~~~~

url http://10.6.0.22:8000/onyma/apidata2

Запрос **GET**

Параметры:

#. action=get_domain_list


Вывод : text
domainid:<id домена>;domainidup:<id родительского домена>;domain:<Название домена>;domaincod:<Код домена>;


Пример запрос:

 ::

    http://10.6.0.22:8000/onyma/apidata2/?action=get_domain_list


Пример ответ:

 ::

    domainid:18971;domainidup:18970;domain:Фролово;domaincod:;
    domainid:28152;domainidup:19790;domain:cttc_slk;domaincod:;
    domainid:28153;domainidup:28152;domain:vzm;domaincod:;
    domainid:28158;domainidup:28152;domain:kirov;domaincod:;
    domainid:28159;domainidup:28152;domain:kaluga;domaincod:;
    domainid:20410;domainidup:19790;domain:moskow;domaincod:;
    domainid:21155;domainidup:18310;domain:sever;domaincod:;
    domainid:22619;domainidup:22610;domain:e-tihoretsk;domaincod:;
    domainid:24392;domainidup:22150;domain:birobidzhan;domaincod:;
    domainid:22610;domainidup:19670;domain:e-rostov_reg;domaincod:;
    domainid:22612;domainidup:22610;domain:e-kamensk_sh;domaincod:;
    domainid:29474;domainidup:22150;domain:vladivostok;domaincod:;
    domainid:18311;domainidup:18310;domain:sankt-petersburg;domaincod:;
    domainid:21072;domainidup:18310;domain:kavkaz;domaincod:;
    domainid:28154;domainidup:28152;domain:dsk;domaincod:;
    domainid:29472;domainidup:22150;domain:vanino;domaincod:;
    domainid:21071;domainidup:18310;domain:sakhalin;domaincod:;
    domainid:21073;domainidup:18310;domain:ttknn;domaincod:;
    domainid:21074;domainidup:18310;domain:sibir;domaincod:;
    domainid:32431;domainidup:21074;domain:sibir.krasnoyarsk;domaincod:;
    domainid:22150;domainidup:18310;domain:dalny_vostok;domaincod:;
    domainid:22330;domainidup:18690;domain:Саратов;domaincod:;
    domainid:19790;domainidup:18310;domain:cttk;domaincod:;
    domainid:21373;domainidup:18310;domain:Ural;domaincod:;
    domainid:25674;domainidup:25271;domain:e-n_rtk;domaincod:;
    domainid:30232;domainidup:30231;domain:Саратовская_обл;domaincod:;
    domainid:18690;domainidup:18310;domain:volga;domaincod:;





