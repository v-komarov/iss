#coding:utf-8

import datetime
import json
import time
import pickle
import operator
import uuid
import email

from email.utils import parsedate_tz, mktime_tz, formatdate
from pytz import timezone

from django.http import HttpResponse

from iss.equipment.models import devices_ip,footnodes



def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get

        #### Фильтр в списке устройств
        if r.has_key("notaccess") and rg("notaccess") != '':
            if request.session.has_key("notaccess"):
                del request.session['notaccess']
            else:
                request.session['notaccess'] = "ok"

        #### Фильтр в списке устройств
        if r.has_key("norewrite") and rg("norewrite") != '':
            if request.session.has_key("norewrite"):
                del request.session['norewrite']
            else:
                request.session['norewrite'] = "ok"

        ### Поиск в списке устройств
        if r.has_key("search") and rg("search") != '':
            if request.GET["search"] == "xxxxx":
                request.session['search'] = ""
            else:
                request.session['search'] = request.GET["search"]

        ## Сохранение данных строки в списке устройств
        if r.has_key("saverow") and rg("saverow") != '':
            rowid = int(request.GET["rowid"],10)
            serial = request.GET["serial"]
            mac = request.GET["mac"]
            if request.GET["readonly"] == "true":
                readonly = True
            else:
                readonly = False

            r = devices_ip.objects.get(pk=rowid)
            r.device_serial = serial
            r.chassisid = mac
            r.no_rewrite = readonly
            r.save()

            response_data["result"] = "ok"


        ### Получение данных snmp
        if r.has_key("getdevice") and rg("getdevice") != '':
            ipaddress = request.GET["getdevice"]
            domen = request.GET["domen"]

            if devices_ip.objects.filter(ipaddress=ipaddress,device_domen=domen).count() == 1:
                r = devices_ip.objects.get(ipaddress=ipaddress, device_domen=domen)
                response_data["result"] = {
                    "sysname":r.device_name,
                    "sysdescr":r.device_descr,
                    "syslocation":r.device_location,
                    "serial":r.device_serial,
                    "mac":r.chassisid
                }

            else:
                response_data["result"] = "error"





    if request.method == "POST":
        data = eval(request.body)

        print data

        if data.has_key("action") and data["action"] == 'create_footnode':


            footnodes.objects.create(
                ipaddress = data["ipaddress"],
                name = data["name"],
                descr = data["descr"],
                location = data["location"],
                serial = data["serial"],
                chassisid = data["mac"],
                device_domen = data["domen"]
            )
        """
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
        """






    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
