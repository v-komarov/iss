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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import TemplateView,RedirectView



from iss.localdicts.models import regions, address_city
from iss.regions.models import orders, reestr

from iss.mydecorators import group_required,anonymous_required



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

    model = orders
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


        return reestr.objects.order_by('region__name')







    def get_context_data(self, **kwargs):
        context = super(Reestr, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['regions_list'] = regions.objects.order_by('name')
        context['cities_list'] = address_city.objects.order_by('name')



        return context






### Отгруженное оборудование
class Shipped(ListView):

    model = orders
    template_name = "regions/orders.html"

    paginate_by = 100



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
        context = super(Shipped, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'
        context['regions_list'] = regions.objects.order_by('name')



        return context

