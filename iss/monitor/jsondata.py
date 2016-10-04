#coding:utf-8

import datetime
import json
import time
import pickle

from pytz import timezone

from django.http import HttpResponse

from iss.monitor.models import events



def get_json(request):

    response_data = {}

    r = request.GET
    rg = request.GET.get


    if r.has_key("status") and rg("status") != '':
        request.session['status_id'] = pickle.dumps(eval(request.GET["status"]))


    if r.has_key("severity") and rg("severity") != '':
        request.session['severity_id'] = pickle.dumps(eval(request.GET["severity"]))

    if r.has_key("manager") and rg("manager") != '':
        request.session['manager'] = pickle.dumps(eval(request.GET["manager"]))

    if r.has_key("first_seen"):
        request.session['first_seen'] = request.GET["first_seen"]

    if r.has_key("last_seen"):
        request.session['last_seen'] = request.GET["last_seen"]

    if r.has_key("search") and rg("search") != '':
        if request.GET["search"] == "xxxxx":
            request.session['search'] = ""
        else:
            request.session['search'] = request.GET["search"]

    if r.has_key("containergroup") and rg("containergroup") != '':
        if request.GET["containergroup"] == "_____":
            del request.session['containergroup']
        else:
            request.session['containergroup'] = request.GET["containergroup"]


    if r.has_key("addgroup") and rg("addgroup") != '[]':
        id_group = eval(request.GET["addgroup"])
        g = []
        for item in id_group:
            if request.session['containergroup'] != item:
                g.append(item)
                i = events.objects.get(pk=item)
                i.agregation = True
                i.agregator = False
                i.data['containergroup'] = []
                i.save()
        e = events.objects.get(pk=request.session['containergroup'])
        data = e.data
        if data.has_key('containergroup'):
            for a in g:
                data['containergroup'].append(a)
        else:
            data['containergroup'] = g
        e.agregation = False
        e.agregator = True
        e.save()



    if r.has_key("getmembers") and rg("getmembers") != '':
        tz = request.session['tz']
        e = events.objects.get(pk=request.session['containergroup'])
        l = e.data['containergroup']
        a = []
        for item in l:
            i = events.objects.get(pk=item)
            a.append(
                {
                    'id':i.id,
                    'uuid':i.uuid,
                    'first_seen':i.first_seen.strftime("%d.%m.%Y %H:%M"),
                    'last_seen':i.last_seen.strftime("%d.%m.%Y %H:%M"),
                    'status':i.status_id.name,
                    'severity':i.severity_id.name,
                    'manager':i.manager,
                    'event_class':i.event_class,
                    'device_system':i.device_system,
                    'device_group':i.device_group,
                    'device_class':i.device_class,
                    'device_net_address':i.device_net_address,
                    'device_location':i.device_location,
                    'element_identifier':i.element_identifier,
                    'element_sub_identifier':i.element_sub_identifier
                }
            )
        response_data['members'] = a



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

