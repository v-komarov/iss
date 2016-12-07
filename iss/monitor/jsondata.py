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

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q


from iss.monitor.models import events,accidents
from iss.localdicts.models import Severity,Status,address_house,accident_cats,accident_list,devices_type

from iss.monitor.othersources import get_zkl
from iss.monitor.models import Profile,messages
from iss.equipment.models import devices_ip
from iss.inventory.models import devices



## Для коммутаторов
devicetype = devices_type.objects.get(pk=1)



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)




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

        if r.has_key("manager") and rg("manager") != '':
            request.session['manager'] = pickle.dumps(eval(request.GET["manager"]))

        if r.has_key("first_seen"):
            request.session['first_seen'] = request.GET["first_seen"]

        if r.has_key("last_seen"):
            request.session['last_seen'] = request.GET["last_seen"]

        if r.has_key("search") and rg("search") != '':
            if request.GET["search"] == "xxxxx":
                request.session['search'] = ""
            else:
                request.session['search'] = request.GET["search"]

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


        # Добавление в группировку (контейнер)
        if r.has_key("addgroup") and rg("addgroup") != '[]':
            container_row = request.GET["container_row"]
            id_group = eval(request.GET["addgroup"])
            g = []
            for item in id_group:
                if container_row != item:
                    g.append(item)
                    i = events.objects.get(pk=item)
                    i.agregation = True
                    #i.agregator = False
                    i.data['containergroup'] = []
                    i.save()
            e = events.objects.get(pk=container_row)
            data = e.data
            if data.has_key('containergroup'):
                for a in g:
                    data['containergroup'].append(a)
            else:
                data['containergroup'] = g
            e.agregation = False
            e.agregator = True
            e.save()



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



        # Удаление из группировки
        if r.has_key("delgroup") and rg("delgroup") != '[]':
            container_row = request.GET["container_row"]
            id_group = eval(request.GET["delgroup"])
            e = events.objects.get(pk=container_row)
            l = e.data['containergroup']
            for item in id_group:
                if item != container_row:
                    i=l.index(item)
                    del l[i]
                    a = events.objects.get(pk=item)
                    a.agregation = False
                    a.save()
                    del item

            e.data['containergroup'] = l
            e.save()


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
                for m in e.data["mails"]:
                    d = datetime.datetime.fromtimestamp(email.utils.mktime_tz(parsedate_tz(m["mail_date"])))
                    list_mail.append({
                        'id_mail':m["mail_id"].replace(">","").replace("<",""),
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
            for m in e.data["mails"]:
                if m["mail_id"] == u"<%s>" % id_mail:
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

            t = term.split(" ")
            if len(t) == 1:
                t1 = t[0]
                data = address_house.objects.filter(Q(house=None) & Q(city__name__icontains=t1) & Q(street=None))


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
                    label = item.city.name+" "+item.street.name+" "+item.house
                elif item.city != None and item.street != None:
                    label = item.city.name+" "+item.street.name
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






        ### Данные по аварии
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
                'accrepair' : acc.acc_repair
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

                address_list = address_list.replace(",;",";").replace("None","").replace(",,;",";").replace(",;",";")

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
                        'accaddresslist':address_list[1:],
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
            # Чередование полей
            pk_user = request.user.pk

            u = User.objects.get(pk=pk_user)
            if Profile.objects.filter(user=u).count() == 1:

                p = Profile.objects.get(user=u)
                data = p.settings
                if data.has_key("monitor-settings"):
                    data['monitor-settings']['head_order'] = head_order
                    p.settings = data
                    p.save()
                else:
                    data["monitor-settings"] = {
                        'head_order': head_order,
                    }
                    p.settings = data
                    p.save()
            else:

                settings = {
                    'monitor-settings':{
                        'head_order': head_order,
                        }
                    }

                Profile.objects.create(
                    user = u,
                    settings = settings
                )




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


            e = events.objects.get(pk=event_id)
            t = accident_list.objects.get(pk=acctype)
            c = accident_cats.objects.get(pk=acccat)


            ### Поиск даты начала аварии - самое ранее событие
            datetime_start = e.first_seen
            if e.data.has_key("containergroup"):
                for item in e.data["containergroup"]:
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



            accidents.objects.create(
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
                acc_repair = accrepair
            )



            e.accident = True
            e.save()






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


            acc.acc_name = accname
            acc.acc_comment = acccomment
            acc.acc_type = t
            acc.acc_cat = c
            acc.acc_reason = accreason
            acc.acc_repair = accrepair
            acc.acc_address = data
            acc.acc_stat = acc_stat

            acc.save()





        ## создание оповещения email сообщения
        if data.has_key("action") and data["action"] == 'create-mcc-message-email':
            values = eval(str(data))
            event_id = values["event_id"]
            ev = events.objects.get(pk=event_id)
            ac = accidents.objects.get(acc_event=ev)
            messages.objects.create(accident=ac,data=values)
            ev.mcc_mail_begin = True
            ev.save()

            print values



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

