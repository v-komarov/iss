#coding:utf-8

import json
import pickle
import datetime

import base64
from io import BytesIO


from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from django.db.models import Count, Q, Avg, Sum
from django.contrib.auth.models import User















def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get




        ### Фильтр по городу улице дому
        if r.has_key("action") and rg("action") == 'filter-addresslist':

            city = request.GET["city"].strip()
            street = request.GET["street"].strip()
            house = request.GET["house"].strip()


            if city != "" or street != "" or house != "":
                request.session["filter_addresslist"] = pickle.dumps({ 'city': city, 'street': street, 'house': house })

            if city == "" and street == "" and house == "":
                if request.session.has_key("filter_addresslist"):
                    del request.session["filter_addresslist"]


            response_data = {"result": "ok"}





        ### Очистка фильтр по городу улице дому
        if r.has_key("action") and rg("action") == 'filter-addresslist-clear':


            if request.session.has_key("filter_addresslist"):
                del request.session["filter_addresslist"]

            response_data = {"result": "ok"}



        ### Фильтр по городу улице дому по компании
        if r.has_key("action") and rg("action") == 'filter-company':

            city = request.GET["city"].strip()
            street = request.GET["street"].strip()
            house = request.GET["house"].strip()
            company = request.GET["company"].strip()


            request.session["filter_company"] = pickle.dumps({ 'city': city, 'street': street, 'house': house, 'company': company })

            if city == "" and street == "" and house == "" and company == "":
                if request.session.has_key("filter_company"):
                    del request.session["filter_company"]


            response_data = {"result": "ok"}





        ### Очистка фильтр по городу улице дому по компании
        if r.has_key("action") and rg("action") == 'filter-company-clear':


            if request.session.has_key("filter_company"):
                del request.session["filter_company"]

            response_data = {"result": "ok"}







    if request.method == "POST":


        data = eval(request.body)



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response


