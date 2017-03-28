#coding:utf-8

import datetime
import json
import logging
import operator

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect

from iss.inventory.models import devices_scheme,interfaces_scheme,devices,devices_ports,devices_slots,devices_combo,devices_properties
from iss.localdicts.models import ports,slots,interfaces,address_companies,address_house,port_status,slot_status
from django.shortcuts import redirect
from django.core import serializers
from django import template
from django.db.models import F,Func,Value
from django.db import models


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
def ports_list(d,request):

    result = []
    for row in d.devices_ports_set.all():
        result.append({
            'id': row.id,
            'datetime_str':DateTimeString(row.datetime_update,request).strip(),
            'num':row.num,
            'comment':row.comment,
            'status':row.status.name,
            'port':row.port.name,
            'author':row.author
        })

    return result



# Слоты в json
def slots_list(d, request):

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
def combo_list(d, request):

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



        ### Получение данных схемы интерфейса
        if r.has_key("interfacescheme") and rg("interfacescheme") != '':
            scheme_id = int(request.GET["interfacescheme"], 10)

            s = interfaces_scheme.objects.get(pk=scheme_id)
            data = {
                "name": s.name,
                "scheme_interface": "%s" % pformat(s.scheme_interface),
            }

            response_data = data



        ### Сохранение device_id
        if r.has_key("action") and rg("action") == 'savedevid':

            dev_id = int(request.GET["dev_id"], 10)
            request.session["dev_id"] = dev_id

            response_data = {"result":"ok"}



        ### Поиск
        if r.has_key("search"):

            search = request.GET["search"]
            request.session["search_device"] = search

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
                    "status":d.status,
                    "company":d.company.name,
                    "ports": ports_list(d,request),
                    "slots": slots_list(d,request),
                    "combo": combo_list(d,request),
                    "properties": properties_list(d,request),
                }
                response_data = {"result": data}
            else:
                response_data = {"result": "error"}




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



        # Создание схемы интерфейса
        if data.has_key("action") and data["action"] == 'create_interfacescheme':

            ### Проверка корректности значений в json схеме
            check = check_json_data2(eval(data["scheme_interface"]))

            if check == "ok":
                interfaces_scheme.objects.create(
                    scheme_interface=eval(data["scheme_interface"]),
                    name=data["name"],
                    author=request.user.get_username() + " (" + request.user.get_full_name() + ")"
                )

            response_data = {"result": check}



        # Изменение схемы интерфейса
        if data.has_key("action") and data["action"] == 'edit_interfacescheme':

            ### Проверка корректности значений в json схеме
            check = check_json_data2(eval(data["scheme_interface"]))

            if check == "ok":
                s = interfaces_scheme.objects.get(pk=int(data["scheme_id"]))
                s.scheme_interface = eval(data["scheme_interface"])
                s.name = data["name"]
                s.save()

                logger.info("{user} внес изменение в модель интерфейса {name}".format(user=request.user.get_username(), name=s.name))

            response_data = {"result": check}




        # Изменение схемы интерфейса
        if data.has_key("action") and data["action"] == 'create_netelement':

            #return HttpResponseRedirect("/inventory/netelement/")

            response_data = {"result": "ok"}




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




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
