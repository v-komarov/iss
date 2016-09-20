#coding:utf-8

import datetime
import json
import time

from django.http import HttpResponse




def get_json(request):

    response_data = {}

    r = request.GET
    rg = request.GET.get

    # Отправка параметров
    if r.has_key("settings") and rg("settings") != '':

        response_data['settings'] = {}
        if request.session.has_key("status_id"):
            response_data['settings']['status'] = request.session["status_id"]
        else:
            response_data['settings']['status'] = ""
        if request.session.has_key("severity_id"):
            response_data['settings']['severity'] = request.session["severity_id"]
        else:
            response_data['settings']['severity'] = ""
        if request.session.has_key("manager"):
            response_data['settings']['manager'] = request.session["manager"]
        else:
            response_data['settings']['manager'] = ""
        if request.session.has_key("first_seen"):
            response_data['settings']['first_seen'] = request.session["first_seen"]
        else:
            response_data['settings']['first_seen'] = ""
        if request.session.has_key("last_seen"):
            response_data['settings']['last_seen'] = request.session["last_seen"]
        else:
            response_data['settings']['last_seen'] = ""

    if r.has_key("status") and rg("status") != '':
        request.session['status_id'] = request.GET["status"]
        print request.session['status_id']

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

