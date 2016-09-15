#coding:utf-8

import iss.settings


def my_static_url(request):

    context = {'MY_STATIC_URL' : iss.settings.MY_STATIC_URL }

    return context

