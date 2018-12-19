#coding:utf-8

import pickle
import datetime

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.views.generic.base import TemplateView,RedirectView
from django.utils.timezone import now

from iss.working.models import marks, working_time, working_log, working_reports
from iss.working.forms  import phonefilter
from iss.working.cassandratools import phone1history



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip







class WorkCard(TemplateView):


    template_name = "working/card.html"


    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='working',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(WorkCard, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(WorkCard, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        context['work_status'] = self.user.profile.work_status
        context['relax_status'] = self.user.profile.relax_status
        context['marks_table'] = marks.objects.filter(visible=True).order_by('order')

        return context







### Подготовка отчетов
class MakeReports(ListView):



    #model = reestr_proj
    template_name = "working/makereports.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='working',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = working_time.objects.order_by('-datetime_begin')

        if self.session.has_key("worker"):
            worker_id = self.session["worker"]
            data = data.filter(user_id=worker_id)

        return data






    def get_context_data(self, **kwargs):
        context = super(MakeReports, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['include_report'] = pickle.loads(self.session["include_report"]) if self.session.has_key("include_report") else []
        context["users"] = working_log.objects.filter(datetime_create__gte=(now() - datetime.timedelta(days=90))).order_by("user__first_name").distinct("user__first_name","user__last_name")
        context["worker"] = self.session["worker"] if self.session.has_key("worker") else ""


        return context








### Логи смены
class Events(ListView):



    #model = reestr_proj
    template_name = "working/events.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='working',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        request.session['events_id'] = kwargs.get('pk')
        self.request = request
        self.session = request.session
        self.user = request.user

        self.working = working_time.objects.get(pk=request.session['events_id'])

        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = self.working.working_log_set.order_by("-datetime_create")

        return data






    def get_context_data(self, **kwargs):
        context = super(Events, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['user'] = self.working.user
        context['worktime'] = self.working.get_work_hour()
        context['relaxtime'] = self.working.get_relax_min()
        context['events'] = self.working.working_log_set.count()


        return context






### Отчеты
class Reports(ListView):



    #model = reestr_proj
    template_name = "working/reports.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='working',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = working_reports.objects.order_by("-datetime_create")

        return data






    def get_context_data(self, **kwargs):
        context = super(Reports, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'


        return context







class StartDesktop(TemplateView):


    template_name = "working/start_desktop.html"


    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='working',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(StartDesktop, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(StartDesktop, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        ip = get_client_ip(self.request)
        prof = self.user.profile
        prof.ip = ip
        prof.save()

        context['ip'] = ip

        return context









class PhoneHistory(TemplateView):


    template_name = "working/phone.html"


    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(PhoneHistory, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(PhoneHistory, self).get_context_data(**kwargs)

        context['form'] = phonefilter(initial={})

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        return context






#### Отображение графиков
class GraphHistory(TemplateView):


    template_name = "working/graph.html"


    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='working', redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(GraphHistory, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(GraphHistory, self).get_context_data(**kwargs)


        context["events"] = marks.objects.filter(visible=True).order_by('order')
        context["users"] = working_log.objects.filter(datetime_create__gte=(now() - datetime.timedelta(days=90))).order_by("user__first_name").distinct("user__first_name","user__last_name")


        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'





        return context






### Отчет по телефонным вызовам группы 1
class PhoneHistory1(ListView):



    #model = reestr_proj
    template_name = "working/phonehistory1.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='working',redirect_url='/begin/access-refused/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = []

        return data






    def get_context_data(self, **kwargs):
        context = super(PhoneHistory1, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'

        context['df'] = phone1history()

        return context



