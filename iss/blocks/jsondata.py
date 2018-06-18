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

from iss.blocks.models import block_managers, buildings, comments_logs
from iss.localdicts.models import address_house













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



        ### Cписок логов карточки компании
        if r.has_key("action") and rg("action") == 'get-company-list-logs':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            log_list = []
            for row in comments_logs.objects.filter(manager=company,log=True).order_by("-datetime_create"):
                log_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": log_list }




        ### Реестр проектов: список коментариев
        if r.has_key("action") and rg("action") == 'get-company-list-comments':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            comment_list = []
            for row in comments_logs.objects.filter(manager=company,log=False).order_by("-datetime_create"):
                comment_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": comment_list }






    if request.method == "POST":


        data = eval(request.body)




        ### Сохранение карточки компании
        if data.has_key("action") and data["action"] == 'company-common-save':


            company_id = data["company_id"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            address_id = data["address"]
            address_law_id = data["address_law"]

            address = address_house.objects.get(pk=int(address_id,10))
            address_law = address_house.objects.get(pk=int(address_law_id,10))

            name = data["name"].strip()
            inn = data["inn"].strip()
            phone = data["phone"].strip()
            email = data["email"].strip()
            contact = data["contact"].strip()



            company.name = name
            company.inn = inn
            company.phone = phone
            company.email = email
            company.contact = contact
            company.address = address
            company.address_law = address_law

            company.save()

            comments_logs.objects.create(
                manager = company,
                user = request.user,
                comment = u"Сохранены данные карточки компании",
                log=True
            )



            response_data = {"result": "ok"}




        ### Добавление коментария компании
        if data.has_key("action") and data["action"] == 'company-comment-add':

            company_id = data["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            comment = data["comment"].strip()

            if comment != "":


                comments_logs.objects.create(
                    manager = company,
                    user = request.user,
                    comment = comment
                )




            response_data = {"result": "ok"}






    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response


