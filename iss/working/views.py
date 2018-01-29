#coding:utf-8

import pickle

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.views.generic.base import TemplateView,RedirectView


from iss.working.models import marks, working_time, working_log, working_reports




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

        return data






    def get_context_data(self, **kwargs):
        context = super(MakeReports, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['include_report'] = pickle.loads(self.session["include_report"]) if self.session.has_key("include_report") else []

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

        ip = self.request.META.get('REMOTE_ADDR')
        prof = self.user.profile
        prof.ip = ip
        prof.save()

        context['ip'] = ip

        return context
