#coding:utf8

import datetime
import csv
from ftplib import FTP

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from pytz import timezone


from iss.equipment.models import client_login_log



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<radius data ...>'
    help = 'getting radius data'





    def handle(self, *args, **options):



        ftp = FTP('10.6.0.88')
        ftp.login()
        ftp.cwd('pub')
        ftp.retrbinary("RETR data.csv", open("/tmp/data.csv", 'wb').write)
        ftp.quit()

        with open('/tmp/data.csv') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            #next(spamreader, None)
            for row in spamreader:
                login = row[1]
                mac = row[2]
                circuit = row[3]
                print login,mac,circuit

                client_login_log.objects.update_or_create(
                    login=login,
                    macaddress=mac
                )
                if len(circuit) > 0:
                    tag = circuit.split("::")

                    client_login_log.objects.filter(login=login, macaddress=mac).update(
                        create_update=krsk_tz.localize(datetime.datetime.now()), circuit_id_tag=circuit, ipaddress=tag[1], port=tag[2])
                else:
                    client_login_log.objects.filter(login=login, macaddress=mac).update(
                        create_update=krsk_tz.localize(datetime.datetime.now()))

                response_data = {'result': 'OK', 'comment': 'updated or inserted'}

