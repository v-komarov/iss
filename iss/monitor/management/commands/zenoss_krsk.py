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


"""

pycurl необходим libgnutls-dev

"""



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


    def handle(self, *args, **options):

        tf = tempfile.NamedTemporaryFile(delete=True)


        """

        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None,'http://10.6.0.22:8080/','vak','')
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        headers = {'User-Agent': 'Mozilla 5.10'}
        request = urllib2.Request('http://10.6.0.22:8080/monitor/events/page/1/', None, headers)
        f = opener.open(request)
        data = f.read()
        print data
        f.close()
        """

#        cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":2000,\"params\":{\"eventState\":[0,1,3]}}' %s" % (tf.name)
        cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":5000,\"sort\":\"lastTime\",\"dir\":\"desc\"}' %s" % (tf.name)
        #cmd = "./json_api.sh evconsole_router EventsRouter query '{\"limit\":3000,\"sort\":\"stateChange\",\"dir\":\"desc\"}' %s" % (tf.name)

        print cmd
        commands.getoutput(cmd)

        uuid_list = []

        data = json.loads(commands.getoutput("cat %s" % tf.name))
        for r in data["result"]["events"]:
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

            location = self.list0name(r["Location"])
            devicesystem = self.list0name(r["Systems"])
            deviceclass = self.list0name(r["DeviceClass"]) # DeviceGroup
            devicegroup = self.list0name(r["DeviceGroups"]) # DeviceClass

            manager = ""
            if r["details"].has_key("manager"):
                manager = ", ".join(r["details"]["manager"])

            if uuid not in uuid_list:
                uuid_list.append(uuid)

                if events.objects.filter(uuid=uuid).count() == 0:
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
                        summary=summary

                    )

                else:

                    evt = events.objects.get(uuid=uuid)

                    evt.first_seen = firsttime
                    evt.update_time = update_time
                    evt.last_seen = lasttime
                    evt.event_class = eventclass
                    evt.severity_id = severity
                    evt.manager = manager
                    evt.device_net_address = ipaddress
                    evt.device_location = location
                    evt.device_class = deviceclass
                    evt.device_group = devicegroup
                    evt.device_system = devicesystem
                    evt.element_identifier = device
                    evt.element_sub_identifier = ""
                    evt.status_id = status
                    evt.summary = summary
                    evt.save()

        print "ok"


