#coding:utf-8

import pickle

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

import datetime
from pytz import timezone

from django.db import connections
from django.db.models import Q
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from iss.monitor.models import events
from iss.localdicts.models import Status,Severity

from iss.mydecorators import group_required,anonymous_required


from django.contrib.auth.models import User
from iss.monitor.models import Profile
from iss.monitor.jsondata import head_order



cursor = connections["default"].cursor()
cursor.execute('SELECT DISTINCT manager FROM monitor_events')
managers = cursor.fetchall()





class EventList(ListView):

    model = events
    template_name = "monitor/event_list.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='monitor',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):

        q = []
        if self.session.has_key("filtergroup"):
            q.append("Q(agregator=%s)" % True)

        if self.session.has_key("status_id"):
            if pickle.loads(self.session["status_id"]) != []:
                qs = []
                for s in pickle.loads(self.session["status_id"]):
                    qs.append("Q(status_id=Status.objects.get(pk=%s))" % s)
                q.append("("+" | ".join(qs)+")")

        if self.session.has_key("severity_id"):
            if pickle.loads(self.session["severity_id"]) != []:
                qv = []
                for v in pickle.loads(self.session["severity_id"]):
                    qv.append("Q(severity_id=Severity.objects.get(pk=%s))" % v)
                q.append("("+" | ".join(qv)+")")

        if self.session.has_key("manager"):
            if pickle.loads(self.session["manager"]) != []:
                qm = []
                for m in pickle.loads(self.session["manager"]):
                    qm.append("Q(manager='%s')" % m)
                q.append("("+" | ".join(qm)+")")

        if self.session.has_key("search"):
            if len(self.session['search']) >= 3:
                for search in self.session['search'].split(" "):
                    if search != " ":
                        q.append("(Q(device_net_address__icontains='%s') | Q(device_system__icontains='%s') | Q(device_group__icontains='%s') | Q(device_class__icontains='%s') | Q(device_location__icontains='%s') | Q(event_class__icontains='%s'))" % (search,search,search,search,search,search))

        if self.session.has_key("first_seen"):
            if self.session["first_seen"] != "":
                try:
                    q.append("Q(first_seen__gte='%s')" % datetime.datetime.strptime(self.session["first_seen"],"%d.%m.%Y").replace(tzinfo=timezone('UTC')))
                except:
                    pass

        if self.session.has_key("last_seen"):
            if self.session["last_seen"] != "":
                try:
                    q.append("Q(last_seen__lte='%s')" % datetime.datetime.strptime(self.session["last_seen"],"%d.%m.%Y").replace(tzinfo=timezone('UTC')))
                except:
                    pass

        if len(q) == 0:
            return events.objects.filter(agregation=False).order_by('-first_seen')[:1000]
        else:
            str_q = " & ".join(q)
            str_sql = "events.objects.filter(%s).filter(agregation=False).order_by('-first_seen')" % str_q

            return (eval(str_sql))[:1000]










    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)

        # Статус
        if self.session.has_key('status_id'):
            status = pickle.loads(self.session['status_id'])
        else:
            status = []

        # Список статусов
        status_list = []
        for row in Status.objects.all().order_by("id"):
            status_list.append("<option value='%s'>%s</option>" % (row.id, row.name))

        context['status'] = status_list
        context['selected_status'] = status



        # Важность
        if self.session.has_key('severity_id'):
            severity = pickle.loads(self.session['severity_id'])
        else:
            severity = []

        # Список важности
        severity_list = []
        for row in Severity.objects.all().order_by("id"):
            severity_list.append("<option value='%s'>%s</option>" % (row.id,row.name))

        context['severity'] = severity_list
        context['selected_severity'] = severity


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
            manager = pickle.loads(self.session['manager'])
        else:
            manager = []

        # Список manager
        manager_list = []
        for row in managers:
            manager_list.append("<option value='%s'>%s</option>" % (row[0],row[0]))

        context['manager'] = manager_list
        context['selected_manager'] = manager

        context['members'] = 0
        if self.session.has_key('containergroup'):

            g = events.objects.get(pk=self.session['containergroup'])
            data = g.data
            if data.has_key('containergroup'):
                context['members'] = len(data['containergroup'])
            context['containergroup'] = events.objects.get(pk=self.session['containergroup'])
        else:
            context['containergroup'] = False



        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'



        if self.session.has_key('filtergroup'):
            context["filtergroup"] = True
        else:
            context["filtergroup"] = False


        # Чередование полей
        pk_user = self.user.pk
        u = User.objects.get(pk=pk_user)
        if Profile.objects.filter(user=u) == 1:
            p = Profile.objects.get(user=u)
            data = p.data
            if data.has_key("monitor-settings"):
                context['head_order'] = data["monitor-settings"]["head_order"]
            else:
                context['head_order'] = head_order
        else:
            context['head_order'] = head_order



        return context

