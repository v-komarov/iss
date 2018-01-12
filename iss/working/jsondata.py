#coding:utf-8

import datetime
import json
import logging
import operator

from pytz import timezone
from pprint import pformat

from django.http import HttpResponse, HttpResponseRedirect

from iss.inventory.models import devices_scheme,devices,devices_ports,devices_slots,devices_combo,devices_properties,devices_statuses,devices_removal,netelems,logical_interfaces,logical_interfaces_prop
from iss.localdicts.models import ports,slots,interfaces,address_companies,address_house,port_status,slot_status,device_status,logical_interfaces_prop_list
from django.shortcuts import redirect
from django.core import serializers
from django import template
from django.db.models import F,Func,Value
from django.db import models
from django.db.models import Q
from django.db.models import Count


from iss.working.models import working_time, working_relax, marks, working_log




def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        ### Получение статусов пользователя
        if r.has_key("action") and rg("action") == 'get-statuses':

            user = request.user
            work = "yes" if user.profile.work_status else "no"
            relax = "yes" if user.profile.relax_status else "no"

            response_data = {"result": "ok", "work": work, "relax": relax}


        ### Начало работы (смены)
        if r.has_key("action") and rg("action") == 'work-start':

            user = request.user
            user.profile.work_status = True
            user.save()


            if not working_time.objects.filter(user=user,current=True).exists():
                ### Создание записи "Смены"
                working_time.objects.create(
                    user=user
                )

            response_data = { "result": "ok" }



        ### Завершение работы (смены)
        if r.has_key("action") and rg("action") == 'work-end':

            user = request.user
            user.profile.work_status = False
            user.save()

            if working_time.objects.filter(user=user,current=True).exists():
                ### Завершение работы (смены)
                current = working_time.objects.filter(current=True,user=user).last()
                current.current = False
                current.save()


            response_data = { "result": "ok" }



        ### Начало перерыва
        if r.has_key("action") and rg("action") == 'relax-start':

            user = request.user
            user.profile.relax_status = True
            user.save()

            if not working_relax.objects.filter(user=user,current=True).exists():
                ### Создание перерыва
                working_relax.objects.create(
                    user=user
                )

            response_data = { "result": "ok" }



        ### Завершение перерыва
        if r.has_key("action") and rg("action") == 'relax-end':

            user = request.user
            user.profile.relax_status = False
            user.save()

            if working_relax.objects.filter(user=user,current=True).exists():
                ### Завершение перерыва
                current = working_relax.objects.filter(current=True,user=user).last()
                current.current = False
                current.save()


            response_data = { "result": "ok" }



        ### Добавление действия - события
        if r.has_key("action") and rg("action") == 'plus-event':
            comment = request.GET["comment"].strip()
            mark_id = int(request.GET["mark_id"],10)
            mark = marks.objects.get(pk=mark_id)
            user = request.user
            if working_time.objects.filter(user=user,current=True).exists():
                wt = working_time.objects.filter(user=user,current=True).last()
                working_log.objects.create(
                    user=user,
                    mark=mark,
                    working=wt,
                    comment=comment

                )

                count = working_log.objects.filter(mark=mark,user=user,working=wt).count()

                response_data = { "result": "ok", "count": count, "mark_id": mark_id }
            else:
                response_data = { "result": "error" }




        ### Первоначальное отображение событий или действий в карточке
        if r.has_key("action") and rg("action") == 'showcount':
            user = request.user
            if working_time.objects.filter(user=user,current=True).exists():
                wt = working_time.objects.filter(user=user,current=True).last()

                items = working_log.objects.filter(working=wt).values('mark').annotate(count=Count('mark'))

                response_data = {"result": "ok", "items": eval(str(items))}
            else:
                response_data = {"result": "error"}






    if request.method == "POST":


        data = eval(request.body)



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response


