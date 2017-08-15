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
from django.contrib.auth.models import User


from iss.mydecorators import group_required, anonymous_required

from iss.exams.models import questions




### Список вопросов
class QuestionsList(ListView):

    model = questions
    template_name = "exams/questions_list.html"

    paginate_by = 100



    @method_decorator(login_required(login_url='/'))
    @method_decorator(group_required(group='exams',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.session = request.session
        self.user = request.user
        return super(ListView, self).dispatch(request, *args, **kwargs)





    def get_queryset(self):

        data = questions.objects.order_by('name')

        return data







    def get_context_data(self, **kwargs):
        context = super(QuestionsList, self).get_context_data(**kwargs)

        context['tz']= self.session['tz'] if self.session.has_key('tz') else 'UTC'


        return context



