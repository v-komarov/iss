#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events,accidents
from iss.localdicts.models import address_house
from iss.equipment.models import devices_ip
from iss.inventory.models import devices,devices_type

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




## Для коммутаторов
devicetype = devices_type.objects.get(pk=1)




class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'




    def handle(self, *args, **options):

        ### Выбор аварий без acc_iss_id
        for ac in accidents.objects.filter(acc_iss_id=None):
            ev = ac.acc_event

            domen = ev.source


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


            houses = []
            #### Сбор id адресов
            #### Поиск устройств по ip адресам
            for ip in ipaddress:
                if devices.objects.filter(data__ipaddress=ip,data__domen=domen,device_type=devicetype).count() == 1:
                    ### Найден коммутатор в базе инвентори
                    dev = devices.objects.get(data__ipaddress=ip,data__domen=domen,device_type=devicetype)
                    if dev.address.house not in houses:
                        houses.append(dev.address.id)





            ### Дополнение из адресов , введеннх операторов
            for addrid in ac.acc_address["address_list"]:
                if int(addrid["addressid"],10) not in houses:
                    houses.append(int(addrid["addressid"],10))



            address_list = ""
            ### Формирование адресной строки
            q = []
            for addr in houses:
                q.append("Q(id=%s)" % addr)

            strsql = "address_house.objects.filter(%s)" % (" | ".join(q))
            data = eval(strsql)

            cities = []
            cityname = []
            for i in data:
                if i.city.id not in cities:
                    cities.append(i.city.id)
                    cityname.append(i.city.name)

            addr = []
            for i in data:
                addr.append(
                    {
                        'city':i.city,
                        'street':i.street,
                        'house':i.house
                    }

                )




            for city,street_house in itertools.groupby(addr,key=lambda x:x['city']):
                #address_list = address_list + "," + str(city) + ","
                for street,houses in itertools.groupby(list(street_house),key=lambda y:y['street']):
                    hl = ""
                    for h in list(houses):
                        a = "%s" % h["house"]
                        hl = hl + a + ","
                    address_list = address_list + str(city) +","+ str(street) + ",%s" % hl.encode("utf-8") + ";"


            address_list = address_list.replace(",;",";").replace("None","").replace(",,;",";")[:-1]
            # accname, acctype, acccat, acccomment, deviceidlist, addresslist, citynamelist
            #
            #

            values = {
                'date':ac.acc_start.astimezone(krsk_tz).strftime('%d.%m.%Y %H:%M'),
                'iss2_id':ac.id,
                'day':day,
                'accname':ac.acc_name,
                'acctypecat' : "%s,%s" % (ac.acc_type.name_short,ac.acc_cat.cat),
                'acccomment' : ac.acc_comment,
                'deviceidlist' : ",".join(iddevices),
                'citynamelist' : ",".join(cityname),
                'addresslist' : address_list.decode("utf-8")
            }

            value = ""
            value = value + "date(%s)%s[%s]" % (day,ac.acc_start.astimezone(krsk_tz).strftime('%d.%m.%Y %H:%M'),day)
            value = value + "iss2_id(%s)%s[%s]" % (day,ac.id,day)
            value = value + "accname(%s)%s[%s]" % (day,ac.acc_name.encode("cp1251"),day)
            value = value + "acctypecat(%s)%s,%s[%s]" % (day,ac.acc_type.name_short.encode("cp1251"),ac.acc_cat.cat.encode("cp1251"),day)
            value = value + "acccomment(%s)%s[%s]" % (day,ac.acc_comment.encode("cp1251"),day)
            value = value + "deviceidlist(%s)%s[%s]" % (day,",".join(iddevices),day)
            value = value + "citynamelist(%s)%s[%s]" % (day,",".join(cityname).encode("cp1251"),day)
            value = value + "addresslist(%s)%s" % (day,address_list.decode("utf-8").encode("cp1251"))





            data = json.dumps(values)

            req = urllib2.Request(url='http://10.6.3.7/departs/rcu/works/create_work_mss_post.php',data=value,headers={'Content-Type': 'text/plain; charset=cp1251'})
            f = urllib2.urlopen(req)
            result = f.read()
            start = result.find("[")
            end = result.find("]")

            id_iss = result[start + 1:end]
            ac.acc_iss_id = int(id_iss,10)
            ac.save()


            #print result

        print "ok"


