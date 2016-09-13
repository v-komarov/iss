#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect


import iss.settings


class Begin(TemplateView):

    template_name = "index.html"

    @csrf_protect
    def get_context_data(self, **kwargs):
        context = super(Begin, self).get_context_data(**kwargs)
        context['STATIC_URL'] = iss.settings.STATIC_URL
        return context


    def get(self, request, *args, **kwargs):
        c = {}
        return render_to_response(self.template_name, c)

