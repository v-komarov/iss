#coding:utf-8

import iss.settings
from iss.localdicts.models import TzList


def my_static_url(request):

    context = {'MY_STATIC_URL' : iss.settings.MY_STATIC_URL }

    return context


def user_tz(request):


    if request.user.is_authenticated():

       context = {
           'MY_USER_NAME' : request.user.get_full_name(),
           'MY_USER_TZ' : request.session["timezone"],
           'MY_USER_TZ_NAME' : TzList.objects.get(tz_id=request.session["timezone"]),
       }

    else:
        context = {
            'MY_USER_NAME': '',
            'MY_USER_TZ': '',
            'MY_USER_TZ_NAME': '',
        }

    return context
