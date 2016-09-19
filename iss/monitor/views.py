#coding:utf-8

from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db import connections
from django.http import HttpResponse
from django.views.generic import ListView
from iss.monitor.models import events


class EventList(ListView):

    model = events
    template_name = "monitor/event_list.html"


    def get_queryset(self):

        #return events.objects.filter(status_id=1)


        return events.objects.all()
