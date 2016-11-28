#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events,accidents
from iss.localdicts.models import address_house
from iss.equipment.models import devices_ip


import time
import datetime
import binascii
from pytz import timezone





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



            """
            ### Формирование id адресов
            idaddress = []
            if ac.acc_address.has_key("address_list"):
                for adr in ac.acc_address["address_list"]:
                    r = address_house.objects.get(pk=int(adr["addressid"],10))
                    city = r.city
                    street = r.street
                    house = r.house
                    ### Выбор всех адресов по совпадению
                    if street == None and house == None:
                        for j in address_house.objects.filter(city=city):
                            if j.iss_address_id:
                                idaddress.append(j.iss_address_id)
                    elif street != None and house == None:
                        for j in address_house.objects.filter(city=city,street=street):
                            if j.iss_address_id:
                                idaddress.append(j.iss_address_id)
                    elif street != None and house != None:
                        for j in address_house.objects.filter(city=city,street=street,house=house):
                            if j.iss_address_id:
                                idaddress.append(j.iss_address_id)

            """


            # accname, acctype, acccat, acccomment, deviceidlist
            #
            #

            values = {
                'accname':ac.acc_name,
                'acctypecat' : "%s,%s" % (ac.acc_type.name,ac.acc_cat.name),
                'acccomment' : ac.acc_comment,
                'deviceidlist' : ",".join(iddevices)
            }



        """
        url = 'http://10.6.0.22/'
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        print req.get_method()
        #response = urllib2.urlopen(req)
        #result = response.read()

        #print result
        """

        print "ok"


