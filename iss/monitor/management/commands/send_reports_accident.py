#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events,accidents
from iss.localdicts.models import address_house
from iss.equipment.models import devices_ip
from iss.inventory.models import devices,devices_type

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





### Перевод id вида аварии ИСС2 в id reports
id_kinds_2_reports = {
    "1" : {"iss2": "Л1", "idreports":1},
    "2": {"iss2": "С1", "idreports": 2},
    "3": {"iss2": "С2", "idreports": 3},
    "4": {"iss2": "С3", "idreports": 4},
    "5": {"iss2": "С4", "idreports": 5},
    "6": {"iss2": "С5", "idreports": 6},
    "7": {"iss2": "И1", "idreports": 7},
    "8": {"iss2": "З1", "idreports": 8},
    "9": {"iss2": "З2", "idreports": 9}
}




## Для коммутаторов
devicetype = devices_type.objects.get(pk=1)




tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)

utc = timezone("UTC")


class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'




    def handle(self, *args, **options):

        ### Выбор аварий без acc_reports_id
        for ac in accidents.objects.order_by("-update_datetime")[:3]:
            ev = ac.acc_event

            domen = ev.source


            ####
            companies = []
            cities = []
            houses = []
            address_str = ""
            zkl = 0


            #### Выбор ip адресов
            ipaddress = [ev.device_net_address]
            if ev.data.has_key("containergroup"):
                for item in ev.data["containergroup"]:
                    a = events.objects.get(pk=item)
                    ipaddress.append(a.device_net_address)
            #### Поиск устройств по ip адресам
            for ip in ipaddress:
                if devices.objects.filter(data__ipaddress=ip,data__domen=domen,device_type=devicetype).count() == 1:
                    ### Найден коммутатор в базе инвентори
                    dev = devices.objects.get(data__ipaddress=ip,data__domen=domen,device_type=devicetype)
                    if dev.company.id not in companies:
                        companies.append(dev.company.id)
                    if dev.address.city.id not in cities:
                        cities.append(dev.address.city.id)
                    if dev.address.house not in houses:
                        houses.append(dev.address.id)





            ### Дополнение из адресов , введеннх операторов
            for addrid in ac.acc_address["address_list"]:
                if int(addrid["addressid"],10) not in houses:
                    houses.append(int(addrid["addressid"],10))



            ### Формирование адресной строки
            for addrid in houses:
                a = address_house.objects.get(pk=addrid)
                if a.street == None and a.house == None:
                    address_str = address_str + "%s," % (a.city.name)
                elif a.house == None:
                    address_str = address_str + "%s: %s," % (a.city.name,a.street.name)
                else:
                    address_str = address_str + "%s: %s: %s," % (a.city.name,a.street.name,a.house)



            ### Расчет ЗКЛ на основе списка ip
            for addrid in houses:
                a = address_house.objects.get(pk=addrid)
                d = devices.objects.filter(address=a)
                for i in d:
                    if i.data["ipaddress"] not in ipaddress:
                        ipaddress.append(i.data["ipaddress"])

            for ip in ipaddress:
                for d in devices_ip.objects.filter(device_domen=domen,ipaddress=ip):
                    if d.data.has_key("ports_info"):
                        zkl = zkl + d.data["ports_info"]["used"]


            ### Преобразование id в reports для городов
            ci = []
            for c in cities:
                ci.append(id_city_2_reports["%s" % c]["idreports"])


            values = {
                'companies':companies,
                'cities':ci,
                'start_datetime':time.mktime(ac.acc_start.replace(tzinfo=timezone('UTC')).timetuple()),
                'category':int(ac.acc_cat.cat,10),
                'kind':ac.acc_type.id,
                'locations':address_str,
                'affected_customers':zkl,
                'reason':ac.acc_reason,
                'actions':ac.acc_repair
            }

            if ac.acc_end != None:
                values['finish_datetime'] = time.mktime(ac.acc_end.replace(tzinfo=timezone('UTC')).timetuple())
            if ac.acc_iss_id != None:
                values['iss_id'] = ac.acc_iss_id
            if ac.acc_reports_id != None:
                values['id'] = ac.acc_reports_id



            data = json.dumps(values)

            #print data

            req = urllib2.Request(url='http://zenoss.sib.transtk.ru:8000/api/reports/accidents/update/',data=data,headers={'Content-Type': 'application/json'})
            #req = urllib2.Request(url='http://127.0.0.1:5000/api/reports/accidents/references/',data=json.dumps({}),headers={'Content-Type': 'application/json'})

            f = urllib2.urlopen(req)
            result = f.read()
            r = json.loads(result)
            if ac.acc_reports_id == None and r.has_key("api_status"):
                if r["api_status"] == "OK":
                    ac.acc_reports_id = r["api_response"]["id"]
                    ac.save()

        """
        data = json.loads(result)
        for key in data["api_response"]["categories"].keys():
            print key,data["api_response"]["categories"][key]

        """

        print "ok"


