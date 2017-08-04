#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q
from django import template


from iss.localdicts.models import cal

import json
from pytz import timezone



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)





class Command(BaseCommand):
    args = '<...>'
    help = 'getting cal'



    def handle(self, *args, **options):

        req = urllib2.Request(url='http://basicdata.ru/api/json/calend/')
        f = urllib2.urlopen(req)
        result = f.read()

        cal.objects.create(year='2017',cal=json.loads(result)["data"]["2017"])

        #print json.loads(result)["data"]["2017"]



