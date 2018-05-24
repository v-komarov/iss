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

from iss.localdicts.models import address_city
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




