#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from easysnmp import Session
from iss.equipment.models import devices_ip
import binascii

community = "sibttklocal"
lldpLocPortTable = "1.0.8802.1.1.2.1.3.7.1.3"
#lldpRemEntry = "1.0.8802.1.1.2.1.4.1.1.7"
portStatus = "1.3.6.1.2.1.2.2.1.8"
lldpRemEntry  = "1.0.8802.1.1.2.1.4.1.1.5"


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'




    def handle(self, *args, **options):

        for ip in devices_ip.objects.filter(device_domen="zenoss_krsk"):
            print "begin for %s" % ip.ipaddress

            try:

                session = Session(hostname=ip.ipaddress, community=community, version=2)

                data = session.walk(lldpRemEntry)
                mac_list = []
                for item in data:
                    if item.snmp_type == "OCTETSTR":
                        mac = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                    else:
                        mac = item.value

                    mac_list.append(mac)

                r = devices_ip.objects.get(ipaddress=ip.ipaddress)
                r.lldp_neighbor_mac = mac_list
                r.save()

            except:
                print "error %s" % ip.ipaddress


        print "ok"

