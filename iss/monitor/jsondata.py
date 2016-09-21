#coding:utf-8

import datetime
import json
import time

from django.http import HttpResponse




def get_json(request):

    response_data = {}

    r = request.GET
    rg = request.GET.get


    if r.has_key("status") and rg("status") != '':
        request.session['status_id'] = request.GET["status"]

    if r.has_key("severity") and rg("severity") != '':
        request.session['severity_id'] = request.GET["severity"]

    if r.has_key("manager") and rg("manager") != '':
        request.session['manager'] = request.GET["manager"]

    if r.has_key("first_seen"):
        request.session['first_seen'] = request.GET["first_seen"]

    if r.has_key("last_seen"):
        request.session['last_seen'] = request.GET["last_seen"]

    if r.has_key("search") and rg("search") != '':
        if request.GET["search"] == "xxxxx":
            request.session['search'] = ""
        else:
            request.session['search'] = request.GET["search"]


    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

