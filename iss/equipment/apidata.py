#coding:utf-8

import datetime
import json
import time
import pickle
import operator
import uuid
import email
import re

from email.utils import parsedate_tz, mktime_tz, formatdate
from pytz import timezone

from django.http import HttpResponse
from django.core.cache import cache

from iss.equipment.models import devices_ip,footnodes,agregators,client_mac_log,client_login_log
from iss.localdicts.models import logical_interfaces_prop_list,address_house
from iss.inventory.models import logical_interfaces_prop,logical_interfaces,devices,netelems

from transliterate import translit
from transliterate import detect_language



prop = logical_interfaces_prop_list.objects.get(name='ipv4')



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


prop = logical_interfaces_prop_list.objects.get(name='ipv4')



def get_apidata(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        result = []



        ### Проверка расчета ЗКЛ по ip адресу
        if r.has_key("action") and rg("action") == 'get_zkllist'  and r.has_key("ipaddress"):
            ipaddress = request.GET["ipaddress"]
            result = []
            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=ipaddress,
                                                      logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.get(prop=prop, val=ipaddress)
                ### Добавление строк с зкл
                result.extend(p.logical_interface.get_zkl(ipaddress))

            response_data = result









    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response





### Вывод результата в текстовом формате
def get_apidata2(request):

    response_data = ""

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get

        #### Вывод списка ip адресов управления, сетевых элементов, устройств
        if r.has_key("action") and rg("action") == 'get_ipnetelemdev':

            response_data = u"IPADDRESS;NETELEM;MODEL;STATUS;PORTS;COMBO;SLOTS;CITY;STREET;HOUSE;\n"

            for li in logical_interfaces.objects.filter(name="manage").order_by("netelem__name"):
                ### Список связанных устройств
                for dev_id in li.get_dev_list():
                    dev = devices.objects.get(pk=dev_id)
                    for li_prop in li.logical_interfaces_prop_set.all():
                        if li_prop.prop == prop:
                            response_data = response_data + u"{ip};{sysname};{model};{status};{ports};{combo};{slots};{city};{street};{house};\n".format(ip=li_prop.val,sysname=li.netelem,model=dev.device_scheme.name,status=dev.getstatus(),ports=dev.get_ports_count(),combo=dev.get_combo_count(),slots=dev.get_slots_count(),city=dev.address.city.name,street=dev.address.street.name,house=dev.address.house)





        #### Вывод сетевых элементов без ip адреса управления
        if r.has_key("action") and rg("action") == 'get_netelemnotip':

            response_data = u"NETELEMID;NETELEM;MODEL;STATUS;PORTS;COMBO;SLOTS;CITY;STREET;HOUSE;\n"

            for ne in netelems.objects.order_by("name"):
                ### Список связанных устройств
                for dev in ne.device.all():
                    if not logical_interfaces.objects.filter(name="manage",netelem=ne).exists():
                        response_data = response_data + u"{id};{sysname};{model};{status};{ports};{combo};{slots};{city};{street};{house};\n".format(
                            id=ne.id,sysname=ne.name, model=dev.device_scheme.name if dev.device_scheme else "", status=dev.getstatus(),
                            ports=dev.get_ports_count(), combo=dev.get_combo_count(), slots=dev.get_slots_count(),
                            city=dev.address.city.name, street=dev.address.street.name, house=dev.address.house)

                    else:
                        li = logical_interfaces.objects.get(name="manage",netelem=ne)
                        if not logical_interfaces_prop.objects.filter(prop=prop,logical_interface=li).exists():
                            response_data = response_data + u"{id};{sysname};{model};{status};{ports};{combo};{slots};{city};{street};{house};\n".format(
                                id=ne.id, sysname=ne.name, model=dev.device_scheme.name if dev.device_scheme else "", status=dev.getstatus(),
                                ports=dev.get_ports_count(), combo=dev.get_combo_count(), slots=dev.get_slots_count(),
                                city=dev.address.city.name, street=dev.address.street.name, house=dev.address.house)



        #### Вывод устройств без связанных сетевых элементов
        if r.has_key("action") and rg("action") == 'get_devicesnotelement':

            response_data = u"DEVICEID;MODEL;SERIAL;STATUS;PORTS;COMBO;SLOTS;CITY;STREET;HOUSE;\n"


            for dev in devices.objects.order_by("device_scheme"):
                if not dev.netelems_set.all().exists():
                    response_data = response_data + u"{id};{model};{status};{ports};{combo};{slots};{city};{street};{house};\n".format(
                        id=dev.id, model=dev.device_scheme.name if dev.device_scheme else "",
                        status=dev.getstatus(),
                        ports=dev.get_ports_count(), combo=dev.get_combo_count(), slots=dev.get_slots_count(),
                        city=dev.address.city.name, street=dev.address.street.name, house=dev.address.house)



    response = HttpResponse(response_data, content_type="text/plain; charset=utf-8")
    response['Access-Control-Allow-Origin'] = "*"
    return response
