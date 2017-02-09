.. contents:: Оглавление
    :depth: 2


Расчет ЗКЛ
==========

.. epigraph::

    Сейчас используется временная схема, "собранная на коленке".
    Выводится ЗКЛ в двух местах интерфейса.



Вывод ЗКЛ из Интерфейса "Оперативный журнал" -> выпадающее меню для каждого события -> "Расчет ЗКЛ"
---------------------------------------------------------------------------------------------------

 Исходный код ::

        # Запрос расчета ЗКЛ
        if r.has_key("getzkl") and rg("getzkl") != "":
            id_event = request.GET["event_id"]
            event_list = [id_event]
            a = events.objects.get(pk=id_event)
            data = a.data
            if data.has_key("containergroup"):
                for item in data["containergroup"]:
                    event_list.append(item)
            response_data = get_zkl(event_list)





#. Предварительное заполнение данными о состоянии портов из ИСС модель devices_ip поле data
#. Выборка всех ip устройств из группировки
#. Отображение состояния портов по каждому устройству и сумму на интерфейсном уровне



 Пример json данных в поле data модели devices_ip ::

    {"ports_info": {"free": 0, "tech": 24, "used": 0, "defective": 0, "reservation": 0, "unconnected": 0}, "iss_id_device": 18841, "iss_address_id": 1370}





.. figure:: _static/zkl1.png
       :scale: 30 %
       :align: center
       :alt: Расчет ЗКЛ через меню






Вывод ЗКЛ из Интерфейса "Оперативный журнал" -> выпадающее меню для каждого события -> "Оповещение об аварии на мсс"
--------------------------------------------------------------------------------------------------------------------

 Исходный код ::

        #### Данные по аварии для отправки email сообщения МСС
        if r.has_key("mailaccidentdata") and rg("mailaccidentdata") != "":
            ### id строки события (контейнера)
            row_id = request.GET["mailaccidentdata"]
            ev = events.objects.get(pk=row_id)
            acc = accidents.objects.get(acc_event=row_id)
            if request.GET["mcc_mail_begin"] == "no":
            # Почтовое сообщение еще не создавалось

                ##### Определение списка адресов ####
                #####################################
                domen = ev.source


                ipaddress = [ev.device_net_address]
                if ev.data.has_key("containergroup"):
                    for item in ev.data["containergroup"]:
                        a = events.objects.get(pk=item)
                        ipaddress.append(a.device_net_address)

                iddevices = []
                ### Поиск соответствия ip адресу id для iss
                for ip in ipaddress:
                    if devices_ip.objects.filter(ipaddress=ip,device_domen="zenoss_krsk").count() == 1:
                        d = devices_ip.objects.get(ipaddress=ip,device_domen="zenoss_krsk")
                        if d.data.has_key("iss_id_device"):
                            iddevices.append("%s" % d.data["iss_id_device"])


                houses = []
                #### Сбор id адресов
                #### Поиск устройств по ip адресам
                for ip in ipaddress:
                    if devices.objects.filter(data__ipaddress=ip,data__domen=domen,device_type=devicetype).count() == 1:
                        ### Найден коммутатор в базе инвентори
                        dev = devices.objects.get(data__ipaddress=ip,data__domen=domen,device_type=devicetype)
                        if dev.address.house not in houses:
                            houses.append(dev.address.id)





                ### Дополнение из адресов , введеннх операторов
                for addrid in acc.acc_address["address_list"]:
                    if int(addrid["addressid"],10) not in houses:
                        houses.append(int(addrid["addressid"],10))



                address_list = ""
                ### Формирование адресной строки
                q = []
                for addr in houses:
                    q.append("Q(id=%s)" % addr)

                strsql = "address_house.objects.filter(%s)" % (" | ".join(q))
                data = eval(strsql)

                cities = []
                cityname = []
                for i in data:
                    if i.city.id not in cities:
                        cities.append(i.city.id)
                        cityname.append(i.city.name)

                addr = []
                for i in data:
                    addr.append(
                        {
                            'city':i.city,
                            'street':i.street,
                            'house':i.house
                        }

                    )



                for city,street_house in itertools.groupby(addr,key=lambda x:x['city']):
                    address_list = address_list + "," + str(city) + ","
                    for street,houses in itertools.groupby(list(street_house),key=lambda y:y['street']):
                        hl = ""
                        for h in list(houses):
                            a = "%s" % h["house"]
                            hl = hl + a + ","
                        address_list = address_list + str(street) + ",%s" % hl.encode("utf-8") + ";"


                address_list = address_list.replace(",;",";").replace("None","").replace(",,;",";")[:-1]


                ### Рсчет ЗКЛ
                zkl = 0
                for ip in ipaddress:
                    for d in devices_ip.objects.filter(device_domen=domen, ipaddress=ip):
                        if d.data.has_key("ports_info"):
                            zkl = zkl + d.data["ports_info"]["used"]

                tzm = 'Europe/Moscow'

                accjson = {
                        'accid': acc.id,
                        'acc_start': acc.acc_start.astimezone(timezone(tzm)).strftime('%d.%m.%Y %H:%M'),
                        'acctype': acc.acc_type.name_short,
                        'acccat': acc.acc_cat.cat,
                        'accreason': acc.acc_reason,
                        'acccities':",".join(cityname),
                        'accaddresslist':address_list[1:-1],
                        'acczkl':zkl
                    }


            else:
            # Почтовое сообщение уже было создано
                m = messages.objects.filter(accident=acc).order_by('-datetime_message').first()


                accjson = {
                    'acc_start': m.data['acc_datetime_begin'],
                    'acccattype': m.data['acc_cat_type'],
                    'accreason': m.data['acc_reason'],
                    'acccities': m.data['acc_cities'],
                    'accaddresslist': m.data['acc_address_list'],
                    'acczkl': m.data['acc_zkl'],
                    'acc_email_templates': m.data['acc_email_templates'],
                    'acc_email_list': m.data['acc_email_list'],
                    'acc_service_stoplist': m.data['acc_service_stoplist'],
                    'acc_repair_end':m.data['acc_repair_end']
                }


            response_data = accjson

#. Предварительное заполнение данными о состоянии портов из ИСС модель devices_ip поле data
#. Выборка всех ip устройств из группировки
#. Выборка id адресов из модели address_house (город,улица,дом) всех добавленных операторов городов, улиц, домов.
#. Получение дополнительных ip адресов устройств по id адресов из модели devices.
#. Расчет ЗКЛ по суммарному списку ip адресов устройств.


.. figure:: _static/zkl2.png
       :scale: 30 %
       :align: center
       :alt: Расчет ЗКЛ при подготовке оповещения

