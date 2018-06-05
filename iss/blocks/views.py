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


from iss.mydecorators import group_required,anonymous_required

from iss.localdicts.models import address_city, address_house
from iss.blocks.models import buildings, block_managers








### Список домов
class BlocksList(ListView):



    model = buildings
    template_name = "blocks/blockslist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = block_managers.objects.order_by("name")

        return data



    def get_context_data(self, **kwargs):
        context = super(BlocksList, self).get_context_data(**kwargs)
        context["city"] = address_city.objects.order_by("name")


        return context







### Список возможных адресов
class AddressList(ListView):



    model = buildings
    template_name = "blocks/addresslist.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='project',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        if self.session.has_key("filter_addresslist"):

            filter_value = pickle.loads(self.session["filter_addresslist"])

            data = address_house.objects.exclude(city=None).exclude(street=None).exclude(house=None).order_by('city','street','house')
            data = data.filter(city_id=int(filter_value["city"],10)) if filter_value["city"] != "" else data
            data = data.filter(street__name__icontains=filter_value["street"]) if filter_value["city"] != "" else data
            data = data.filter(house__icontains=filter_value["house"]) if filter_value["house"] != "" else data

            return data

        else:

            return []



    def get_context_data(self, **kwargs):
        context = super(AddressList, self).get_context_data(**kwargs)
        context["city"] = address_city.objects.order_by("name")
        context["filter"] = pickle.loads(self.session["filter_addresslist"]) if self.session.has_key("filter_addresslist") else {'city': "", 'street': "", "house": ""}

        return context




