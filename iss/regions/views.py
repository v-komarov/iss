#coding:utf-8

import pickle
import operator

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

import datetime
from pytz import timezone

from django.db import connections
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView,RedirectView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from iss.localdicts.models import regions, address_city
from iss.regions.models import orders, reestr, proj, proj_stages, reestr_proj
from iss.regions.forms import ProjForm, ProjForm2, StageForm, ReestrProjCreateForm, ReestrProjUpdateForm

from iss.mydecorators import group_required,anonymous_required



#message_type_first = MessageType.objects.get(pk=1)
#message_status_first = MessageStatus.objects.get(pk=1)



### Заказы
class Orders(ListView):

    model = orders
    template_name = "regions/orders.html"

    paginate_by = 0



    #@method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


            return []







    def get_context_data(self, **kwargs):
        context = super(Orders, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['regions_list'] = regions.objects.order_by('name')



        return context





### Реестр
class Reestr(ListView):

    model = reestr
    template_name = "regions/reestr.html"

    paginate_by = 100



    #@method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        if self.session.has_key("filter-city-reestr") and self.session.has_key("filter-region-reestr"):
            region = regions.objects.get(pk=int(self.session["filter-region-reestr"], 10))
            city = address_city.objects.get(pk=int(self.session["filter-city-reestr"], 10))
            return reestr.objects.filter(region=region,city=city).order_by('invnum', 'name')

        elif self.session.has_key("filter-city-reestr") == False and self.session.has_key("filter-region-reestr"):
            region = regions.objects.get(pk=int(self.session["filter-region-reestr"], 10))
            return reestr.objects.filter(region=region).order_by('city__name', 'invnum', 'name')

        elif self.session.has_key("filter-city-reestr") and self.session.has_key("filter-region-reestr") == False :
            city = address_city.objects.get(pk=int(self.session["filter-city-reestr"], 10))
            return reestr.objects.filter(city=city).order_by('region__name', 'invnum', 'name')

        else:

            return reestr.objects.order_by('region__name', 'city__name', 'invnum', 'name')







    def get_context_data(self, **kwargs):
        context = super(Reestr, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['regions_list'] = regions.objects.order_by('name')
        context['cities_list'] = address_city.objects.order_by('name')

        context['region'] = self.session["filter-region-reestr"] if self.session.has_key("filter-region-reestr") else "0"
        context['city'] = self.session["filter-city-reestr"] if self.session.has_key("filter-city-reestr") else "0"


        return context




### Редактировать строку реестра
@method_decorator(login_required(login_url='/'), name='dispatch')
@method_decorator(group_required(group='reestr', redirect_url='/regions/reestr/page/1/'), name='dispatch')
class ReestrUpdate(UpdateView):
    model = reestr
    fields = ['region', 'god_balans', 'original', 'net', 'city', 'project_code', 'invnum', 'start_date', 'ed_os', 'name', 'comcode', 'serial', 'nomen', 'ed', 'count', 'price', 'actos1', 'group', 'age', 'address', 'dwdm', 'tdm', 'sdh', 'ip', 'atm', 'emcs', 'res_count', 'res_serial', 'res_invnum']
    success_url = '/regions/reestr/page/1/'
    template_name = "regions/edit_reestr.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.get_username() + " (" + self.request.user.get_full_name() + ")"
        form.instance.rowsum = form.instance.price * form.instance.count
        return super(ReestrUpdate, self).form_valid(form)




### Добавить позицию реестра
@method_decorator(login_required(login_url='/'), name='dispatch')
@method_decorator(group_required(group='reestr', redirect_url='/regions/reestr/page/1/'), name='dispatch')
class ReestrCreate(CreateView):
    model = reestr
    fields = ['region', 'god_balans', 'original', 'net', 'city', 'project_code', 'invnum', 'start_date', 'ed_os',
              'name', 'comcode', 'serial', 'nomen', 'ed', 'count', 'price', 'actos1', 'group', 'age', 'address',
              'dwdm', 'tdm', 'sdh', 'ip', 'atm', 'emcs', 'res_count', 'res_serial', 'res_invnum']
    success_url = '/regions/reestr/page/1/'
    template_name = "regions/edit_reestr.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.get_username() + " (" + self.request.user.get_full_name() + ")"
        form.instance.rowsum = form.instance.price * form.instance.count
        return super(ReestrCreate, self).form_valid(form)









### Проекты (список)
class ProjList(ListView):

    model = proj
    template_name = "regions/projlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = proj.objects.order_by('-datetime_create')

        return data







    def get_context_data(self, **kwargs):
        context = super(ProjList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form']= ProjForm()


        return context







### Этапы проекта (список)
class ProjStagesList(ListView):

    model = proj_stages
    template_name = "regions/projstageslist.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        request.session["proj_id"] = kwargs.get('project')
        self.request = request
        self.session = request.session
        self.user = request.user
        self.proj = proj.objects.get(pk=int(self.session["proj_id"], 10))
        self.actions = []
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = proj_stages.objects.filter(proj=self.proj)

        ### Вычисление пунктов исполнения
        rows = self.proj.make_dict()
        G = self.proj.make_graph(rows)
        G = self.proj.graph_edge_order(G, rows)
        self.actions = self.proj.actions(G)

        for item in data:
            item.order = ".".join(["%s" % x for x in item.stage_order])
            item.depend = ".".join(["%s" % x for x in item.depend_on["stages"]])
            item.action = True if item.id in self.actions else False


        return data







    def get_context_data(self, **kwargs):
        context = super(ProjStagesList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form']= ProjForm2(instance=self.proj)
        context['user_list']= User.objects.order_by('first_name')
        context['stageform']= StageForm()
        context['project']= self.session["proj_id"]

        ### Вычисление пунктов исполнения
        context['actions'] = self.actions



        return context





### Задачи исполнителей
class TaskList(ListView):

    model = proj_stages
    template_name = "regions/workertask.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        begin = self.session['begin_date'] if self.session.has_key('begin_date') else datetime.datetime.today() - datetime.timedelta(days=30)
        end = self.session['end_date'] if self.session.has_key('end_date') else datetime.datetime.today() + datetime.timedelta(days=30)

        data = proj_stages.objects.filter( (Q(begin__gte=begin) & Q(end__lte=end)) | (Q(begin__gte=begin) & Q(begin__lte=end)) | (Q(end__gte=begin) & Q(end__lte=end)) ).order_by('-begin')

        data2 = []
        if self.session.has_key('user_id'):
            u = User.objects.get(pk=self.session['user_id'])
            for i in data:
                if u in i.workers.all():
                    data2.append(i)
            return data2
        else:

            return data







    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['begin_date'] = self.session['begin_date'] if self.session.has_key('begin_date') else datetime.datetime.today() - datetime.timedelta(days=30)
        context['end_date'] = self.session['end_date'] if self.session.has_key('end_date') else datetime.datetime.today() + datetime.timedelta(days=30)
        context['user_id'] = self.session['user_id'] if self.session.has_key('user_id') else ""
        context['user_list'] = User.objects.order_by('first_name')

        return context







### реестр проектов (таблица - список)
class ReestrProjList(ListView):



    model = reestr_proj
    template_name = "regions/reestrproj/reestrprojlist.html"

    paginate_by = 100



    #@method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

            data = reestr_proj.objects.order_by("-id")

            return data






    def get_context_data(self, **kwargs):
        context = super(ReestrProjList, self).get_context_data(**kwargs)
        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form'] = ReestrProjCreateForm()

        return context






"""
### Добавление реестра проекта
class ReestrProjAdd(CreateView):
    model = reestr_proj
    fields = ['proj_kod','region','proj_name']
    success_url = '/regions/reestrproj/page/1/'
    template_name = "regions/reestrproj/reestrprojadd.html"



    def form_valid(self, form):
        form.instance.author = self.request.user
        #form.instance.rowsum = form.instance.price * form.instance.count
        return super(ReestrProjAdd, self).form_valid(form)
"""




### Изменение реестра проекта
class ReestrProjEdit(UpdateView):
    model = reestr_proj
    form_class = ReestrProjUpdateForm
    template_name = "regions/reestrproj/reestrprojedit.html"
    success_url = '/regions/reestrproj/reestrproj/edit/1/'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ReestrProjEdit, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ReestrProjEdit, self).get_context_data(**kwargs)
        context["proj"] = self.get_object()
        return context


    def form_valid(self, form):
        #form.instance.rowsum = form.instance.price * form.instance.count
        return super(ReestrProjEdit, self).form_valid(form)
