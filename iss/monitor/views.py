#coding:utf-8

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


from django.db import connections
from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from iss.monitor.models import events
from iss.localdicts.models import Status,Severity


cursor = connections["default"].cursor()
cursor.execute('SELECT DISTINCT manager FROM monitor_events')
managers = cursor.fetchall()





class EventList(ListView):

    model = events
    template_name = "monitor/event_list.html"
    paginate_by = 50


    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        #client_bind.objects.filter(Q(console_number=term) | Q(client_object__address_building__name__icontains=term))

        return events.objects.all().order_by('-update_time')


    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)

        # Статус
        if self.session.has_key('status_id'):
            status = self.session['status_id']
        else:
            status = "xxxxx"

        # Список статусов
        if status == "":
            status_list = ["<option value='xxxxx' selected>Все</option>"]
        else:
            status_list = ["<option value='xxxxx'>Все</option>"]
        for row in Status.objects.all().order_by("id"):
            if "%s" % row.id == status:
                status_list.append("<option value='%s' selected>%s</option>" % (row.id,row.name))
            else:
                status_list.append("<option value='%s'>%s</option>" % (row.id,row.name))

        context['status'] = status_list


        # Важность
        if self.session.has_key('severity_id'):
            severity = self.session['severity_id']
        else:
            severity = "xxxxx"

        # Список важности
        if severity == "":
            severity_list = ["<option value='xxxxx' selected>Все</option>"]
        else:
            severity_list = ["<option value='xxxxx'>Все</option>"]
        for row in Severity.objects.all().order_by("id"):
            if "%s" % row.id == severity:
                severity_list.append("<option value='%s' selected>%s</option>" % (row.id,row.name))
            else:
                severity_list.append("<option value='%s'>%s</option>" % (row.id,row.name))

        context['severity'] = severity_list


        # last_seen
        if self.session.has_key('last_seen'):
            context['last_seen'] = self.session['last_seen']
        else:
            context['last_seen'] = ""


        # first_seen
        if self.session.has_key('first_seen'):
            context['first_seen'] = self.session['first_seen']
        else:
            context['first_seen'] = ""


        # search
        if self.session.has_key('search'):
            context['search'] = self.session['search']
        else:
            context['search'] = ""


        # Manager
        if self.session.has_key('manager'):
            manager = self.session['manager']
        else:
            manager = "xxxxx"

        # Список manager
        if manager == "xxxxx":
            manager_list = ["<option value='xxxxx' selected>Все</option>"]
        else:
            manager_list = ["<option value='xxxxx'>Все</option>"]
        for row in managers:
            if row[0] == manager:
                manager_list.append("<option value='%s' selected>%s</option>" % (row[0],row[0]))
            else:
                manager_list.append("<option value='%s'>%s</option>" % (row[0],row[0]))

        context['manager'] = manager_list

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context

