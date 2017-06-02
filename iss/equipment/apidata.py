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



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


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

            response_data = {'result': 'OK'}



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
