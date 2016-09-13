#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect




import iss.settings

@csrf_protect
def Begin(request):

    c = RequestContext(request, {"ROOT_URL":iss.settings.ROOT_URL})
    return render_to_response("index.html",c)
