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
        if r.has_key("action") and rg("action") == 'get_agregators':

            for a in agregators.objects.all():
                result.append({
                    'ipaddress':a.ipaddress,
                    'descr':a.descr,
                    'location':a.location,
                    'name':a.name,
                    'domen':a.domen,
                    'mac':a.chassisid,
                    'serial':a.serial,
                    'uplink_ports':a.uplink_ports
                })


            response_data = result

        if r.has_key("action") and rg("action") == 'get_lldpdata':

            for d in devices_ip.objects.all():
                result.append({
                    'ipaddress':d.ipaddress,
                    'descr':d.device_descr,
                    'location':d.device_location,
                    'name':d.device_name,
                    'domen':d.device_domen,
                    'mac':d.chassisid,
                    'serial':d.device_serial,
                    'lldp':d.ports
                })

            response_data = result



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




        ### Загрузка данных для отловленных mac адресов клиентов
        if r.has_key("action") and rg("action") == 'push_client_mac' and r.has_key("ipaddress") and r.has_key("port") and r.has_key("macaddress"):
            ### Получение ip адреса комутатора,порта,mac клиента
            ipaddress = request.GET["ipaddress"]
            macaddress = request.GET["macaddress"]
            port = request.GET["port"]

            ### Убрать из mac лишние символы
            reg = re.compile('[^a-zA-Z0-9 ]')
            m = reg.sub('', macaddress).lower()
            m2 = m[0:2] + ":" + m[2:4] + ":" + m[4:6] + ":" + m[6:8] + ":" + m[8:10] + ":" + m[10:12]

            ### Если такая запись уже есть - обновляем (дату)
            if client_mac_log.objects.filter(ipaddress=ipaddress,macaddress=m2,port=port).exists():

                client_mac_log.objects.filter(ipaddress=ipaddress,macaddress=m2,port=port).update(
                    create_update = krsk_tz.localize(datetime.datetime.now())
                )

            ### Если такой записи нет - добавляем
            else:
                client_mac_log.objects.create(
                    ipaddress=ipaddress,
                    macaddress=m2,
                    port=port
                )

            response_data = {'result':'OK'}




        ### Вывод отловленных mac адресов клиентов по ip коммутатора
        if r.has_key("action") and rg("action") == 'get_client_mac' and r.has_key("ipaddress"):
            ### Получение ip адреса комутатора
            ipaddress = request.GET["ipaddress"]

            for i in client_mac_log.objects.filter(ipaddress=ipaddress).order_by('create'):
                result.append({
                    'datetime':i.create.strftime('%Y-%m-%d %H:%M:%S'),
                    'ipaddress':i.ipaddress,
                    'port':i.port,
                    'macaddress':i.macaddress
                })

            response_data = result



        ### Загрузка отловленных логинов и mac адресов клиентов radius авторизации
        if r.has_key("action") and rg("action") == 'push_client_login' and r.has_key("macaddress") and r.has_key("login") and rg("macaddress") != "" and rg("login") != "":
            login = request.GET["login"]
            circuit_id = request.GET["circuit_id"]
            m = request.GET["macaddress"]
            m2 = m[0:2] + ":" + m[2:4] + ":" + m[4:6] + ":" + m[6:8] + ":" + m[8:10] + ":" + m[10:12]
            # Проверка наличие логина в кэше
            if not cache.get(login):
                client_login_log.objects.update_or_create(
                    login = login,
                    macaddress = m2
                )
                client_login_log.objects.filter(login=login,macaddress=m2).update(create_update=krsk_tz.localize(datetime.datetime.now()),circuit_id_tag=circuit_id)
                cache.set(login, m, 3600)

                response_data = {'result': 'OK','comment':'updated or inserted'}

            else:

                response_data = {'result': 'OK','comment':'found in cache'}



        ### Проверка наличия общих адресов (city=None,street=None) и их создание
        if r.has_key("action") and rg("action") == 'address_check':
            for addr in address_house.objects.exclude(street=None).exclude(city=None):
                addr.common_address()

            response_data = {"result": "ok"}





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



        #### Вывод списка адресов (домов)
        if r.has_key("action") and rg("action") == 'get_addresslist':
            response_data = u"ADDRESSID;CITYNAME;CITYID;STREETNAME;STREETID;HOUSE;\n"

            for addr in address_house.objects.order_by("city__name","street__name","house"):
                response_data = response_data + u"{addressid};{cityname};{cityid};{streetname};{streetid};{house};\n".format(
                    addressid=addr.id, cityname=addr.city.name, cityid=addr.city.id,
                    streetname=addr.street.name if addr.street else "", streetid=addr.street.id if addr.street else "",
                    house=addr.house if addr.house else "")



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
