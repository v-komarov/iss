#coding:utf-8

import datetime
import json
import logging

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect

from iss.inventory.models import devices_scheme,interfaces_scheme,devices
from iss.localdicts.models import ports,slots,interfaces,address_companies,address_house
from django.shortcuts import redirect
from django.core import serializers


logger = logging.getLogger('inventory')



ports_list = []
slots_list = []
interfaces_list = []


for item in ports.objects.all():
    ports_list.append(item.name)

for item in slots.objects.all():
    slots_list.append(item.name)


for item in interfaces.objects.all():
    interfaces_list.append(item.name)




### Проверка допустимости значений
def check_json_data(data):

    for i in data["slots"].keys():
        if data["slots"].get(i)["type"] not in slots_list:
            return "error slots value!"

    for i in data["ports"].keys():
        if data["ports"].get(i)["type"] not in ports_list:
            return "error ports value!"

    for i in data["allowed_parrents"]:
        if i not in slots_list:
            return "error allowed_parents value!"

    for i in data["combo"].keys():
        if data["combo"].get(i)["port"]["type"] not in ports_list:
            return "error combo value!"
        if data["combo"].get(i)["slot"]["type"] not in slots_list:
            return "error combo value!"



    return "ok"





### Проверка допустимости значений для модели интерфейсов
def check_json_data2(data):


    for i in data["interfaces"]:
        if i not in interfaces_list:
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

            if request.session.has_key("dev_id"):
                dev_id = request.session["dev_id"]
                d = devices.objects.get(pk=dev_id)



                data = {
                    "tz":request.session["tz"],
                    "model":d.device_scheme.name,
                    "address":d.address.city.name,
                    "status":d.status,
                    "company":d.company.name,
                    "ports":serializers.serialize('json', d.devices_ports_set.all()),
                    "slots":serializers.serialize('json', d.device_link.all()),
                    "combo":serializers.serialize('json', d.devices_combo_set.all()),
                    "properties":serializers.serialize('json', d.devices_properties_set.all()),
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




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
