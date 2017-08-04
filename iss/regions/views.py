#coding:utf-8

import pickle

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



from iss.localdicts.models import regions, address_city, InOut, MessageType, MessageStatus
from iss.regions.models import orders, reestr, messages, proj, proj_stages
from iss.regions.forms import MessageForm, ProjForm

from iss.mydecorators import group_required,anonymous_required



message_type_first = MessageType.objects.get(pk=1)
message_status_first = MessageStatus.objects.get(pk=1)



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












### Документооборот
class DocsList(ListView):

    model = orders
    template_name = "regions/docs_list.html"

    paginate_by = 0



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):


        data = messages.objects.filter(user=self.user).order_by('-datetime_update')

        for x in data:
            if x.user == self.user:
                x.inout = u'Исходящее'
                x.inout_id = 1
            else:
                x.inout = u'Входящее'
                x.inout_id = 2



        return data







    def get_context_data(self, **kwargs):
        context = super(DocsList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['inout'] = InOut.objects.order_by('name')
        context['message_type'] = MessageType.objects.order_by('name')
        context['message_status'] = MessageStatus.objects.order_by('name')

        context['inout_value'] = self.session['inout_value'] if self.session.has_key('inout_value') else "0"
        context['message_type_value'] = self.session['message_type_value'] if self.session.has_key('message_type_value') else "0"
        context['message_status_value'] = self.session['message_status_value'] if self.session.has_key('message_status_value') else "0"


        return context





### Редактирование и наполнение данными сообщения
class DocsUpdate(TemplateView):

    template_name = 'regions/docs_data.html'
    action = 'update'

    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user


        return super(DocsUpdate, self).dispatch(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super(DocsUpdate, self).get_context_data(**kwargs)

        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'

        if self.action == 'create':
            m = messages.objects.create(user=self.user, message_type=message_type_first, status=message_status_first)
            context['message_id'] = m.id
        else:
            m = messages.objects.get(pk=int(self.session['message_id'], 10))
            context['message_id'] = self.session['message_id']

        if m.user == self.user:
            context['access'] = 'owner'
        else:
            context['access'] = 'public'

        form = MessageForm(instance=m)
        form.fields['status'].widget.attrs['disabled'] = True
        context['form'] = form


        return context














### Проекты (список)
class ProjList(ListView):

    model = proj
    template_name = "regions/projlist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
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
    #@method_decorator(group_required(group='inventory',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        self.proj = proj.objects.get(pk=int(self.session["proj_id"], 10))
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = proj_stages.objects.filter(proj=self.proj).order_by('order')
        for item in data:
            item.steps = []
            for row in item.proj_steps_set.all().order_by('order'):
                item.steps.append(row)

        print data

        return data







    def get_context_data(self, **kwargs):
        context = super(ProjStagesList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['form']= ProjForm()


        return context

