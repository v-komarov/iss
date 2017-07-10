#coding:utf-8

import datetime
import json
import logging
import operator

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect

from iss.localdicts.models import address_city, address_house
from django.shortcuts import redirect
from django.core import serializers
from django import template
from django.db.models import F,Func,Value
from django.db.models import Q







def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get








        ### Получение координат городов и населенных пунктов
        if r.has_key("action") and rg("action") == 'get_city_geo':
            city_id = int(request.GET["city_id"],10)

            city = address_city.objects.get(pk=city_id)
            r = address_house.objects.filter(city=city,house=None,street=None).first()

            data = {
                "lat": r.geo["lat"],
                "lng": r.geo["lng"]
            }

            response_data = data




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
