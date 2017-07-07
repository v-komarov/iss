#coding:utf8

import urllib
import json
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.localdicts.models import address_house





tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)





class Command(BaseCommand):
    args = '<None>'
    help = 'Разовая команда определение координад по городам и населенным пунктам в сервисе google'


    def check(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("SKIPPING SYSTEM CHECKS!\n"))



    def handle(self, *args, **options):


        #### Выбор 100 адресов случайным образом (по которым еще не было запроса о координатах)
        for addr in address_house.objects.filter(street=None,house=None,geo__result="empty"):

            city = urllib.quote(addr.city.name.encode("utf-8"))

            addr_str = u"{city}".format(city=city)

            url = u'http://maps.googleapis.com/maps/api/geocode/json?'

            param = 'address={addr_str}&sensor=false&region=ru'.format(addr_str=addr_str)

            f = urllib.urlopen(url+param)
            #print f.url
            data = json.loads(f.read())

            if data.has_key("status") and data["status"] == "OK":
                c = data["results"][0]["geometry"]["location"]
                addr.geo = {
                    "result": "ok",
                    "lat": c["lat"],
                    "lng": c["lng"]
                }

                addr.save()

            else:

                addr.geo = {
                    "result": "failure"
                }
                addr.save()