#coding:utf8


from requests import post

from django.core.management.base import BaseCommand, CommandError

from django.core.cache import cache


from iss.monitor.models import events,events_history

from pprint import pformat

import datetime
import logging
import hashlib
from pytz import timezone
from kafka import KafkaProducer
from iss.localdicts.models import Status,Severity
import json

import iss.dbconn
import iss.settings


zenoss = "http://10.5.16.99:8080/zport/dmd/evconsole_router"


username = iss.dbconn.ZENOSS_API_IRK_USERNAME
password = iss.dbconn.ZENOSS_API_IRK_PASSWORD


logger = logging.getLogger('debugging')
loggerjson = logging.getLogger('events')


kafka_server = iss.dbconn.KAFKA_SERVER
producer = KafkaProducer(bootstrap_servers=kafka_server)


#tz = 'Asia/Irkutsk'
tz = 'Europe/Moscow'
irk_tz = timezone(tz)








#### Отправка сообщений в топик
def SendMsgTopic(evid,first_seen,last_seen,event_class,severity,device_net_address,device_location,uuid,device_class,device_group,device_system,element_identifier,status,summary):

    msg = {
        "evid":evid,
        "first_seen":first_seen.strftime("%d.%m.%Y %H:%M %z"),
        "last_seen":last_seen.strftime("%d.%m.%Y %H:%M %z"),
        "event_class":event_class,
        "severity":severity.name,
        "device_net_address":device_net_address,
        "device_location":device_location,
        "uuid":uuid,
        "device_class":device_class,
        "device_group":device_group,
        "device_system":device_system,
        "element_identifier":element_identifier,
        "status":status.name,
        "summary":summary
    }


    producer.send("zenoss-irk", json.dumps(msg))












class Command(BaseCommand):
    args = '<zenoss message ...>'
    help = 'saving zenoss message'


    def check(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("SKIPPING SYSTEM CHECKS!\n"))



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

        startTime = (datetime.datetime.now(timezone(tz)) - datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S').encode("utf-8")
        endTime = (datetime.datetime.now(timezone(tz)) + datetime.timedelta(minutes=3)).strftime('%Y-%m-%dT%H:%M:%S').encode("utf-8")



        query = {'action': 'EventsRouter', 'data': [{
            'limit': 2000,
            'sort': 'lastTime',
            'params': {'lastTime': "%s/%s" % (startTime, endTime)} }],
            'method': 'query',
            'tid': 1 }
        rec = post(url=zenoss, json=query, verify=False, auth=(username, password))
        print pformat(json.loads(rec.text))
        data = json.loads(rec.text)



        for r in (data["result"]["events"]):

            evid = r["evid"].strip()


            ### Обработка записи только такая запись уже не обрабатывалась
            if r["device"].has_key("uuid"):


                firsttime = irk_tz.localize(datetime.datetime.strptime(r["firstTime"], "%Y-%m-%d %H:%M:%S"))
                lasttime = irk_tz.localize(datetime.datetime.strptime(r["lastTime"], "%Y-%m-%d %H:%M:%S"))
                update_time = irk_tz.localize(datetime.datetime.strptime(r["stateChange"], "%Y-%m-%d %H:%M:%S"))  # update_time

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

                key = hashlib.md5("{evid}zenoss_irk{severity}:{status}".format(evid=evid, severity=r["severity"], status=r["eventState"])).hexdigest()


                last_action = cache.get(key)
                ### Если такого ключа нет, добавить запись

                ### Определение что делать с записью по информации в кэше
                if last_action == None and severity.id != 0 and severity.id != 1 and severity.id != 4:
                    if events.objects.filter(evid=evid).exists() == False:
                        action = "insert"
                    else:
                        action = "update"
                ### Если ключ есть  - обновить запись
                else:
                    action = "update"


                ### Отладка
                if iss.settings.DEBUG == True:
                    logger.debug(
                        'key:{key} action:{action} lasttime:{lasttime} firsttime:{firsttime} last_action:{last_action} severity:{severity} location:{location}'.format(
                            key=key,action=action,last_action=last_action,severity=severity.id,firsttime=firsttime,lasttime=lasttime,location=location)
                    )





                ### Запись сообщения в топик
                SendMsgTopic(evid,firsttime,lasttime,eventclass,severity,ipaddress,location,uuid,deviceclass,devicegroup,devicesystem,device,status,summary)




                ### Формирование нового события или запись в существующие
                """
                    Для severity: info, debug, clear (0,1,4) нет необходимости создавать новое событие
                """
                if action == "insert":
                    events.objects.create(
                        evid=evid,
                        source='zenoss_irk',
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
                    cache.set(key, "insert", 360000)


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
                        ### Перенос данных в events_history при определенных условиях
                        r0 = events.objects.filter(evid=evid, source='zenoss_irk')
                        if r0.count() > 0:
                            e = r0[0]
                            if e.agregator == False and e.agregation == False and e.accident == False:
                                events_history.objects.create(
                                    events_id=e.id,
                                    datetime_evt=e.datetime_evt,
                                    source='zenoss_irk',
                                    uuid=e.uuid,
                                    first_seen=e.first_seen,
                                    update_time=e.update_time,
                                    last_seen=e.last_seen,
                                    event_class=e.event_class,
                                    severity_id=e.severity_id,
                                    manager=e.manager,
                                    device_net_address=e.device_net_address,
                                    device_location=e.device_location,
                                    device_class=e.device_class,
                                    device_group=e.device_group,
                                    device_system=e.device_system,
                                    element_identifier=e.element_identifier,
                                    element_sub_identifier="",
                                    status_id=e.status_id,
                                    summary=e.summary,
                                    started_date=e.started_date,
                                    finished_date=lasttime
                                )
                                r0.delete()

                            else:
                                events.objects.filter(evid=evid, source='zenoss_irk').update(
                                    first_seen=firsttime,
                                    update_time=update_time,
                                    last_seen=lasttime,
                                    severity_id=severity,
                                    status_id=status,
                                    summary=summary,
                                    finished_date = lasttime
                                )
                        # Запись кэш об завершении события для evid
                        cache.delete(key)

                        #### Если событие не завершено
                        """
                            Обновление открытых аварийных событий
                        """
                    else:
                        events.objects.filter(evid=evid, source='zenoss_irk').update(
                            first_seen=firsttime,
                            update_time=update_time,
                            last_seen=lasttime,
                            severity_id=severity,
                            summary=summary,
                            status_id=status
                        )
                        # Запись кэш об обновлении события для evid
                        cache.set(key,"update", 360000)



        producer.flush()

        print "ok"


