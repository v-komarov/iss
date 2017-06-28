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

    prop = logical_interfaces_prop_list.objects.get(name='ipv4')


    def get_zkl(rowid_list):

        result = []

        for rowid in rowid_list:
            r = events.objects.get(pk=rowid)

            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=r.device_net_address, logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.get(prop=prop, val=r.device_net_address)
                ### Добавление строк с зкл
                result.extend(p.logical_interface.get_zkl(r.device_net_address))

        return result

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



#. Предварительное заполнение данными о состоянии портов и combo модели **devices_ports** **devices_combo**
#. Выборка всех ip устройств из группировки
#. Отображение состояния портов по каждому устройству и сумму на интерфейсном уровне




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

                ### IP Адреса устройств
                ipaddress = groupevents_ip(ev.id)

                iddevices = []
                #### Поиск устройств на основании ip адресов
                for ip in ipaddress:
                    ### Поиск по ip адресу на интерфейсе manager
                    if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                        p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                        ### Получение id устройств
                        iddevices.extend(p.logical_interface.get_dev_list())

                houses = []
                #### Сбор id адресов
                for d in iddevices:
                    dev = devices.objects.get(pk=d)
                    if dev.address.id not in houses:
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

                address_list = address_list.replace(",;",";").replace("None","").replace(",,;",";").replace(",;",";").replace(";,",";")

                ### Рсчет ЗКЛ на основе списка id адресов
                zkl = 0
                for addr in houses:
                    a = address_house.objects.get(pk=addr)
                    zkl = zkl + a.get_zkl()


                tzm = 'Europe/Moscow'

                accjson = {
                        'accid': acc.id,
                        'acc_start': acc.acc_start.astimezone(timezone(tzm)).strftime('%d.%m.%Y %H:%M'),
                        'acctype': acc.acc_type.name_short,
                        'acccat': acc.acc_cat.cat,
                        'accreason': acc.acc_reason,
                        'acccities':",".join(cityname),
                        'accaddresslist':address_list[1:],
                        'acczkl':zkl
                    }


            else:
            # Почтовое сообщение уже было создано
                m = messages.objects.filter(accident=acc,data__acc_email_templates="1").order_by('-datetime_message').first()


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


#. Предварительное заполнение данными о состоянии портов и комбо портов моделей **devices_ports**  **devices_combo**
#. Выборка всех ip устройств из группировки
#. Выборка id адресов из модели address_house (город,улица,дом) всех добавленных операторов городов, улиц, домов.
#. Получение дополнительных ip адресов устройств по id адресов из модели devices.
#. Расчет ЗКЛ по суммарному списку ip адресов устройств.


.. figure:: _static/zkl2.png
       :scale: 30 %
       :align: center
       :alt: Расчет ЗКЛ при подготовке оповещения

