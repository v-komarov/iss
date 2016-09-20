#coding:utf-8

from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore


from django.contrib.sessions.backends.signed_cookies import SessionStore

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from iss.monitor.models import events
from iss.localdicts.models import Status,Severity


class EventList(ListView):

    model = events
    template_name = "monitor/event_list.html"
    paginate_by = 50


    def dispatch(self, request, *args, **kwargs):
        self.session = request.session
        return super(ListView, self).dispatch(request, *args, **kwargs)



    def get_queryset(self):
        return events.objects.all().order_by('-update_time')


    def get_context_data(self, **kwargs):
        context = super(EventList, self).get_context_data(**kwargs)

        if self.session.has_key("status_id"):
            context['status'] = self.session['status_id']
        else:
            context['status'] = ""
        print context['status']

        return context

