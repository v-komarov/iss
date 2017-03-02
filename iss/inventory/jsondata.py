#coding:utf-8

import datetime
import json

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse

from iss.inventory.models import devices_scheme,interfaces_scheme
from iss.localdicts.models import ports,slots,interfaces




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

            response_data = {"result": check}




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
