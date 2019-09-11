#coding:utf8

from requests import post

from django.core.management.base import BaseCommand, CommandError


from pprint import pformat
from kafka import KafkaProducer
import datetime
from pytz import timezone
import json


import iss.dbconn
import iss.settings


zenoss = "http://10.6.0.129:8080/zport/dmd/evconsole_router"


username = iss.dbconn.ZENOSS_API_KRSK_USERNAME
password = iss.dbconn.ZENOSS_API_KRSK_PASSWORD



tz = 'Europe/Moscow'
krsk_tz = timezone(tz)



kafka_server = iss.dbconn.KAFKA_SERVER
producer = KafkaProducer(bootstrap_servers=kafka_server)



severity_dict = {
    '0': 'Debug',
    '1': 'Info',
    '2': 'Error',
    '3': 'Warning',
    '4': 'Clear',
    '5': 'Critical'
}





#### Отправка сообщений в топик
def SendMsgTopic(evid,first_seen,last_seen,event_class,severity,device_net_address,device_location,uuid,device_class,device_group,device_system,element_identifier,status,summary):

    msg = {
        "evid":"krsk-{}".format(evid),
        "first_seen":first_seen.strftime("%d.%m.%Y %H:%M %z"),
        "last_seen":last_seen.strftime("%d.%m.%Y %H:%M %z"),
        "event_class":event_class,
        "severity":severity,
        "device_net_address":device_net_address,
        "device_location":device_location,
        "uuid":uuid,
        "device_class":device_class,
        "device_group":device_group,
        "device_system":device_system,
        "element_identifier":element_identifier,
        "status":status,
        "summary":summary
    }


    producer.send("zenoss", json.dumps(msg))







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
        endTime = (datetime.datetime.now(timezone(tz)) + datetime.timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S').encode("utf-8")

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


            if r["device"].has_key("uuid"):



                firsttime = krsk_tz.localize(datetime.datetime.strptime(r["firstTime"], "%Y-%m-%d %H:%M:%S"))
                lasttime = krsk_tz.localize(datetime.datetime.strptime(r["lastTime"], "%Y-%m-%d %H:%M:%S"))

                severity = severity_dict["%s" % r["severity"]]
                summary = r["summary"]
                ipaddress = ", ".join(r["ipAddress"])  # ip

                uuid = r["device"]["uuid"]
                status = r["eventState"] # Статус
                eventclass = r["eventClass"]["text"]

                device = r["device"]["text"]

                location = self.list2name(r["Location"])
                devicesystem = self.list2name(r["Systems"])
                deviceclass = self.list2name(r["DeviceClass"]) # DeviceGroup
                devicegroup = self.list2name(r["DeviceGroups"]) # DeviceClass



                ### Запись сообщения в топик
                SendMsgTopic(evid,firsttime,lasttime,eventclass,severity,ipaddress,location,uuid,deviceclass,devicegroup,devicesystem,device,status,summary)



        producer.flush()

        print "ok"


