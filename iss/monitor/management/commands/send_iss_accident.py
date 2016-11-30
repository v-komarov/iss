#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events,accidents
from iss.localdicts.models import address_house
from iss.equipment.models import devices_ip

import json
import time
import datetime
import binascii
from pytz import timezone


### Ключ для iss
day = "eed3eis9quei7ga9avievaegaaNieHui"


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'




    def handle(self, *args, **options):

        ### Выбор аварий без acc_iss_id
        for ac in accidents.objects.filter(acc_iss_id=None):
            ev = ac.acc_event

            ipaddress = [ev.device_net_address]
            if ev.data.has_key("containergroup"):
                for item in ev.data["containergroup"]:
                    a = events.objects.get(pk=item)
                    ipaddress.append(a.device_net_address)

            iddevices = []
            ### Поиск соответствия ip адресу id для iss
            for ip in ipaddress:
                if devices_ip.objects.filter(ipaddress=ip,device_domen="zenoss_krsk").count() == 1:
                    d = devices_ip.objects.get(ipaddress=ip,device_domen="zenoss_krsk")
                    if d.data.has_key("iss_id_device"):
                        iddevices.append("%s" % d.data["iss_id_device"])




            # accname, acctype, acccat, acccomment, deviceidlist
            #
            #

            values = {
                'date':ac.acc_start.astimezone(krsk_tz).strftime('%d.%m.%Y %H:%M'),
                'iss2_id':ac.id,
                'day':day,
                'accname':ac.acc_name.encode("cp1251"),
                'acctypecat' : "%s,%s" % (ac.acc_type.name,ac.acc_cat.name),
                'acccomment' : ac.acc_comment.encode("cp1251"),
                'deviceidlist' : ",".join(iddevices)
            }

            print values


            #req = urllib2.Request(url='http://127.0.0.1:5000/api/reports/accidents/references/',data=json.dumps({}),headers={'Content-Type': 'application/json'})

            #req = urllib2.Request(url='http://127.0.0.1:8000',data="",headers={'Content-Type': 'application/json'})
            #f = urllib2.urlopen(req)
            #result = f.read()

        print "ok"


