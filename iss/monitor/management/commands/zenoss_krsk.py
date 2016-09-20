#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

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

        timedelta = int(time.time()*1000) - 3600

        data = []

        for table in 'event_summary','event_archive':

            cursor = connections["zenoss_krsk"].cursor()
            q = "SELECT first_seen,update_time,last_seen,summary,message,details_json,event_class.name,severity_id,uuid,element_identifier,element_sub_identifier,status_id FROM %s LEFT JOIN event_class ON %s.event_class_id=event_class.id WHERE update_time > %s ORDER BY first_seen;" % (table,table,timedelta)

            cursor.execute(q)

            d = cursor.fetchall()

            for row in d:

                manager = ""
                device_class = ""
                device_group = ""
                device_net_address = ""
                device_location = ""
                device_system = ""

                arrayjson = eval(row[5])

                for item in arrayjson:
                    if item['name'] == 'manager':
                        manager = item['value'][0]
                    elif item['name'] == 'zenoss.device.ip_address':
                        device_net_address = item['value'][0]
                    elif item['name'] == 'zenoss.device.location':
                        device_location = item['value'][0]
                    elif item['name'] == 'zenoss.device.device_class':
                        device_class = item['value'][0]
                    elif item['name'] == 'zenoss.device.groups':
                        device_group = item['value'][0]
                    elif item['name'] == 'zenoss.device.systems':
                        device_system = item['value'][0]



                if events.objects.filter(Q(uuid=binascii.b2a_hex(row[8]),source = 'zenoss_krsk')).count() == 0:
                    events.objects.create(
                        datetime_evt = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[0]) / 1000)),
                        source = 'zenoss_krsk',
                        uuid = binascii.b2a_hex(row[8]),
                        first_seen = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[0]) / 1000)),
                        update_time = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[1]) / 1000)),
                        last_seen = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[2]) / 1000)),
                        event_class = row[6],
                        severity_id = row[7],
                        manager = manager,
                        device_net_address = device_net_address,
                        device_location = device_location,
                        device_class = device_class,
                        device_group = device_group,
                        device_system = device_system,
                        element_identifier = row[9],
                        element_sub_identifier = row[10],
                        status_id = row[11]
                    )


                else:

                    evt = events.objects.filter(uuid=binascii.b2a_hex(row[8]),source='zenoss_krsk').get()

                    evt.datetime_evt = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[0]) / 1000))
                    evt.first_seen = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[0]) / 1000))
                    evt.update_time = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[1]) / 1000))
                    evt.last_seen = krsk_tz.localize(datetime.datetime.fromtimestamp(int(row[2]) / 1000))
                    evt.event_class = row[6]
                    evt.severity_id = row[7]
                    evt.manager = manager
                    evt.device_net_address = device_net_address
                    evt.device_location = device_location
                    evt.device_class = device_class
                    evt.device_group = device_group
                    evt.device_system = device_system
                    evt.element_identifier = row[9]
                    evt.element_sub_identifier = row[10]
                    evt.status_id = row[11]
                    evt.save()

        print "ok"


