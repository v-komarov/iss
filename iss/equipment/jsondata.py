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

from iss.equipment.models import devices_ip



def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get

        if r.has_key("notaccess") and rg("notaccess") != '':
            if request.session.has_key("notaccess"):
                del request.session['notaccess']
            else:
                request.session['notaccess'] = "ok"

        if r.has_key("norewrite") and rg("norewrite") != '':
            if request.session.has_key("norewrite"):
                del request.session['norewrite']
            else:
                request.session['norewrite'] = "ok"

        if r.has_key("search") and rg("search") != '':
            if request.GET["search"] == "xxxxx":
                request.session['search'] = ""
            else:
                request.session['search'] = request.GET["search"]


    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
