#coding:utf-8

import pickle

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required
from django.views.generic.base import TemplateView,RedirectView







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

        return context









