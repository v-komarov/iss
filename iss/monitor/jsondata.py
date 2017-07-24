#coding:utf-8

import datetime
import json
import time
import pickle
import operator
import uuid
import email
import itertools



from email.utils import parsedate_tz, mktime_tz, formatdate
from pytz import timezone

import logging

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django import template


from iss.monitor.models import events, accidents, drp_list
from iss.localdicts.models import Severity,Status,address_house,accident_cats,accident_list,address_templates,logical_interfaces_prop_list,device_status

from iss.monitor.othersources import get_zkl
from iss.monitor.models import Profile,messages
#from iss.equipment.models import devices_ip
from iss.inventory.models import devices,logical_interfaces_prop


from iss.monitor.tools import groupevents_ip



logger = logging.getLogger('monitor')




tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)

dev_use = device_status.objects.get(name="Используется")
prop = logical_interfaces_prop_list.objects.get(name='ipv4')

### Чередование полей по умолчанию
head_order = [
    {'name': 'status_id', 'title': 'Status'},
    {'name': 'severity_id', 'title': 'Severity'},
    {'name': 'manager', 'title': 'Manager'},
    {'name': 'event_class', 'title': 'EventClass'},
    {'name': 'device_system', 'title': 'DeviceSystem'},
    {'name': 'device_group', 'title': 'DeviceGroup'},
    {'name': 'device_class', 'title': 'DeviceClass'},
    {'name': 'device_net_address', 'title': 'DeviceNetAddress'},
    {'name': 'device_location', 'title': 'DeviceLocation'},
    {'name': 'element_identifier', 'title': 'ElementIdentifier'},
    {'name': 'element_sub_identifier', 'title': 'ElementSubIdentifier'},
    {'name': 'summary', 'title': 'Summary'},

]






### Формирование словаря адресов аварии
def accident_dict(acc):
    data = {}
    data["comment"] = acc.acc_address_comment

    #### Список id адресов с showitem="no"
    showitemno = []
    if acc.acc_address_devices.has_key("address_list"):
        for row in acc.acc_address_devices["address_list"]:
            if row["showitem"] == "no":
                showitemno.append(int(row["addressid"],10))


    address_list = []
    ### Для адресов, сформированных на основе ручного ввода адресов
    for item in acc.acc_address["address_list"]:
        addr = address_house.objects.get(pk=item["addressid"])
        ### Может город и улица в адресе отсутствовать . Про город - маловероятно
        city = addr.city.name if addr.city else ""
        street = addr.street.name if addr.street else ""
        house = addr.house if addr.house else ""

        address_list.append(
            {
                'address_id': addr.id,
                'city' : city,
                'street' : street,
                'house' : house
            }
        )




    ### Для адресов, вычисляемых на основе событий - ip адресов
    for ip in acc.get_event_ip_list():

        ### Поиск по ip адресу на интерфейсе manager
        if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
            p = logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').first()
            #### Определение серевого элемента
            ne = p.logical_interface.netelem

            ### Поиск связанных устройств
            for d in ne.device.all():

                ### Может город и улица в адресе отсутствовать . Про город - маловероятно
                city = d.address.city.name if d.address.city else ""
                street = d.address.street.name if d.address.street else ""
                house = d.address.house if d.address.house else ""

                ## Флаг showitem
                if d.address.id in showitemno:
                    showitem = "no"
                else:
                    showitem = "yes"

                address_list.append(
                    {
                        'address_id': d.address.id,
                        'city': city,
                        'street': street,
                        'house': house,
                        'showitem': showitem
                    }
                )

    data["address_list"] = address_list

    return data








### Формирование словаря адресов аварии (по списку id адресов)
def accident_dict2(addressid_list):

    data = {}

    address_list = []
    ### Для адресов, сформированных на основе ручного ввода адресов
    for item in addressid_list:
        address_id = int(item['addressid'],10)
        addr = address_house.objects.get(pk=address_id)

        ### Может город и улица в адресе отсутствовать . Про город - маловероятно
        if addr.city:
            city = addr.city.name
        else:
            city = ''
        if addr.street:
            street = addr.street.name
        else:
            street = ''
        if addr.house:
            house = addr.house
        else:
            house = ""
        address_list.append(
            {
                'city' : city,
                'street' : street,
                'house' : house
            }
        )

    data["address_list"] = address_list

    return data







def my_fields_order(request):
    # Чередование полей
    pk_user = request.user.pk
    u = User.objects.get(pk=pk_user)
    if Profile.objects.filter(user=u).count() == 1:
        p = Profile.objects.get(user=u)
        data = p.settings
        if data.has_key("monitor-settings"):
            return data["monitor-settings"]["head_order"]
        else:
            return head_order
    else:
        return head_order






def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        if r.has_key("status") and rg("status") != '':
            request.session['status_id'] = pickle.dumps(eval(request.GET["status"]))


        if r.has_key("severity") and rg("severity") != '':
            request.session['severity_id'] = pickle.dumps(eval(request.GET["severity"]))

        ### Сохранить список source
        if r.has_key("source") and rg("cource") != '':
            request.session['source'] = pickle.dumps(eval(request.GET["source"]))

        if r.has_key("first_seen"):
            request.session['first_seen'] = request.GET["first_seen"]

        if r.has_key("last_seen"):
            request.session['last_seen'] = request.GET["last_seen"]

        if r.has_key("search") and rg("search") != '':
            if request.GET["search"] == "xxxxx":
                request.session['search'] = ""
            else:
                request.session['search'] = request.GET["search"]

        ### Строка поиска в интерфейсе аварий
        if r.has_key("searchaccident") and rg("searchaccident") != '':
            if request.GET["searchaccident"] == "xxxxx":
                request.session['searchaccident'] = ""
            else:
                request.session['searchaccident'] = request.GET["searchaccident"]



        ### Показывать только группировки
        if r.has_key("filtergroup") and rg("filtergroup") != '':
            if request.session.has_key("filtergroup"):
                del request.session['filtergroup']
            else:
                request.session['filtergroup'] = "ok"




        if r.has_key("containergroup") and rg("containergroup") != '':
            if request.GET["containergroup"] == "_____":
                del request.session['containergroup']
            else:
                request.session['containergroup'] = request.GET["containergroup"]




        ### Показывать только только с авариями
        if r.has_key("filteraccident") and rg("filteraccident") != '':
            if request.session.has_key("filteraccident"):
                del request.session['filteraccident']
            else:
                request.session['filteraccident'] = "ok"




        ### Показывать только только закрытые (c finished_date=True)
        if r.has_key("filterhistory") and rg("filterhistory") != '':
            if request.session.has_key("filterhistory"):
                del request.session['filterhistory']
            else:
                request.session['filterhistory'] = "ok"




        ### данные по списку событий в контейнере
        if r.has_key("getmembers") and rg("getmembers") != '':
            container_row = request.GET["container_row"]
            tz = request.session['tz']
            e = events.objects.get(pk=container_row)
            a = []

            h = my_fields_order(request)

            if e.data.has_key("containergroup"):
                l = e.data['containergroup']

                for item in l:
                    i = events.objects.get(pk=item)
                    if i.byhand == True:
                        byhand = "yes"
                    else:
                        byhand = "no"
                    if i.agregator == True:
                        agregator = "yes"
                    else:
                        agregator = "no"
                    if i.bymail == True:
                        bymail = "yes"
                    else:
                        bymail = "no"

                    field = []

                    for j in range(0,len(h)):
                        if h[j]['name'] == "status_id":
                            field.append(i.status_id.name)
                        elif h[j]['name'] == "severity_id":
                            field.append(i.severity_id.name)
                        else:
                            field.append(eval("i.%s" % h[j]['name']))

                    a.append(
                        {
                            'id':i.id,
                            'dateorder':time.mktime(i.last_seen.timetuple()),
                            'uuid':i.uuid,
                            'first_seen':i.first_seen.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M %Z"),
                            'last_seen':i.last_seen.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M %Z"),
                            'field0':field[0],
                            'field1':field[1],
                            'field2':field[2],
                            'field3':field[3],
                            'field4':field[4],
                            'field5':field[5],
                            'field6':field[6],
                            'field7':field[7],
                            'field8':field[8],
                            'field9':field[9],
                            'field10':field[10],
                            'field11':field[11],
                            'byhand':byhand,
                            'agregator':agregator,
                            'bymail':bymail
                        }
                    )

                a = sorted(a, key=operator.itemgetter('dateorder'),reverse=True)
            response_data['members'] = a





        # Данные по событию для отображения в форме
        if r.has_key("getevent") and rg("getevent") != '':
            tz = request.session['tz']
            id_event = request.GET["getevent"]
            e = events.objects.get(pk=id_event)
            data = {
                'id':e.id,
                'event_class':e.event_class,
                'severity':e.severity_id.id,
                'device_system':e.device_system,
                'device_group':e.device_group,
                'device_class':e.device_class,
                'device_net_address':e.device_net_address,
                'device_location':e.device_location,
                'element_identifier':e.element_identifier,
                'element_sub_identifier':e.element_sub_identifier,
                'status':e.status_id.id
            }

            list_mail = []

            # Если событие на основе почтового сообщения, то отправляем список почтовых сообщений
            if e.bymail == True:

                for m in eval(str(e.data))['mails']:
                    d = datetime.datetime.fromtimestamp(email.utils.mktime_tz(parsedate_tz(m["mail_date"])))
                    list_mail.append({
                        'id_mail':m["mail_id"],
                        'label_mail':m["mail_from"].replace(">","").replace("<","")+" ("+d.replace(tzinfo=timezone("UTC")).astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M:%S")+")"
                    })

                data["list_mail"] = list_mail

            response_data = data



        ## Содержание письма
        if r.has_key("getmail") and rg("getmail") != '':

            data = {}
            id_event = request.GET["event_id"]
            id_mail = request.GET["mail_id"]
            e = events.objects.get(pk=id_event)
            for m in eval(str(e.data))['mails']:

                if m["mail_id"] == id_mail:
                    files = []
                    for a in m["attachment"]:
                        files.append(a["file_name"])
                    data = {
                        'subject':m["subject"],
                        'body':m["mail_body"],
                        'files':files
                    }

            response_data = data


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




        #### Поиск по адресу
        if r.has_key("term") and rg("term") != "":
            term = request.GET["term"]
            obj = []

            t = term.split(",")
            if len(t) == 1:
                t1 = t[0]
                data = address_house.objects.filter(Q(house=None) & Q(city__name__icontains=t1) & Q(street=None))
                #data = address_house.objects.filter(Q(house=None) & Q(street=None))

            elif len(t) == 2:
                t1 = t[0]
                t2 = t[1]
                t3 = None
                data = address_house.objects.filter(Q(house=None) & Q(city__name__icontains=t1) & Q(street__name__icontains=t2))

            elif len(t) == 3:
                t1 = t[0]
                t2 = t[1]
                t3 = t[2]
                data = address_house.objects.filter(Q(house__icontains=t3) & Q(city__name__icontains=t1) & Q(street__name__icontains=t2))

            else:
                data = address_house.objects.filter(Q(house__icontains=term) | Q(city__name__icontains=term) | Q(street__name__icontains=term))



            for item in data:

                if item.city != None and item.street != None and item.house != None:
                    label = item.city.name+","+item.street.name+","+item.house
                elif item.city != None and item.street != None:
                    label = item.city.name+","+item.street.name
                elif item.city != None:
                    label = item.city.name
                else:
                    label = ""

                obj.append(
                    {
                        "label": label,
                        "value": item.id
                    }
                )



            response_data = obj






        #### Получение адресов на основании группировки события ip адресов для первоначального отображения в интерфейсе создания аварии
        if r.has_key("getaccidentipaddress") and rg("getaccidentipaddress") != "":
            ### id строки события (контейнера)
            row_id = request.GET["getaccidentipaddress"]
            evt = events.objects.get(pk=row_id)

            #### Список ip адресов
            list_ip = groupevents_ip(evt.id)
            #### Список id устройств
            dev_list = []
            #### Контроль уникальности id адресов
            address_list = []


            #### Поиск устройств на основании ip адресов
            addressjson = []
            for ip in list_ip:
                ### Поиск по ip адресу на интерфейсе manager
                if logical_interfaces_prop.objects.filter(prop=prop, val=ip,logical_interface__name='manage').exists():
                    p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                    ### Получение id устройств
                    dev_list.extend(p.logical_interface.get_dev_list())

            ### Обход id устройств
            for devid in dev_list:
                d = devices.objects.get(pk=devid)
                if not d.address.id in address_list:
                    ### Если такого адреса нет - то добавляем
                    address_list.append(d.address.id)
                    addressjson.append(
                        {
                            'addressid':d.address.id,
                            'addresslabel':d.getaddress(),
                            'show':True
                        }
                    )

            response_data = {
                'address_list':addressjson
            }







        ### Данные по аварии для формы аварии интерфейса оперативный журнал
        if r.has_key("getaccidentdata") and rg("getaccidentdata") != "":
            ### id строки события (контейнера)
            row_id = request.GET["getaccidentdata"]
            acc = accidents.objects.get(acc_event=row_id)
            if acc.acc_end != None:
                accend = "yes"
            else:
                accend = "no"

            if acc.acc_stat == True:
                accstat = "yes"
            else:
                accstat = "no"


            accjson = {
                'accid' : acc.id,
                'address' : acc.acc_address,
                'acctype' : acc.acc_type.id,
                'acccat' : acc.acc_cat.id,
                'accname' : acc.acc_name,
                'acccomment' : acc.acc_comment,
                'accend' : accend,
                'accstat' : accstat,
                'accreason' : acc.acc_reason,
                'accrepair' : acc.acc_repair,
                'accdevaddress' : acc.acc_address_devices,
                'accaddrcomment' : acc.acc_address_comment
            }


            ### Номер в ИСС
            if acc.acc_iss_id != None:
                accjson['accissid'] = acc.acc_iss_id
            else:
                accjson['accissid'] = 0


            response_data = accjson





        ### Данные по аварии для формы аварии интерфейса аварий
        if r.has_key("getaccidentdata2") and rg("getaccidentdata2") != "":
            tz = request.session['tz']
            ### id строки аварии
            row_id = request.GET["getaccidentdata2"]
            acc = accidents.objects.get(pk=row_id)
            if acc.acc_end != None:
                accend = "yes"
            else:
                accend = "no"

            if acc.acc_stat == True:
                accstat = "yes"
            else:
                accstat = "no"

            if acc.acc_end != None:
                accenddate = acc.acc_end.astimezone(timezone(tz)).strftime("%d.%m.%Y")
                accendtime = acc.acc_end.astimezone(timezone(tz)).strftime("%H:%M")
            else:
                accenddate = ''
                accendtime = ''


            accjson = {
                'accid' : acc.id,
                'address' : acc.acc_address,
                'acctype' : acc.acc_type.id,
                'acccat' : acc.acc_cat.id,
                'accname' : acc.acc_name,
                'acccomment' : acc.acc_comment,
                'accend' : accend,
                'accstat' : accstat,
                'accreason' : acc.acc_reason,
                'accrepair' : acc.acc_repair,
                'accstartdate' : acc.acc_start.astimezone(timezone(tz)).strftime("%d.%m.%Y"),
                'accstarttime' : acc.acc_start.astimezone(timezone(tz)).strftime("%H:%M"),
                'accenddate': accenddate,
                'accendtime': accendtime,
                'accdevaddress': acc.acc_address_devices,
                'accaddrcomment': acc.acc_address_comment
            }

            ### Номер в ИСС
            if acc.acc_iss_id != None:
                accjson['accissid'] = acc.acc_iss_id
            else:
                accjson['accissid'] = 0


            response_data = accjson






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
                    for street,house in itertools.groupby(list(street_house),key=lambda y:y['street']):
                        hl = ""

                        for h in list(house):
                            a = "%s" % h["house"]
                            hl = hl + a + ","
                        address_list = address_list + str(street) + ",%s" % hl.encode("utf-8") + ";"

                address_list = address_list.replace(",;",";").replace("None","").replace(",,;",";").replace(",;",";").replace(";,",";")

                ### Рсчет ЗКЛ на основе списка id адресов
                zkl = 0

                for ad in houses:
                    a = address_house.objects.get(pk=ad)
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








        #### Данные по устранении аварии для отправки email сообщения МСС
        if r.has_key("mailaccidentdataend") and rg("mailaccidentdataend") != "":
            ### id строки события (контейнера)
            row_id = request.GET["mailaccidentdataend"]
            ev = events.objects.get(pk=row_id)
            acc = accidents.objects.get(acc_event=row_id)

            tzm = 'Europe/Moscow'

            m = messages.objects.filter(accident=acc, data__acc_email_templates="2").order_by('-datetime_message')
            # Сообщение о завершении еще не отправлялось - ,берем даннные из сообщения о начале
            if m.count() == 0:
                me = messages.objects.filter(accident=acc, data__acc_email_templates="1").order_by('-datetime_message').first()

                accjson = {
                    'acc_start': me.data['acc_datetime_begin'],
                    'acccattype': me.data['acc_cat_type'],
                    'accreason': acc.acc_reason,
                    'acccities': me.data['acc_cities'],
                    'accaddresslist': me.data['acc_address_list'],
                    'acc_email_templates': me.data['acc_email_templates'],
                    'acc_email_list': me.data['acc_email_list'],
                    'acc_service_stoplist': me.data['acc_service_stoplist'],
                    'acc_repair_end':acc.acc_end.astimezone(timezone(tzm)).strftime('%d.%m.%Y %H:%M'),
                    'acc_repair':acc.acc_repair
                }


            ### Сообщение об устранении уже отправлялось - берем данные от последнего
            else:
                me = m.first()

                accjson = {
                    'acc_start': me.data['acc_datetime_begin'],
                    'acccattype': me.data['acc_cat_type'],
                    'accreason': me.data['acc_reason'],
                    'acccities': me.data['acc_cities'],
                    'accaddresslist': me.data['acc_address_list'],
                    'acc_email_templates': me.data['acc_email_templates'],
                    'acc_email_list': me.data['acc_email_list'],
                    'acc_service_stoplist': me.data['acc_service_stoplist'],
                    'acc_repair_end':me.data['acc_repair_end'],
                    'acc_repair': me.data['acc_repair_acctions']
                }


            response_data = accjson








        ### Определение зарегистрирована авария в ИСС или нет
        if r.has_key("issaccidentok") and rg("issaccidentok") != "":
            ### id строки события (контейнера)
            row_id = request.GET["issaccidentok"]
            ev = events.objects.get(pk=row_id)
            acc = accidents.objects.get(acc_event=row_id)
            if acc.acc_iss_id:
                response_data = {'iss':'yes'}
            else:
                response_data = {'iss':'no'}




        ### Данные по колоночным фильтрам
        if r.has_key("getfiltercolumns") and rg("getfiltercolumns") != "":
            pk_user = request.user.pk

            u = User.objects.get(pk=pk_user)
            if Profile.objects.filter(user=u).count() == 1:

                p = Profile.objects.get(user=u)
                data = p.settings
                if data.has_key("monitor-settings"):
                    if data["monitor-settings"].has_key("columns-filter"):
                        response_data = data["monitor-settings"]["columns-filter"]
                    else:
                        response_data = {
                            'f1': '',
                            'f2': '',
                            'f3': '',
                            'f4': '',
                            'f5': '',
                            'f6': '',
                            'f7': '',
                            'f8': '',
                            'f9': '',
                            'f10': '',
                            'f11': '',
                            'f12': '',
                            'f13': '',
                            'f14': ''
                        }

                else:
                    response_data = {
                        'f1': '',
                        'f2': '',
                        'f3': '',
                        'f4': '',
                        'f5': '',
                        'f6': '',
                        'f7': '',
                        'f8': '',
                        'f9': '',
                        'f10': '',
                        'f11': '',
                        'f12': '',
                        'f13': '',
                        'f14': ''
                    }
            else:

                response_data = {
                    'f1':'',
                    'f2': '',
                    'f3': '',
                    'f4': '',
                    'f5': '',
                    'f6': '',
                    'f7': '',
                    'f8': '',
                    'f9': '',
                    'f10': '',
                    'f11': '',
                    'f12': '',
                    'f13': '',
                    'f14': ''
                }




        ### Данные для интерфеса списка ДРП интерфейса списка аварий
        if r.has_key("getdrplist") and rg("getdrplist") != "":
            tz = request.session['tz']
            accident_id = int(request.GET["getdrplist"],10)
            mess_list = []
            file_list = []
            acc = accidents.objects.get(pk=accident_id)
            for drp in acc.drp_list_set.all():
                if drp.num_drp == 0:
                    file_list.append({
                        'datetime_order':int((time.mktime(drp.datetime_drp.astimezone(timezone('UTC')).timetuple()))*10000),
                        'id':drp.id,
                        'datetime': drp.datetime_drp.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M"),
                        'filename':drp.data_files["filename"],
                        'author':drp.author
                    })
                else:
                    mess_list.append({
                        'num_drp': drp.num_drp,
                        'id':drp.id,
                        'message':drp.message_drp,
                        'datetime': drp.datetime_drp.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M"),
                        'author': drp.author
                    })

            if len(mess_list) != 0:
                mess_list = sorted(mess_list, key=operator.itemgetter('num_drp'),reverse=True)
            if len(file_list) != 0:
                file_list = sorted(file_list, key=operator.itemgetter('datetime_order'),reverse=True)

            #logger.info(request.user.get_username()+"\t"+"")

            response_data["accident_name"] = acc.acc_name
            response_data["file_list"] = file_list
            response_data["mess_list"] = mess_list



        ### Установка id адреса устройств для интерфейса ЗКЛ
        if r.has_key("action") and r["action"] == "set_zkl_address" and r.has_key("address_id") and r["address_id"] != "":
            address_id = int(request.GET["address_id"], 10)
            addr = address_house.objects.get(pk=address_id)
            dev_list = []
            ### Когда определен только город
            if addr.city and addr.street == None and addr.house == None:
                for dev in devices.objects.filter(address__city = addr.city,status=dev_use):
                    if dev.id not in dev_list:
                        dev_list.append(dev.id)

            ### Когда определен город и улица
            elif addr.city and addr.street and addr.house == None:
                for dev in devices.objects.filter(address__city = addr.city,address__street = addr.street,status=dev_use):
                    if dev.id not in dev_list:
                        dev_list.append(dev.id)


            ### Когда определены город, улица, дом
            elif addr.city and addr.street and addr.house:
                for dev in devices.objects.filter(address__city=addr.city, address__street=addr.street, address__house=addr.house,status=dev_use):
                    if dev.id not in dev_list:
                        dev_list.append(dev.id)



            if request.session.has_key("device_zkl_list"):
                devs = pickle.loads(request.session["device_zkl_list"])
                for i in dev_list:
                    if i not in devs:
                        devs.append(i)
                request.session["device_zkl_list"] = pickle.dumps(devs)
            else:
                request.session["device_zkl_list"] = pickle.dumps(dev_list)

            response_data = {"result":"OK"}





        ### Установка ip адреса устройств для интерфейса ЗКЛ через определение и добавление id адресов устройств
        if r.has_key("action") and r["action"] == "set_zkl_ip" and r.has_key("ip") and r["ip"] != "":
            ip = request.GET["ip"]
            dev_list = []
            ### Поиск оборудования с управлением по этому ip
            if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                #### Определение серевого элемента
                ne = p.logical_interface.netelem
                dev_list = []
                ### Поиск связанного устройства
                for dev in ne.device.filter(status=dev_use):
                    dev_list.append(dev.id)

                if request.session.has_key("device_zkl_list"):
                    devs = pickle.loads(request.session["device_zkl_list"])
                    for i in dev_list:
                        if i not in devs:
                            devs.append(i)
                    request.session["device_zkl_list"] = pickle.dumps(devs)
                else:
                    request.session["device_zkl_list"] = pickle.dumps(dev_list)

            response_data = {"result":"OK"}




        ### Список устройств для интерфейса ЗКЛ
        if r.has_key("action") and r["action"] == "get_zkl_devices":
            q_str = []
            for q in pickle.loads(request.session["device_zkl_list"]):
                q_str.append("Q(id=%s)" % q)

            result = []
            str_sql = "devices.objects.filter(%s).order_by('address__street__name','address__house')" % " | ".join(q_str)
            for d in eval(str_sql):
                ne = []
                for n in d.get_netelems():
                    ne.append(n["name"])
                result.append({
                    "device_address": d.getaddress(),
                    "device_model": d.device_scheme.name,
                    "device_serial": d.serial,
                    "device_netelems": " ".join(ne),
                    "device_ip": " ".join(d.get_manage_ip()),
                    "device_ports": d.get_ports_count(),
                    "device_use_ports": d.get_use_ports(),
                    "device_tech_ports": d.get_tech_ports(),
                    "device_reserv_ports": d.get_reserv_ports(),
                    "device_use_combo": d.get_use_combo(),
                    "device_tech_combo": d.get_tech_combo(),
                    "device_reserv_combo": d.get_reserv_combo(),
                    "device_combo": d.get_combo_count()

                })



            #print result

            response_data = result






        #### Очистить список устройств интерфейса ЗКЛ
        if r.has_key("action") and r["action"] == "clear_zkl_devices":
            request.session["device_zkl_list"] = pickle.dumps([])







    if request.method == "POST":
        data = eval(request.body)



        if data.has_key("action") and data["action"] == 'create_event':

            now = datetime.datetime.now(timezone('UTC'))
            source = request.user.username

            events.objects.create(
                source = source,
                datetime_evt = now,
                first_seen = now,
                update_time = now,
                last_seen = now,
                event_class = data["event_class"],
                severity_id = Severity.objects.get(pk=data["severity"]),
                manager = 'operator',
                device_system = data["device_system"],
                device_group = data["device_group"],
                device_class = data["device_class"],
                device_net_address = data["device_net_address"],
                device_location = data["device_location"],
                element_identifier = data["element_identifier"],
                element_sub_identifier = data["element_sub_identifier"],
                status_id = Status.objects.get(pk=data["status"]),
                byhand = True

            )

        if data.has_key("action") and data["action"] == 'edit_event':
            now = datetime.datetime.now(timezone('UTC'))
            #source = request.user.username

            e = events.objects.get(pk=data['event_id'])
            e.update_time = now
            e.last_seen = now
            e.event_class = data["event_class"]
            e.severity_id = Severity.objects.get(pk=data["severity"])
            e.device_system = data["device_system"]
            e.device_group = data["device_group"]
            e.device_class = data["device_class"]
            e.device_net_address = data["device_net_address"]
            e.device_location = data["device_location"]
            e.element_identifier = data["element_identifier"]
            e.element_sub_identifier = data["element_sub_identifier"]
            e.status_id=Status.objects.get(pk=data["status"])
            e.save()



        if data.has_key("action") and data["action"] == 'save-settings':

            head_order = eval(str(data["head_order"]))
            row_page_data = eval(str(data["row_page_data"]))
            refresh_data = eval(str(data["refresh_data"]))

            # Чередование полей
            pk_user = request.user.pk

            u = User.objects.get(pk=pk_user)
            if Profile.objects.filter(user=u).count() == 1:

                p = Profile.objects.get(user=u)
                data = p.settings
                if data.has_key("monitor-settings"):
                    data['monitor-settings']['head_order'] = head_order
                    data['monitor-settings']['row_page_data'] = row_page_data
                    data['monitor-settings']['refresh_data'] = refresh_data
                    p.settings = data
                    p.save()
                else:
                    data["monitor-settings"] = {
                        'head_order': head_order,
                        'row_page_data': row_page_data,
                        'refresh_data': refresh_data
                    }
                    p.settings = data
                    p.save()
            else:

                #print row_page_data,type(row_page_data)
                #print refresh_data,type(refresh_data)

                settings = {
                    'monitor-settings':{
                        'head_order': head_order,
                        'row_page_data': row_page_data,
                        'refresh_data': refresh_data
                        }
                    }

                Profile.objects.create(
                    user = u,
                    settings = settings
                )




        ### Создание аварии - интерфейс оперативного журнала
        if data.has_key("action") and data["action"] == 'create-accident':

            accident_data = eval(str(data))
            data = {}
            data["address_list"] = accident_data["address_list"]
            event_id = accident_data["event_id"]
            acctype = int(accident_data["acctype"],10)
            acccat = int(accident_data["acccat"],10)
            accname = accident_data["accname"]
            acccomment = accident_data["acccomment"]
            accend = accident_data["accend"]
            accstat = accident_data["accstat"]
            accreason = accident_data["accreason"]
            accrepair = accident_data["accrepair"]
            data2 = {}
            data2["address_list"] = accident_data["device_address"]
            accaddrcomment = accident_data["addrcomment"]

            e = events.objects.get(pk=event_id)
            t = accident_list.objects.get(pk=acctype)
            c = accident_cats.objects.get(pk=acccat)


            ### Формирование списка id событий
            events_list = [e.id]


            ### Поиск даты начала аварии - самое ранее событие
            datetime_start = e.first_seen
            if e.data.has_key("containergroup"):
                for item in e.data["containergroup"]:

                    #### Добавление id события в список
                    events_list.append(item)

                    a = events.objects.get(pk=item)
                    if datetime_start > a.first_seen:
                        datetime_start = a.first_seen


            if accend == "yes":
                acc_end = krsk_tz.localize(datetime.datetime.now())
                e.accident_end = True
                e.save()
            else:
                acc_end = None
                e.accident_end = False
                e.save()

            if accstat == "yes":
                acc_stat = True
            else:
                acc_stat = False



            a = accidents.objects.create(
                acc_name = accname,
                acc_comment = acccomment,
                acc_cat = c,
                acc_type = t,
                acc_event = e,
                acc_address = data,
                acc_start = datetime_start,
                acc_end = acc_end,
                acc_stat = acc_stat,
                acc_reason = accreason,
                acc_repair = accrepair,
                acc_address_devices = data2,
                acc_address_comment = accaddrcomment,
                acc_events_list = {'events_list':events_list},
                author = request.user.get_username()+ " ("+request.user.get_full_name()+")"

            )



            e.accident = True
            e.save()

            ### Формирование словаря адресов
            a.acc_addr_dict = {'address_list' : accident_dict(a)}
            a.save()

            logger.info("{user}    создал аварию id:{acc_id} name:{name}".format(user=request.user.get_username(),acc_id=a.id,name=a.acc_name))






        ### Редактирование аварии интерфейс оперативного журнала
        if data.has_key("action") and data["action"] == 'edit-accident':
            accident_data = eval(str(data))
            data = {}
            data["address_list"] = accident_data["address_list"]
            event_id = accident_data["event_id"]
            acctype = int(accident_data["acctype"], 10)
            acccat = int(accident_data["acccat"], 10)
            accname = accident_data["accname"]
            acccomment = accident_data["acccomment"]
            accend = accident_data["accend"]
            accstat = accident_data["accstat"]
            accreason = accident_data["accreason"]
            accrepair = accident_data["accrepair"]
            data2 = {}
            data2["address_list"] = accident_data["device_address"]
            accaddrcomment = accident_data["addrcomment"]


            e = events.objects.get(pk=event_id)
            t = accident_list.objects.get(pk=acctype)
            c = accident_cats.objects.get(pk=acccat)

            acc = accidents.objects.get(acc_event=e)

            ### Текущее состояние - завершена или нет
            if acc.acc_end == None and accend == "yes":
                acc.acc_end = krsk_tz.localize(datetime.datetime.now())
                e.accident_end = True
                e.save()

            elif acc.acc_end != None and accend == "no":
                acc.acc_end = None
                e.accident_end = False
                e.save()

            if accstat == "yes":
                acc_stat = True
            else:
                acc_stat = False

            ### Формирование списка id событий
            events_list = [e.id]
            if e.data.has_key("containergroup"):
                for item in e.data["containergroup"]:
                    #### Добавление id события в список
                    events_list.append(item)


            acc.acc_name = accname
            acc.acc_comment = acccomment
            acc.acc_type = t
            acc.acc_cat = c
            acc.acc_reason = accreason
            acc.acc_repair = accrepair
            acc.acc_address = data
            acc.acc_stat = acc_stat
            acc.acc_address_devices = data2
            acc.acc_address_comment = accaddrcomment

            acc.acc_addr_dict = {'address_list' : accident_dict(acc)}

            acc.acc_events_list = {'events_list':events_list}

            acc.save()

            logger.info("{user}    отредактировал аварию id:{acc_id} name:{name}".format(user=request.user.get_username(), acc_id=acc.id,name=acc.acc_name))


        ## создание оповещения email сообщения о начале аварии
        if data.has_key("action") and data["action"] == 'create-mcc-message-email':
            values = eval(str(data))
            event_id = values["event_id"]
            ev = events.objects.get(pk=event_id)
            ac = accidents.objects.get(acc_event=ev)
            messages.objects.create(accident=ac,data=values,author=request.user.get_username()+ " ("+request.user.get_full_name()+")")
            ev.mcc_mail_begin = True
            ev.save()

            #print values



        ## создание оповещения email сообщения о завершении аварии
        if data.has_key("action") and data["action"] == 'create-mcc-message-email-end':
            values = eval(str(data))
            event_id = values["event_id"]
            ev = events.objects.get(pk=event_id)
            ac = accidents.objects.get(acc_event=ev)
            messages.objects.create(accident=ac,data=values,author=request.user.get_username()+ " ("+request.user.get_full_name()+")")




        ## сохранение значений колоночных фильтров
        if data.has_key("action") and data["action"] == 'save-filter-columns':
            values = eval(str(data))

            pk_user = request.user.pk

            u = User.objects.get(pk=pk_user)
            if Profile.objects.filter(user=u).count() == 1:

                p = Profile.objects.get(user=u)
                data = p.settings
                if data.has_key("monitor-settings"):
                    data['monitor-settings']['columns-filter'] = values
                    p.settings = data
                    p.save()
                else:
                    data["monitor-settings"] = {
                        'columns-filter': values
                    }
                    p.settings = data
                    p.save()
            else:

                settings = {
                    'monitor-settings':{
                        'columns-filter': values
                        }
                    }

                Profile.objects.create(
                    user = u,
                    settings = settings
                )



        ### Редактирование аварии интерфейс журнала аварий
        if data.has_key("action") and data["action"] == 'edit-accident2':
            tzuser = request.session['tz']
            accident_data = eval(str(data))
            data = {}
            data["address_list"] = accident_data["address_list"]
            acc_id = accident_data["acc_id"]
            acctype = int(accident_data["acctype"], 10)
            acccat = int(accident_data["acccat"], 10)
            accname = accident_data["accname"]
            acccomment = accident_data["acccomment"]
            accend = accident_data["accend"]
            accstat = accident_data["accstat"]
            accreason = accident_data["accreason"]
            accrepair = accident_data["accrepair"]
            accstartdate = accident_data["accstartdate"]
            accstarttime = accident_data["accstarttime"]
            accenddate = accident_data["accenddate"]
            accendtime = accident_data["accendtime"]
            data2 = {}
            data2["address_list"] = accident_data["device_address"]
            accaddrcomment = accident_data["addrcomment"]

            t = accident_list.objects.get(pk=acctype)
            c = accident_cats.objects.get(pk=acccat)

            acc = accidents.objects.get(pk=acc_id)

            e = events.objects.get(pk=acc.acc_event.id)

            ### Формирование списка id событий
            events_list = [e.id]
            if e.data.has_key("containergroup"):
                for item in e.data["containergroup"]:
                    #### Добавление id события в список
                    events_list.append(item)


            ### Текущее состояние - завершена или нет
            if acc.acc_end == None and accend == "yes":
                acc.acc_end = timezone(tzuser).localize(datetime.datetime.strptime(accenddate+" "+accendtime, "%d.%m.%Y %H:%M"))
                e.accident_end = True
                e.save()

            elif acc.acc_end != None and accend == "no":
                acc.acc_end = None
                e.accident_end = False
                e.save()

            if accstat == "yes":
                acc_stat = True
            else:
                acc_stat = False

            #print accstartdate+" "+accstarttime
            #print datetime.datetime.strptime(accstartdate+" "+accstarttime, "%d.%m.%Y %H:%M")
            #print timezone(tzuser).localize(datetime.datetime.strptime(accstartdate+" "+accstarttime, "%d.%m.%Y %H:%M"))
            #print timezone(tzuser)

            acc.acc_start = timezone(tzuser).localize(datetime.datetime.strptime(accstartdate+" "+accstarttime, "%d.%m.%Y %H:%M"))
            acc.acc_name = accname
            acc.acc_comment = acccomment
            acc.acc_type = t
            acc.acc_cat = c
            acc.acc_reason = accreason
            acc.acc_repair = accrepair
            acc.acc_address = data
            acc.acc_stat = acc_stat
            acc.acc_address_devices = data2
            acc.acc_address_comment = accaddrcomment

            acc.acc_addr_dict = {'address_list' : accident_dict(acc)}

            acc.acc_events_list = {'events_list':events_list}

            acc.save()

            logger.info("{user}    отредактировал аварию id:{acc_id} name:{name}".format(user=request.user.get_username(),acc_id=acc.id, name=acc.acc_name))




        ### Формирование адресной строки для загрузки в наименование
        if data.has_key("action") and data["action"] == 'writeaddressdata':
            accident_data = eval(str(data))
            data = {}
            data["address_list"] = accident_data["address_list"]

            ### Формирование через шаблонизатор
            address_str = ""
            if address_templates.objects.filter(name="accidentname").count() == 1:
                templ = address_templates.objects.get(name="accidentname").template
                t = template.Template(templ)
                c = template.Context({'data': accident_dict2(data["address_list"])})
                address_str = t.render(c)

            response_data = {'address':address_str}




        ### Добавление отмеченных событий (строк) в группировку (контейнер)
        if data.has_key("action") and data["action"] == 'addgroup':
            group_data = eval(str(data))
            container = group_data["container_row"]
            group_row = group_data["addgroup"]

            g = []
            for item in group_row:
                if container != item:
                    g.append(item)
                    i = events.objects.get(pk=item)
                    i.agregation = True
                    i.agregator = False
                    i.data['containergroup'] = []
                    i.save()

            e = events.objects.get(pk=container)
            data = e.data
            if data.has_key('containergroup'):
                for a in g:
                    data['containergroup'].append(a)
            else:
                data['containergroup'] = g
            e.agregation = False
            e.agregator = True
            e.save()


            response_data = {'result': "ok"}

            logger.info("{user}    добавил в группировку id={id} {cont} события".format(user=request.user.get_username(),id=e.id,cont=e.device_location))






        # Удаление из группировки
        if data.has_key("action") and data["action"] == 'delgroup':
            group_data = eval(str(data))
            container = group_data["container_row"]
            group_row = group_data["delgroup"]

            e = events.objects.get(pk=container)
            l = e.data['containergroup']
            for item in group_row:
                if item != container:
                    i=l.index(item)
                    del l[i]
                    a = events.objects.get(pk=item)
                    a.agregation = False
                    a.save()
                    del item

            e.data['containergroup'] = l
            e.save()

            response_data = {'result': "ok"}

            logger.info("{user}    удалил из группировки id={id} {cont} события".format(user=request.user.get_username(), id=e.id,cont=e.device_location))



        ### Добавление нового ДРП
        if data.has_key("action") and data["action"] == 'adding-drp':
            data = eval(str(data))
            acc = accidents.objects.get(pk=int(data["accident"], 10))
            drp_text = data["drp_text"]

            if drp_list.objects.filter(accident=acc).exists():
                num_drp = drp_list.objects.filter(accident=acc).order_by('datetime_drp').last().num_drp + 1
            else:
                num_drp = 1

            drp_list.objects.create(
                message_drp= drp_text,
                accident= acc,
                num_drp = num_drp,
                author = request.user.get_username()+ " ("+request.user.get_full_name()+")"
            )

            response_data = {'result': 'ok'}




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

