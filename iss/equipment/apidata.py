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
from django import template
from django.views.decorators.csrf import csrf_exempt

from iss.equipment.models import devices_ip,footnodes,agregators,client_mac_log,client_login_log
from iss.localdicts.models import logical_interfaces_prop_list,address_house,address_templates
from iss.inventory.models import logical_interfaces_prop,logical_interfaces,devices,netelems

from transliterate import translit
from transliterate import detect_language



prop = logical_interfaces_prop_list.objects.get(name='ipv4')



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)








def ip2address(ip):
    """Определение id адреса по ip"""

    ### Поиск по ip адресу на интерфейсе manager
    if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
        p = logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').first()
        #### Определение серевого элемента
        ne = p.logical_interface.netelem

        if ne.device.all().count() != 0:
            ### Поиск связанного устройства
            device = ne.device.all().first()

            return device.address.id

        else:
            return None


    else:

        return None





def address_dict2(ip_list):
    """Формирование словаря адресов аварии (по списку id адресов)"""

    addressid_list = []
    for ip in ip_list:
        address_id = ip2address(ip)
        if address_id != None:
            addressid_list.append(address_id)

    data = {}

    address_list = []

    for item in addressid_list:
        addr = address_house.objects.get(pk=item)

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









@csrf_exempt
def get_apidata(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get



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




    if request.method == "POST":

        action = request.POST['action']
        ip_list = request.POST['iplist'].split(";")

        response_data = {'result':'ok'}

        ### Формирование через шаблонизатор
        address_str = ""
        if address_templates.objects.filter(name="accidentname").count() == 1:
            templ = address_templates.objects.get(name="accidentname").template
            t = template.Template(templ)
            c = template.Context({'data': address_dict2(ip_list)})
            address_str = t.render(c)

            response_data = {'address':address_str}



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
