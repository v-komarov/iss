#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q
from django import template


from iss.monitor.models import events,accidents
from iss.localdicts.models import address_house,address_templates
from iss.equipment.models import devices_ip
from iss.inventory.models import devices

import itertools
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


    def check(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("SKIPPING SYSTEM CHECKS!\n"))



    def handle(self, *args, **options):

        ### Выбор аварий без acc_iss_id
        #for ac in accidents.objects.filter(pk=116):

        for ac in accidents.objects.filter(acc_iss_id=None):
            ip_list = ac.get_event_ip_list()
            #ip_list = ['55.49.4.75','55.49.8.68','55.49.11.41','55.21.13.81','55.21.20.74']

            addrjson = ac.acc_addr_dict["address_list"]

            ### Формирование списка городов
            cities = []
            for item in addrjson["address_list"]:
                if item["city"].encode("cp1251") not in cities:
                    cities.append(item["city"].encode("cp1251"))

            templ = address_templates.objects.get(name="accidentname").template
            t = template.Template(templ)
            c = template.Context({'data': addrjson["address_list"]})
            address_list = t.render(c)

            #
            #

            value = ""
            value = value + "type_query(%s)create_work[%s]" % (day,day)
            value = value + "date(%s)%s[%s]" % (day,ac.acc_start.astimezone(krsk_tz).strftime('%d.%m.%Y %H:%M'),day)
            value = value + "iss2_id(%s)%s[%s]" % (day,ac.id,day)
            value = value + "accname(%s)%s[%s]" % (day,ac.acc_name.encode("cp1251"),day)
            value = value + "acctypecat(%s)%s,%s[%s]" % (day,ac.acc_type.name_short.encode("cp1251"),ac.acc_cat.cat.encode("cp1251"),day)
            value = value + "acccomment(%s)%s[%s]" % (day,ac.acc_comment.encode("cp1251"),day)
            value = value + "iplist(%s)%s[%s]" % (day,",".join(map(lambda ip: ip.encode("cp1251"),ip_list)), day)
            value = value + "citynamelist(%s)%s[%s]" % (day,",".join(cities),day)
            value = value + "addresslist(%s)%s[%s]" % (day,address_list.decode("utf-8").encode("cp1251"),day)
            value = value + "reason(%s)%s" % (day, ac.acc_reason.encode("cp1251"))

            #print value.decode("cp1251")

            req = urllib2.Request(url='http://10.6.3.77:8080/departs/rcu/works/create_work_mss_post.php',data=value,headers={'Content-Type': 'text/plain; charset=cp1251'})
            f = urllib2.urlopen(req)
            result = f.read()
            start = result.find("[")
            end = result.find("]")

            id_iss = result[start + 1:end]
            ac.acc_iss_id = int(id_iss,10)
            ac.save()

            #print result

        print "ok"


