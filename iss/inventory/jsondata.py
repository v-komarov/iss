#coding:utf-8

import datetime
import json
import logging
import operator

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect

from iss.inventory.models import devices_scheme,devices,devices_ports,devices_slots,devices_combo,devices_properties,devices_statuses,devices_removal,netelems,logical_interfaces,logical_interfaces_prop
from iss.localdicts.models import ports,slots,interfaces,address_companies,address_house,port_status,slot_status,device_status,logical_interfaces_prop_list
from django.shortcuts import redirect
from django.core import serializers
from django import template
from django.db.models import F,Func,Value
from django.db import models
from django.db.models import Q



logger = logging.getLogger('inventory')



ports_list2 = []
slots_list2 = []
interfaces_list2 = []


for item in ports.objects.all():
    ports_list2.append(item.name)

for item in slots.objects.all():
    slots_list2.append(item.name)


for item in interfaces.objects.all():
    interfaces_list2.append(item.name)




# Преобразование даты в строку + таймзона
def DateTimeString(vardatetime,request):
    tz = request.session["tz"]
    t = template.Template("""
        {% load tz %}
        {% timezone tz %}
        {{ vardatetime|date:"d.m.Y H:i e" }}
        {% endtimezone %}
    """)
    c = template.Context({'vardatetime': vardatetime, 'tz':tz})
    return t.render(c)



# Порты в json
def Ports_List(d,request):

    result = []
    for row in d.devices_ports_set.order_by('num'):
        result.append({
            'id': row.id,
            'datetime_str':DateTimeString(row.datetime_update,request).strip(),
            'num':row.num,
            'comment':row.comment,
            'status':row.status.name,
            'port':row.port.name,
            'author':row.author,
            'dogcode_list':row.get_dogcode_list()
        })

    return result



# Слоты в json
def Slots_List(d, request):

    result = []
    for row in d.device_link.all():
        result.append({
            'id': row.id,
            'datetime_str': DateTimeString(row.datetime_update, request).strip(),
            'num': row.num,
            'comment': row.comment,
            'status': row.status.name,
            'slot': row.slot.name,
            'author': row.author
        })

    return result



# Комбо в json
def Combo_List(d, request):

    result = []
    for row in d.devices_combo_set.all():
        result.append({
            'id': row.id,
            'datetime_str': DateTimeString(row.datetime_update, request).strip(),
            'num': row.num,
            'comment': row.comment,
            'status_port': row.status_port.name,
            'status_slot': row.status_slot.name,
            'slot': row.slot.name,
            'port': row.port.name,
            'author': row.author
        })

    return result




# Свойства в json
def properties_list(d, request):

    result = []
    for row in d.devices_properties_set.all():
        result.append({
            'id': row.id,
            'datetime_str': DateTimeString(row.datetime_update, request).strip(),
            'name': row.name,
            'value': row.value,
            'author': row.author
        })

    return result




# История статусов в json
def statuses_list(d, request):

    result = []
    for row in d.devices_statuses_set.all():
        result.append({
            'id': row.id,
            'datetime_str': DateTimeString(row.datetime_create, request).strip(),
            'status': row.status.name,
            'comment': row.comment,
            'author': row.author
        })

    return result




# История перемещений в json
def removal_list(d, request):

    result = []
    for row in d.devices_removal_set.all():
        result.append({
            'id': row.id,
            'datetime_str': DateTimeString(row.datetime_create, request).strip(),
            'address': row.address.getaddress(),
            'comment': row.comment,
            'author': row.author
        })

    return result







### Проверка допустимости значений
def check_json_data(data):


    for i in data["slots"].keys():
        print slots_list2
        if data["slots"].get(i)["type"] not in slots_list2:
            return "error slots value!"

    for i in data["ports"].keys():
        if data["ports"].get(i)["type"] not in ports_list2:
            return "error ports value!"

    for i in data["allowed_parrents"]:
        if i not in slots_list2:
            return "error allowed_parents value!"

    for i in data["combo"].keys():
        if data["combo"].get(i)["port"]["type"] not in ports_list2:
            return "error combo value!"
        if data["combo"].get(i)["slot"]["type"] not in slots_list2:
            return "error combo value!"



    return "ok"





### Проверка допустимости значений для модели интерфейсов
def check_json_data2(data):


    for i in data["interfaces"]:
        if i not in interfaces_list2:
            return "error interfaces value!"


    return "ok"




def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get








        ### Получение данных схемы
        if r.has_key("scheme") and rg("scheme") != '':
            scheme_id = int(request.GET["scheme"],10)

            s = devices_scheme.objects.get(pk=scheme_id)
            data = {
                "name":s.name,
                "scheme_device":"%s" % pformat(s.scheme_device),
            }

            response_data = data





        ### Сохранение device_id
        if r.has_key("action") and rg("action") == 'savedevid':

            dev_id = int(request.GET["dev_id"], 10)
            request.session["dev_id"] = dev_id

            response_data = {"result":"ok"}



        ### Поиск для устройств
        if r.has_key("search"):

            search = request.GET["search"]
            request.session["search_device"] = search

            response_data = {"result":"ok"}



        ### Поиск для сетевых элементов
        if r.has_key("search2"):

            search = request.GET["search2"]
            request.session["search_netelem"] = search

            response_data = {"result":"ok"}




        ### Данные по устройству в целом
        if r.has_key("action") and rg("action") == 'getdevicedata':

            tz = request.session['tz']

            if request.session.has_key("dev_id"):
                dev_id = request.session["dev_id"]
                d = devices.objects.get(pk=dev_id)


                data = {
                    "serial":d.serial,
                    "model":d.device_scheme.name,
                    "address":d.address.getaddress(),
                    "status":d.getstatus(),
                    "company":d.company.name,
                    "ports": Ports_List(d,request),
                    "slots": Slots_List(d,request),
                    "combo": Combo_List(d,request),
                    "properties": properties_list(d,request),
                    "statuses": statuses_list(d,request),
                    "removal": removal_list(d,request)
                }
                response_data = {"result": data}
            else:
                response_data = {"result": "error"}




        #### Поиск устройства
        if r.has_key("term") and rg("term") != "":
            term = request.GET["term"]
            obj = []



            for item in devices.objects.filter(Q(address__city__name__icontains=term) | Q(address__street__name__icontains=term) | Q(serial__icontains=term)).order_by("address__city__name","address__street__name"):

                label =  "{name} серийник:{serial} адрес: {city} {street} {house}".format(name=item.name.encode("utf-8")[:40] if item.name else '',serial=item.serial.encode("utf-8")[:20] if item.serial else '',city=item.address.city.name.encode("utf-8") if item.address.city.name else '',street=item.address.street.name.encode("utf-8") if item.address.street.name else '',house=item.address.house.encode("utf-8") if item.address.house else '')
                obj.append(
                    {
                        "label": label,
                        "value": item.id
                    }
                )

            response_data = obj





        ### Сохранение id сетевого элемента
        if r.has_key("savenetelem") and rg("savenetelem") != '':

            netelemid = int(request.GET["savenetelem"],10)
            request.session["netelemid"] = netelemid

            response_data = {"result":"ok"}




        ### Получение названия сетевого элемента
        if r.has_key("action") and rg("action") == 'getelemname':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)

            response_data = {"result": "ok","name":ne.name}




        ### Получение названия сетевого элемента
        if r.has_key("action") and rg("action") == 'saveelemname':
            name = request.GET["name"]
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)

            if netelems.objects.filter(name=name).exclude(pk=netelemid).count() == 0:
                ne.name = name
                ne.save()

            response_data = {"result": "ok"}




        ### Добавление устройства к сетевому элементу
        if r.has_key("action") and rg("action") == 'adddevice':
            deviceid = request.GET["deviceid"]
            d = devices.objects.get(pk=deviceid)
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)

            # Проверка есть ли уже такая запись
            if not ne.device.filter(pk=d.pk).exists():
                ne.device.add(d)

            response_data = {"result": "ok"}





        ### Удаление устройства из сетевому элементу
        if r.has_key("action") and rg("action") == 'deldevice':
            deviceid = request.GET["deviceid"]
            d = devices.objects.get(pk=deviceid)
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)

            ne.device.remove(d)

            response_data = {"result": "ok"}





        ### Список устройств по сетевому элементу
        if r.has_key("action") and rg("action") == 'listdevice':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)
            device_list = []
            for item in ne.device.all():
                device_list.append({
                    "id":item.id,
                    "name":item.name,
                    "address_city":item.address.city.name,
                    "address_street": item.address.street.name,
                    "address_house": item.address.house,
                    "serial":item.serial

                })

            response_data = {"result": "ok","device_list":device_list}




        ### Список портов на основе списка устройств
        if r.has_key("action") and rg("action") == 'interfaceform':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)
            ports_list = []
            for item in ne.device.all():
                for i in item.devices_ports_set.all():
                    ports_list.append({
                        "port_id":i.id,
                        "device_name":item.name,
                        "device_status":item.status.name,
                        "port_num":i.num,
                        "port":i.port.name,
                        "port_status":i.status.name
                    })

            response_data = {"result":"ok","ports_list":ports_list}







        ### Список связанных портов , название интерфейса, комментарий
        if r.has_key("action") and rg("action") == 'interfaceform2':
            interface_id = request.GET["interface_id"]
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)
            interface = logical_interfaces.objects.get(pk=int(interface_id,10))
            ports_list = []
            for item in interface.ports.all():
                ports_list.append(item.id)

            response_data = {"result":"ok","ports_list":ports_list,"name":interface.name,"comment":interface.comment}




        ### Задание id адреса для отображения устройств аудита портов
        if r.has_key("action") and rg("action") == 'get_devices_byaddress':
            address_id = request.GET["address_id"]
            address_label = request.GET["address_label"]

            request.session['address_id'] = address_id
            request.session['address_label'] = address_label

            response_data = {"result":"ok"}






        ### Список логических интерфейсов по текущему сетевому элементу
        if r.has_key("action") and rg("action") == 'interfacedata':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)
            interfaces_list = []

            for item in ne.logical_interfaces_set.all():

                ## Порты
                ports = []
                for i in item.ports.all():
                    ports.append({
                        "num":i.num,
                        "port":i.port.name,
                        "device":i.device.name
                    })

                # свойства логического интерфейса
                props = []

                for j in logical_interfaces_prop.objects.filter(logical_interface=item):
                    props.append({
                        "interface_id":item.id,
                        "prop_id":j.id,
                        "prop_name":j.prop.name,
                        "prop_select_id":j.prop.id,
                        "prop_val":j.val,
                        "prop_comment":j.comment
                    })

                interfaces_list.append({
                    "interface_id": item.id,
                    "interface_name": item.name,
                    "interface_comment": item.comment,
                    "devices_ports": ports,
                    "props":props
                })

            response_data = {"result": "ok", "interfaces_list": interfaces_list}




        ### Удаление логического интерфейса
        if r.has_key("action") and rg("action") == 'deleteinterface':
            interface_id = request.GET["interface_id"]
            interface = logical_interfaces.objects.get(pk=int(interface_id,10))
            for port in interface.ports.all():
                interface.ports.remove(port)

            ## Удаление созданных свойств
            logical_interfaces_prop.objects.filter(logical_interface=interface).delete()

            interface.delete()

            response_data = {"result": "ok"}



        ### Удаление устройства из сетевому элементу
        if r.has_key("action") and rg("action") == 'deleteprop':
            prop_id = int(request.GET["prop_id"],10)
            p = logical_interfaces_prop.objects.get(pk=prop_id)
            p.delete()

            response_data = {"result": "ok"}







    if request.method == "POST":


        data = eval(request.body)

        # Создание схемы устройства
        if data.has_key("action") and data["action"] == 'create_scheme':

            ### Проверка корректности значений в json схеме
            check = check_json_data(eval(data["scheme_device"]))

            if check == "ok":

                devices_scheme.objects.create(
                    scheme_device=eval(data["scheme_device"]),
                    name=data["name"],
                    author=request.user.get_username() + " (" + request.user.get_full_name() + ")"
                )

            response_data = {"result":check}



        # Изменение схемы устройства
        if data.has_key("action") and data["action"] == 'edit_scheme':

            ### Проверка корректности значений в json схеме
            check = check_json_data(eval(data["scheme_device"]))

            if check == "ok":

                s = devices_scheme.objects.get(pk=int(data["scheme_id"]))
                s.scheme_device = eval(data["scheme_device"])
                s.name = data["name"]
                s.save()

                logger.info("{user} внес изменение в модель устройства {name}".format(user=request.user.get_username(),name=s.name))

            response_data = {"result":check}







        # Создание устройства
        if data.has_key("action") and data["action"] == 'create-device':

            scheme = int(data["scheme"],10)
            company = int(data["company"],10)
            address = data["address"]
            serial = data["serial"]

            s = devices_scheme.objects.get(pk=scheme)
            c = address_companies.objects.get(pk=company)
            a = address_house.objects.get(pk=address)

            u = request.user.get_username()+ " ("+request.user.get_full_name()+")"

            d = devices.objects.create(
                name = s.name,
                company = c,
                address = a,
                serial = serial,
                device_scheme = s,
                author = u
            )


            d.mkports(author=u)
            d.mkslots(author=u)
            d.mkcombo(author=u)
            d.mkprop(author=u)

            request.session["dev_id"] = d.id

            response_data = {"result": "ok" }




        # Изменение порта
        if data.has_key("action") and data["action"] == 'edit-port':

            port_id = int(data["port_id"], 10)
            status = int(data["status"], 10)
            num = data["num"]
            comment = data["comment"]

            s = port_status.objects.get(pk=status)
            p = devices_ports.objects.get(pk=port_id)
            u = request.user.get_username()+ " ("+request.user.get_full_name()+")"

            p.num = num
            p.status = s
            p.comment = comment
            p.author = u
            p.save()

            response_data = {"result": "ok"}





        # Изменение порта
        if data.has_key("action") and data["action"] == 'edit-slot':
            slot_id = int(data["slot_id"], 10)
            status = int(data["status"], 10)
            num = data["num"]
            comment = data["comment"]

            st = slot_status.objects.get(pk=status)
            s = devices_slots.objects.get(pk=slot_id)
            u = request.user.get_username() + " (" + request.user.get_full_name() + ")"

            s.num = num
            s.status = st
            s.comment = comment
            s.author = u
            s.save()

            response_data = {"result": "ok"}





        # Изменение комбо порта
        if data.has_key("action") and data["action"] == 'edit-combo':
            port_id = int(data["port_id"], 10)
            status_port = int(data["status_port"], 10)
            status_slot = int(data["status_slot"], 10)
            num = data["num"]
            comment = data["comment"]

            ss = slot_status.objects.get(pk=status_slot)
            sp = port_status.objects.get(pk=status_port)
            c = devices_combo.objects.get(pk=port_id)
            u = request.user.get_username() + " (" + request.user.get_full_name() + ")"

            c.num = num
            c.status_port = sp
            c.status_slot = ss
            c.comment = comment
            c.author = u
            c.save()

            response_data = {"result": "ok"}




        # Изменение свойства
        if data.has_key("action") and data["action"] == 'edit-prop':
            prop_id = int(data["prop_id"], 10)
            value = data["value"]

            p = devices_properties.objects.get(pk=prop_id)

            u = request.user.get_username() + " (" + request.user.get_full_name() + ")"

            p.value = value
            p.author = u
            p.save()

            response_data = {"result": "ok"}




        # Установка статуса устройства
        if data.has_key("action") and data["action"] == 'set-device-status':

            status_id = int(data["status_id"],10)
            comment = data["comment"]

            ds = device_status.objects.get(pk=status_id)

            d = devices.objects.get(pk=request.session["dev_id"])

            u = request.user.get_username() + " (" + request.user.get_full_name() + ")"

            d.status = ds
            d.author = u
            d.save()

            devices_statuses.objects.create(
                device = d,
                status = ds,
                author = u,
                comment = comment
            )

            response_data = {"result": "ok"}





        # Перемещение
        if data.has_key("action") and data["action"] == 'device-removal':
            address_id = data["address_id"]
            comment = data["comment"]

            a = address_house.objects.get(pk=address_id)

            d = devices.objects.get(pk=request.session["dev_id"])

            u = request.user.get_username() + " (" + request.user.get_full_name() + ")"

            d.address = a
            d.author = u
            d.save()

            devices_removal.objects.create(
                device=d,
                address=a,
                author=u,
                comment=comment
            )

            response_data = {"result": "ok"}




        # Создание сетевого элемента
        if data.has_key("action") and data["action"] == 'create_netelement':
            name = data["name"]

            if netelems.objects.filter(name=name).count() == 0:

                u = request.user.get_username() + " (" + request.user.get_full_name() + ")"
                ne = netelems.objects.create(name=name,author=u)
                response_data = {"result": "ok", "neid":ne.id}

            else:

                response_data = {"result": "error"}





        # Изменение сетевого элемента
        if data.has_key("action") and data["action"] == 'edit_netelement':
            ne = data["ne"]
            name = data["name"]

            if netelems.objects.filter(name=name).count() == 0:

                netelems.objects.create(name=name)
                response_data = {"result": "ok"}

            else:

                response_data = {"result": "error"}






        # Создание логического интерфейса
        if data.has_key("action") and data["action"] == 'createinterface':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)

            # Проверка есть ли такой интерфейс
            if not logical_interfaces.objects.filter(name=data["name"],netelem=ne).exists():

                ports = data["ports"]
                # Создание логического интерфейса
                lint = logical_interfaces.objects.create(name=data["name"],comment=data["comment"],netelem=ne)
                ## Связывание по физическим портам
                for a in ports:
                    p = devices_ports.objects.get(pk=a)
                    lint.ports.add(p)


                response_data = {"result": "ok"}

            ### Интерфейс с таким именем уже есть
            else:
                response_data = {"result": "error"}




        # редактирование логического интерфейса
        if data.has_key("action") and data["action"] == 'editinterface':
            netelemid = request.session["netelemid"]
            ne = netelems.objects.get(pk=netelemid)
            interfaceid = data["interfaceid"]

            # Проверка есть ли такой интерфейс с таким же именем за исключением этого
            if not logical_interfaces.objects.filter(name=data["name"], netelem=ne).exclude(pk=interfaceid).exists():

                # порты , которые отмечены
                ports_click = data["ports"]
                # порты в данные момент связанные
                ports_link = []

                lint = logical_interfaces.objects.get(pk=interfaceid)
                lint.name = data["name"]
                lint.comment = data["comment"]
                lint.save()

                for p in lint.ports.all():
                    ports_link.append(p.id)

                ### Проверка и добавление связанности по портам
                for port_id in ports_click:
                    if port_id not in ports_link:
                        n = devices_ports.objects.get(pk=port_id)
                        lint.ports.add(n)

                ### Проверка на отсутсвие и удаление
                for port_id in ports_link:
                    if port_id not in ports_click:
                        n = devices_ports.objects.get(pk=port_id)
                        lint.ports.remove(n)



                response_data = {"result": "ok"}

            ### Интерфейс с таким именем уже есть
            else:
                response_data = {"result": "error"}




        # Создание свойства логического интерфейса
        if data.has_key("action") and data["action"] == 'createprop':

            prop = logical_interfaces_prop_list.objects.get(pk=int(data["prop"],10))
            lint = logical_interfaces.objects.get(pk=int(data["interface_id"],10))

            logical_interfaces_prop.objects.create(
                logical_interface = lint,
                prop = prop,
                val = data["value"],
                comment = data["comment"]
            )


            response_data = {"result": "ok"}



        # Редактирование свойства логического интерфейса
        if data.has_key("action") and data["action"] == 'editprop':
            lintprop = logical_interfaces_prop.objects.get(pk=int(data["prop_id"],10))
            prop = logical_interfaces_prop_list.objects.get(pk=int(data["prop"], 10))

            lintprop.prop = prop
            lintprop.val = data["value"]
            lintprop.comment = data["comment"]
            lintprop.save()

            response_data = {"result": "ok"}



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
