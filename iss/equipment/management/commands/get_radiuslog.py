#coding:utf8

import datetime
import re

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from pytz import timezone


from iss.equipment.models import client_login_log



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)

## Шаблоны поиска
client_login = re.compile("User-Name=\"(\w+)\"")
client_mac = re.compile("client-mac-address=\"(\w{4}.\w{4}.\w{4})\"")
curcuit_id_tag = re.compile("circuit-id-tag=\"(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}::\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}::\d+)\"")


class Command(BaseCommand):
    args = '<radius data ...>'
    help = 'getting radius data'





    def handle(self, *args, **options):

        filename = args[0].split("#")
        for file in filename:
            if file != "":
                with open(file,'r') as f:
                    for line in f.readlines():
                        circuit = curcuit_id_tag.search(line)
                        mac = client_mac.search(line)
                        login = client_login.search(line)
                        if login and mac:
                            print file, login.group(1)
                            m = mac.group(1).replace(".","")
                            m2 = m[0:2] + ":" + m[2:4] + ":" + m[4:6] + ":" + m[6:8] + ":" + m[8:10] + ":" + m[10:12]
                            # Проверка наличие логина в кэше
                            if not cache.get(login.group(1)):
                                client_login_log.objects.update_or_create(
                                    login=login.group(1),
                                    macaddress=m2
                                )
                                if circuit:
                                    circuit_id = circuit.group(1)
                                    tag = circuit_id.split("::")

                                    client_login_log.objects.filter(login=login.group(1), macaddress=m2).update(
                                        create_update=krsk_tz.localize(datetime.datetime.now()), circuit_id_tag=circuit_id, ipaddress=tag[1], port=tag[2])
                                else:
                                    client_login_log.objects.filter(login=login, macaddress=m2).update(
                                        create_update=krsk_tz.localize(datetime.datetime.now()))

                                cache.set(login.group(1), m, 3600)

                                response_data = {'result': 'OK', 'comment': 'updated or inserted'}

                            else:

                                response_data = {'result': 'OK', 'comment': 'found in cache'}
