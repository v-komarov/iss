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
                rr = devices_ip.objects.get(ipaddress=ipaddress, device_domen=domen)
                response_data["result"] = {
                    "sysname":rr.device_name,
                    "sysdescr":rr.device_descr,
                    "syslocation":rr.device_location,
                    "serial":rr.device_serial,
                    "mac":rr.chassisid
                }

            else:
                response_data["result"] = "error"



        ### Получение данных опорного узла
        if r.has_key("ftnode") and rg("ftnode") != '':
            footnode = int(request.GET["ftnode"],10)
            print footnode
            f = footnodes.objects.get(pk=footnode)
            response_data["result"] = {
                "ipaddress":f.ipaddress,
                "descr":f.descr,
                "location":f.location,
                "serial":f.serial,
                "name":f.name,
                "mac":f.chassisid,
                "domen":f.device_domen
            }
            print response_data["result"]



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

        if data.has_key("action") and data["action"] == 'edit_footnode':

            n = footnodes.objects.get(pk=int(data["row_id"]))
            n.ipaddress = data["ipaddress"]
            n.name = data["name"]
            n.descr = data["descr"]
            n.location = data["location"]
            n.chassisid = data["mac"]
            n.serial = data["serial"]
            n.device_domen = data["domen"]
            n.save()






    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
