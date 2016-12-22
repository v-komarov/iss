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
from iss.localdicts.models import accident_cats,accident_list,email_templates


cursor = connections["default"].cursor()
cursor.execute('SELECT DISTINCT manager FROM monitor_events')
managers = cursor.fetchall()





class EventList(ListView):

    model = events
    template_name = "monitor/event_list.html"

    paginate_by = 50


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='monitor',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)


    def my_fields_order(self):

        # Чередование полей
        pk_user = self.user.pk
        u = User.objects.get(pk=pk_user)
        if Profile.objects.filter(user=u).count() == 1:
            p = Profile.objects.get(user=u)
            data = p.settings
            if data.has_key("monitor-settings"):
                return data["monitor-settings"]["head_order"]
            else:
                return head_order
        else:
            return head_order



    ### Через сколько обновлять таблицу
    def my_refresh_table(self):

        pk_user = self.user.pk
        u = User.objects.get(pk=pk_user)
        if Profile.objects.filter(user=u).count() == 1:
            p = Profile.objects.get(user=u)
            data = p.settings
            if data.has_key("monitor-settings"):
                if data["monitor-settings"].has_key("refresh_data"):
                    return data["monitor-settings"]["refresh_data"]
                else:
                    return 0
            else:
                return 0
        else:
            return 0

    #### Сколько событий на странице
    def my_row_page_table(self):

        pk_user = self.user.pk
        u = User.objects.get(pk=pk_user)
        if Profile.objects.filter(user=u).count() == 1:
            p = Profile.objects.get(user=u)
            data = p.settings
            if data.has_key("monitor-settings"):
                if data["monitor-settings"].has_key("row_page_data"):
                    return data["monitor-settings"]["row_page_data"]
                else:
                    return 50
            else:
                return 50
        else:
            return 50


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
            data = events.objects.filter(agregation=False).order_by('-first_seen').select_related()[:1000]
        else:
            str_q = " & ".join(q)
            str_sql = "events.objects.filter(%s).filter(agregation=False).order_by('-first_seen').select_related()" % str_q

            data = (eval(str_sql))[:1000]


        #for i in data:
        #    i.field1 = eval(("i.%s") % (self.my_fields_order()[0]["name"]))


        return data










    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)

        # Статус
        if self.session.has_key('status_id'):
            status = pickle.loads(self.session['status_id'])
        else:
            status = [1,2,3]
            self.session['status_id'] = pickle.dumps(status)


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
            severity = [5,]
            self.session['severity_id'] = pickle.dumps(severity)

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
        context['head_order'] = self.my_fields_order()


        # Категории аварий
        context["accident_cats"] = accident_cats.objects.all().distinct('cat')

        # Вид аварии
        context["accident_list"] = accident_list.objects.all()


        ## Шаблоны сообщений
        context["email_templates"] = email_templates.objects.all()


        # Значение через сколько обновлять таблицу
        context["refresh_table"] = "%s" % self.my_refresh_table()


        # Сколько событий на странице
        context["row_page_table"] = "%s" % self.my_row_page_table()



        return context

