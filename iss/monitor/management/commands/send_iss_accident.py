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







### Перевод id городов ИСС2 к id городов Reports
id_city_2_reports = {

    "1" : {"iss2":"Абакан","idreports":14},
    "2": {"iss2": "Красноярск", "idreports": 21},
    "3": {"iss2": "Лесосибирск", "idreports": 22},
    "4": {"iss2": "Заозерный", "idreports": 18},
    "5": {"iss2": "Ачинск", "idreports": 15},
    "6": {"iss2": "Зеленогорск", "idreports": 19},
    "7": {"iss2": "Дивногорск", "idreports": 17},
    "8": {"iss2": "Минусинск", "idreports": 23},
    "9": {"iss2": "Бородино", "idreports": 16},
    "10": {"iss2": "Чернореченская", "idreports": 35},
    "11": {"iss2": "Тяжин", "idreports": 36},
    "12": {"iss2": "Солянка", "idreports": 37},
    "13": {"iss2": "Абакумовка", "idreports": 38},
    "14": {"iss2": "Боготол", "idreports": 32},
    "15": {"iss2": "Саянский", "idreports": 29},
    "16": {"iss2": "Аскиз", "idreports": 28},
    "17": {"iss2": "Козулька", "idreports": 39},
    "18": {"iss2": "Камарчага", "idreports": 40},
    "19": {"iss2": "Бугач", "idreports": 41},
    "20": {"iss2": "Бискамжа", "idreports": 42},
    "21": {"iss2": "Биркчул", "idreports": 43},
    "22": {"iss2": "Базаиха", "idreports": 44},
    "23": {"iss2": "Решоты", "idreports": 30},
    "24": {"iss2": "Мариинск", "idreports": 33},
    "25": {"iss2": "Кошурниково", "idreports": 20},
    "26": {"iss2": "Иланский", "idreports": 31},
    "27": {"iss2": "Уяр", "idreports": 34},
    "28": {"iss2": "Назарово", "idreports": 24},
    "29": {"iss2": "Черногорск", "idreports": 26},
    "30": {"iss2": "Большая Кеть", "idreports": 45},
    "31": {"iss2": "Новобирюсинск", "idreports": 46},
    "32": {"iss2": "Чунояр", "idreports": 47},
    "33": {"iss2": "Тамтачет", "idreports": 48},
    "34": {"iss2": "Овсянка", "idreports": 49},
    "35": {"iss2": "Канск", "idreports": 27},
    "36": {"iss2": "Кильчуг", "idreports": 50},
    "37": {"iss2": "Железногорск", "idreports": 51},
    "38": {"iss2": "Новоенисейск", "idreports": 25},
    "39": {"iss2": "Слизнево", "idreports": 52},
    "40": {"iss2": "Курагино", "idreports": 53},
    "41": {"iss2": "Щетинкино", "idreports": 54},
    "42": {"iss2": "Карабула", "idreports": 55},
    "43": {"iss2": "Пихтовая", "idreports": 56},
    "44": {"iss2": "Сосновоборск", "idreports": 57},
    "45": {"iss2": "Ужур", "idreports": 58},
    "46": {"iss2": "Нижняя Пойма", "idreports": 59},
    "47": {"iss2": "Суриково", "idreports": 60},
    "48": {"iss2": "Зерцалы", "idreports": 61},
    "49": {"iss2": "Абаза", "idreports": 62},
    "50": {"iss2": "Дубинино", "idreports": 63},
    "51": {"iss2": "Мана", "idreports": 64}

}






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




        req = urllib2.Request(url='http://127.0.0.1:5000/api/reports/accidents/references/',data=json.dumps({}),headers={'Content-Type': 'application/json'})

        #req = urllib2.Request(url='http://127.0.0.1:8000',data="",headers={'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        result = f.read()

        data = json.loads(result)
        for key in data["api_response"]["companies"].keys():
            print key,data["api_response"]["companies"][key]

        print "ok"


