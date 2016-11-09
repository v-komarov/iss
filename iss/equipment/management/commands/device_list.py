#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import devices_ip,device_access_error
from django.db import connections
from easysnmp import Session

#import asyncio

from iss.monitor.models import events


community = "sibttklocal"

lldplocchassisid = "1.0.8802.1.1.2.1.3.2"
phys = "1.3.6.1.2.1.47.1.1.1.1.11.1"
serial_oid = "1.3.6.1.4.1.171.12.1.1.12"
#serial_oid = "1.3.6.1.2.1.47.1.1.1.1.11.1"
sysName = "1.3.6.1.2.1.1.5"
sysLocation = "1.3.6.1.2.1.1.6"
sysDescr = "1.3.6.1.2.1.1.1"



class Command(BaseCommand):
    args = '<graph ...>'
    help = 'saving graph'


    #@asyncio.coroutine
    def get_data(self,ip,source):


        try:

            session = Session(hostname=ip, community=community, version=2)

            name = session.get((sysName, '0')).value
            descr = session.get((sysDescr, '0')).value
            location = session.get((sysLocation, '0')).value
            chassisid = session.get((lldplocchassisid, '0'))
            if chassisid.snmp_type == "OCTETSTR":
                chassisid = ':'.join(['%0.2x' % ord(_) for _ in chassisid.value])
            else:
                chassisid = session.get((phys, '0')).value
                mac_list = chassisid.split(":")
                res = []
                for m in mac_list:
                    if m == "0":
                        res.append("00")
                    else:
                        res.append(m)

                chassisid = ":".join(res)

            serial = session.get((serial_oid, '0'))

            if serial.snmp_type == "OCTETSTR" or serial.snmp_type == "STRING":
                serial = serial.value
            else:
                serial = ""


            if devices_ip.objects.filter(ipaddress=ip).all().count() == 1:
                r = devices_ip.objects.get(ipaddress=ip)
                r.device_descr = descr
                r.device_name = name
                r.device_location = location
                r.device_domen = source
                r.chassisid = chassisid
                r.device_serial = serial
                r.save()
            else:
                devices_ip.objects.create(
                    ipaddress=ip,
                    device_descr=descr,
                    device_name=name,
                    device_location=location,
                    device_domen=source,
                    chassisid = chassisid,
                    device_serial = serial
                )

        except:
            print "error %s" % ip
            device_access_error.objects.create(ipaddress=ip,device_domen=source)
            devices_ip.objects.filter(ipaddress=ip, device_domen=source).update(access=False)



    def handle(self, *args, **options):



        source = args[0]
        iplist = args[1]

        if iplist == "all":


            #device_access_error.objects.filter(device_domen=source).delete()

            for ip in events.objects.filter(source=source).exclude(device_net_address="").distinct("device_net_address"):
                if devices_ip.objects.filter(ipaddress=ip.device_net_address,no_rewrite=True).count() == 0:
                    print ip.device_net_address
                    self.get_data(ip.device_net_address,source)

        else:
            self.get_data(iplist, source)
        print "ok"




