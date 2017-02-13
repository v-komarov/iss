#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from iss.monitor.models import events

import time
import datetime
import binascii
from pytz import timezone
from iss.localdicts.models import Status,Severity
import json
import cStringIO
import commands
import tempfile

import iss.dbconn



username = iss.dbconn.ZENOSS_API_USERNAME
password = iss.dbconn.ZENOSS_API_PASSWORD




tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'



    def list0name(self,name):
        if len(name) > 0:
            return name[0]["name"]
        else:
            return ""


    def list2name(self,namelist):
        names = []
        for item in namelist:
            names.append(item['name'])
        return ", ".join(names)




    def handle(self, *args, **options):

        tf = tempfile.NamedTemporaryFile(delete=True)



        cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":5000,\"sort\":\"lastTime\",\"dir\":\"desc\"}' %s %s %s" % (tf.name,username,password)

        print cmd
        commands.getoutput(cmd)

        data = json.loads(commands.getoutput("cat %s" % tf.name))

        for r in (data["result"]["events"])[::-1]:
            event_str = json.dumps(r, sort_keys=True,indent=4,separators=(',',':'))
            print event_str
            id_row = r["id"] # id
            ipaddress = ", ".join(r["ipAddress"]) # ip
            firsttime = krsk_tz.localize(datetime.datetime.strptime(r["firstTime"],"%Y-%m-%d %H:%M:%S"))
            lasttime = krsk_tz.localize(datetime.datetime.strptime(r["lastTime"],"%Y-%m-%d %H:%M:%S"))
            summary = r["summary"]
            severity = Severity.objects.get(pk=r["severity"])
            update_time = krsk_tz.localize(datetime.datetime.strptime(r["stateChange"],"%Y-%m-%d %H:%M:%S")) # update_time
            uuid = r["device"]["uuid"] # uuid
            status = Status.objects.get(name=r["eventState"]) # Статус
            eventclass = r["eventClass"]["text"]

            device = r["device"]["text"]

            location = self.list2name(r["Location"])
            devicesystem = self.list2name(r["Systems"])
            deviceclass = self.list2name(r["DeviceClass"]) # DeviceGroup
            devicegroup = self.list2name(r["DeviceGroups"]) # DeviceClass

            manager = ""
            if r["details"].has_key("manager"):
                manager = ", ".join(r["details"]["manager"])

            ### Формирование нового события или запись в существующие
            """
                Для severity: info, debug, clear (0,1,4) нет необходимости создавать новое событие
            """
            if events.objects.filter(uuid=uuid,finished_date=None,event_class=eventclass).count() == 0 and severity.id != 0 and severity.id != 1 and severity.id != 4:
                events.objects.create(
                    source='zenoss_krsk',
                    uuid=uuid,
                    first_seen=firsttime,
                    update_time=update_time,
                    last_seen=lasttime,
                    event_class=eventclass,
                    severity_id=severity,
                    manager=manager,
                    device_net_address=ipaddress,
                    device_location=location,
                    device_class=deviceclass,
                    device_group=devicegroup,
                    device_system=devicesystem,
                    element_identifier=device,
                    element_sub_identifier="",
                    status_id=status,
                    summary=summary,
                    started_date = firsttime

                )

            else:

                #### Завершение события (очистка) или нет - определение в зависимости от статуса
                """
                    для статусов closed , cleared (4,5) при обновлении открытого (с finished_date = None)
                    аварийного события фиксируем завершение этого события установкой finished_date
                """
                if status.id == 4 or status.id == 5:
                    events.objects.filter(uuid=uuid, finished_date=None, event_class=eventclass).update(
                        first_seen=firsttime,
                        update_time=update_time,
                        last_seen=lasttime,
                        severity_id=severity,
                        status_id=status,
                        finished_date = lasttime
                    )

                #### Если событие не завершено
                    """
                        Обновление открытых аварийных событий
                    """
                else:
                    events.objects.filter(uuid=uuid, finished_date=None, event_class=eventclass).update(
                        first_seen=firsttime,
                        update_time=update_time,
                        last_seen=lasttime,
                        severity_id=severity,
                        status_id=status
                    )

        print "ok"


