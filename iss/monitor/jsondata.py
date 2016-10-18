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

from iss.monitor.models import events
from iss.localdicts.models import Severity,Status






def get_json(request):

    response_data = {}

    if request.method == "GET":

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

        ### Показывать только группировки
        if r.has_key("filtergroup") and rg("filtergroup") != '':
            if request.session.has_key("filtergroup"):
                del request.session['filtergroup']
            else:
                request.session['filtergroup'] = "ok"

        if r.has_key("containergroup") and rg("containergroup") != '':
            if request.GET["containergroup"] == "_____":
                del request.session['containergroup']
            else:
                request.session['containergroup'] = request.GET["containergroup"]


        # Добавление в группировку (контейнер)
        if r.has_key("addgroup") and rg("addgroup") != '[]':
            container_row = request.GET["container_row"]
            id_group = eval(request.GET["addgroup"])
            g = []
            for item in id_group:
                if container_row != item:
                    g.append(item)
                    i = events.objects.get(pk=item)
                    i.agregation = True
                    #i.agregator = False
                    i.data['containergroup'] = []
                    i.save()
            e = events.objects.get(pk=container_row)
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
            container_row = request.GET["container_row"]
            tz = request.session['tz']
            e = events.objects.get(pk=container_row)
            l = e.data['containergroup']
            a = []
            for item in l:
                i = events.objects.get(pk=item)
                if i.byhand == True:
                    byhand = "yes"
                else:
                    byhand = "no"
                if i.agregator == True:
                    agregator = "yes"
                else:
                    agregator = "no"
                if i.bymail == True:
                    bymail = "yes"
                else:
                    bymail = "no"

                a.append(
                    {
                        'id':i.id,
                        'dateorder':time.mktime(i.last_seen.timetuple()),
                        'uuid':i.uuid,
                        'first_seen':i.first_seen.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M %Z"),
                        'last_seen':i.last_seen.astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M %Z"),
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
                        'element_sub_identifier':i.element_sub_identifier,
                        'byhand':byhand,
                        'agregator':agregator,
                        'bymail':bymail,
                        'summary':i.summary
                    }
                )

            a = sorted(a, key=operator.itemgetter('dateorder'),reverse=True)
            response_data['members'] = a



        # Удаление из группировки
        if r.has_key("delgroup") and rg("delgroup") != '[]':
            container_row = request.GET["container_row"]
            id_group = eval(request.GET["delgroup"])
            e = events.objects.get(pk=container_row)
            l = e.data['containergroup']
            for item in id_group:
                if item != container_row:
                    i=l.index(item)
                    del l[i]
                    a = events.objects.get(pk=item)
                    a.agregation = False
                    a.save()
                    del item

            e.data['containergroup'] = l
            e.save()


        # Данные по событию для отображения в форме
        if r.has_key("getevent") and rg("getevent") != '':
            tz = request.session['tz']
            id_event = request.GET["getevent"]
            e = events.objects.get(pk=id_event)
            data = {
                'id':e.id,
                'event_class':e.event_class,
                'severity':e.severity_id.id,
                'device_system':e.device_system,
                'device_group':e.device_group,
                'device_class':e.device_class,
                'device_net_address':e.device_net_address,
                'device_location':e.device_location,
                'element_identifier':e.element_identifier,
                'element_sub_identifier':e.element_sub_identifier,
                'status':e.status_id.id
            }

            list_mail = []

            # Если событие на основе почтового сообщения, то отправляем список почтовых сообщений
            if e.bymail == True:
                for m in e.data["mails"]:
                    d = datetime.datetime.fromtimestamp(email.utils.mktime_tz(parsedate_tz(m["mail_date"])))
                    list_mail.append({
                        'id_mail':m["mail_id"].replace(">","").replace("<",""),
                        'label_mail':m["mail_from"].replace(">","").replace("<","")+" ("+d.replace(tzinfo=timezone("UTC")).astimezone(timezone(tz)).strftime("%d.%m.%Y %H:%M:%S")+")"
                    })

                data["list_mail"] = list_mail

            response_data = data



        ## Содержание письма
        if r.has_key("getmail") and rg("getmail") != '':

            data = {}
            id_event = request.GET["event_id"]
            id_mail = request.GET["mail_id"]
            e = events.objects.get(pk=id_event)
            for m in e.data["mails"]:
                if m["mail_id"] == u"<%s>" % id_mail:
                    files = []
                    for a in m["attachment"]:
                        files.append(a["file_name"])
                    data = {
                        'subject':m["subject"],
                        'body':m["mail_body"],
                        'files':files
                    }

            response_data = data




    if request.method == "POST":
        data = eval(request.body)

        print data

        if data.has_key("action") and data["action"] == 'create_event':

            now = datetime.datetime.now(timezone('UTC'))
            source = request.user.username

            events.objects.create(
                source = source,
                datetime_evt = now,
                first_seen = now,
                update_time = now,
                last_seen = now,
                event_class = data["event_class"],
                severity_id = Severity.objects.get(pk=data["severity"]),
                manager = 'operator',
                device_system = data["device_system"],
                device_group = data["device_group"],
                device_class = data["device_class"],
                device_net_address = data["device_net_address"],
                device_location = data["device_location"],
                element_identifier = data["element_identifier"],
                element_sub_identifier = data["element_sub_identifier"],
                status_id = Status.objects.get(pk=data["status"]),
                byhand = True

            )

        if data.has_key("action") and data["action"] == 'edit_event':
            now = datetime.datetime.now(timezone('UTC'))
            #source = request.user.username

            e = events.objects.get(pk=data['event_id'])
            e.update_time = now
            e.last_seen = now
            e.event_class = data["event_class"]
            e.severity_id = Severity.objects.get(pk=data["severity"])
            e.device_system = data["device_system"]
            e.device_group = data["device_group"]
            e.device_class = data["device_class"]
            e.device_net_address = data["device_net_address"]
            e.device_location = data["device_location"]
            e.element_identifier = data["element_identifier"]
            e.element_sub_identifier = data["element_sub_identifier"]
            e.status_id=Status.objects.get(pk=data["status"])
            e.save()


    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response

