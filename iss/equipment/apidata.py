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



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
