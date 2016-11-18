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

from iss.equipment.models import devices_ip,footnodes,agregators





def outdata(response_data):

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response





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

            ra = devices_ip.objects.get(pk=rowid)
            ra.device_serial = serial
            ra.chassisid = mac
            ra.no_rewrite = readonly
            ra.save()

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

            f = footnodes.objects.get(pk=footnode)
            response_data["result"] = {
                "ipaddress":f.ipaddress,
                "descr":f.descr,
                "location":f.location,
                "serial":f.serial,
                "name":f.name,
                "mac":f.chassisid,
                "domen":f.domen
            }

            response_data["result"]

        ### Получение данных агрегатора
        if r.has_key("agregator") and rg("agregator") != '':
            ag = int(request.GET["agregator"], 10)

            f = agregators.objects.get(pk=ag)
            response_data["result"] = {
                "ipaddress": f.ipaddress,
                "descr": f.descr,
                "location": f.location,
                "serial": f.serial,
                "name": f.name,
                "mac": f.chassisid,
                "domen": f.domen,
                "footnode":f.footnode.id,
                "uplink":f.uplink_ports
            }

            response_data["result"]




    if request.method == "POST":


        data = eval(request.body)


        if data.has_key("action") and data["action"] == 'create_footnode':


            footnodes.objects.create(
                ipaddress = data["ipaddress"],
                name = data["name"],
                descr = data["descr"],
                location = data["location"],
                serial = data["serial"],
                chassisid = data["mac"],
                domen = data["domen"]
            )

        if data.has_key("action") and data["action"] == 'edit_footnode':

            n = footnodes.objects.get(pk=int(data["row_id"]))
            n.ipaddress = data["ipaddress"]
            n.name = data["name"]
            n.descr = data["descr"]
            n.location = data["location"]
            n.chassisid = data["mac"]
            n.serial = data["serial"]
            n.domen = data["domen"]
            n.save()


        if data.has_key("action") and data["action"] == 'create_agregator':
            print data
            agregators.objects.create(
                ipaddress=data["ipaddress"],
                name=data["name"],
                descr=data["descr"],
                location=data["location"],
                serial=data["serial"],
                chassisid=data["mac"],
                domen=data["domen"],
                footnode = footnodes.objects.get(pk=data["footnode"]),
                uplink_ports=data["uplink"].split(",")
            )


        if data.has_key("action") and data["action"] == 'edit_agregator':
            a = agregators.objects.get(pk=int(data["row_id"]))
            a.ipaddress = data["ipaddress"]
            a.name = data["name"]
            a.descr = data["descr"]
            a.location = data["location"]
            a.chassisid = data["mac"]
            a.serial = data["serial"]
            a.domen = data["domen"]
            a.footnode = footnodes.objects.get(pk=data["footnode"])
            a.uplink_ports = data["uplink"].split(",")
            a.save()

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
