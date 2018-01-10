#coding:utf-8

import pickle

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from iss.mydecorators import group_required,anonymous_required

#from iss.working.models import works






class WorkList(ListView):


    #model = devices_ip
    template_name = "working/card.html"
    paginate_by = 100


    @method_decorator(login_required(login_url='/'))
    #@method_decorator(group_required(group='working',redirect_url='/mainmenu/'))
    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):



        return []








    def get_context_data(self, **kwargs):
        context = super(WorkList, self).get_context_data(**kwargs)


        if self.session.has_key('tz'):
            context['tz']= self.session['tz']
        else:
            context['tz']= 'UTC'


        # search
        if self.session.has_key('search'):
            context['search'] = self.session['search']
        else:
            context['search'] = ""


        return context



