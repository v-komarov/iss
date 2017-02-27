#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q

from django.core.cache import cache


from iss.monitor.models import events

from pprint import pformat

import time
import datetime
import binascii
import logging
import hashlib
from pytz import timezone
from iss.localdicts.models import Status,Severity
import json
import cStringIO
import commands
import tempfile

import iss.dbconn
import iss.settings



username = iss.dbconn.ZENOSS_API_USERNAME
password = iss.dbconn.ZENOSS_API_PASSWORD


logger = logging.getLogger('debugging')



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)



### Дата появления поля finished_date 30.01.2017
fd = datetime.datetime.strptime("2017-01-30","%Y-%m-%d").replace(tzinfo=krsk_tz)





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

        startTime = (datetime.datetime.now(timezone(tz)) - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S').encode("utf-8")
        endTime = (datetime.datetime.now(timezone(tz)) + datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S').encode("utf-8")

        #cache.clear()

        cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":5000,\"sort\":\"lastTime\",\"dir\":\"desc\",\"params\":{\"lastTime\":\"%s/%s\"}}' %s %s %s" % (startTime,endTime,tf.name,username,password)
        #cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":5000,\"sort\":\"lastTime\",\"dir\":\"desc\",\"params\":{\"lastTime\":\"2017-02-16T00:00:00/2017-02-17T00:00:00\"}}' %s %s %s" % (tf.name,username,password)
        print cmd

        commands.getoutput(cmd)

        data = json.loads(commands.getoutput("cat %s" % tf.name))

        for r in (data["result"]["events"])[::-1]:
            event_str = json.dumps(r, sort_keys=True,indent=4,separators=(',',':'))
            print event_str

            id_row = r["id"]  # id
            evid = r["evid"].strip()


            ### Обработка записи только такая запись уже не обрабатывалась
            if r["device"].has_key("uuid"):


                firsttime = krsk_tz.localize(datetime.datetime.strptime(r["firstTime"], "%Y-%m-%d %H:%M:%S"))
                lasttime = krsk_tz.localize(datetime.datetime.strptime(r["lastTime"], "%Y-%m-%d %H:%M:%S"))
                update_time = krsk_tz.localize(datetime.datetime.strptime(r["stateChange"], "%Y-%m-%d %H:%M:%S"))  # update_time

                severity = Severity.objects.get(pk=r["severity"])
                summary = r["summary"]
                ipaddress = ", ".join(r["ipAddress"])  # ip

                uuid = r["device"]["uuid"]
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

                key = "%s%s%s" % (uuid,eventclass,location) # 20.02.2017
                hash_key = hashlib.md5(key).hexdigest() # 20.02.2017
                #key = evid # 20.02.2017


                last_action = cache.get(hash_key)
                ### Если такого ключа нет, добавить запись

                ### Определение что делать с записью по информации в кэше
                if last_action == None:
                    action = "insert"
                ### Если ключ есть  - обновить запись или ничего не делать
                elif last_action == "done":
                    action = ""
                else:
                    action = "update"


                ### Отладка
                if iss.settings.DEBUG == True:
                    logger.debug(
                        'key:{key} action:{action} lasttime:{lasttime} firsttime:{firsttime} last_action:{last_action} severity:{severity} location:{location}'.format(
                            key=key,action=action,last_action=last_action,severity=severity.id,firsttime=firsttime,lasttime=lasttime,location=location)
                    )




                ### Формирование нового события или запись в существующие
                """
                    Для severity: info, debug, clear (0,1,4) нет необходимости создавать новое событие
                """
                if severity.id != 0 and severity.id != 1 and severity.id != 4 and action == "insert":

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

                    # Запись кэш об insert для evid
                    cache.set(hash_key, "insert", 360000)


                elif action == "update":


                    ### Отладка
                    #if iss.settings.DEBUG == True:
                    #    logger.info(
                    #        'evid:{evid} id:{id} uuid:{uuid} firstTime:{firstTime} lastTime:{lastTime} eventclass:{eventclass} location:{location} elementIdentifier:{iden} key:{key}'.format(
                    #            location=location, evid=evid, uuid=uuid, eventclass=eventclass,
                    #            firstTime=r["firstTime"], id= id_row, lastTime=r["lastTime"], iden=device, key= keyevid)
                    #    )

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
                            summary=summary,
                            finished_date = lasttime
                        )
                        # Запись кэш об завершении события для evid
                        cache.set(hash_key,"done", 60)

                        #### Если событие не завершено
                        """
                            Обновление открытых аварийных событий
                        """
                    else:
                        events.objects.filter(uuid=uuid, finished_date=None, event_class=eventclass, datetime_evt__gt=fd).update(
                            first_seen=firsttime,
                            update_time=update_time,
                            last_seen=lasttime,
                            severity_id=severity,
                            summary=summary,
                            status_id=status
                        )
                        # Запись кэш об обновлении события для evid
                        cache.set(hash_key,"update", 360000)

        print "ok"


