#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from easysnmp import Session
from iss.equipment.models import devices_ip,scan_iplist
import binascii

#community = "sibttklocal"
lldpLocPortTable = "1.0.8802.1.1.2.1.3.7.1.3"
#lldpRemEntry = "1.0.8802.1.1.2.1.4.1.1.7"
portStatus = "1.3.6.1.2.1.2.2.1.8"
lldpRemEntry  = "1.0.8802.1.1.2.1.4.1.1.5"


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'




    def handle(self, *args, **options):

        domen = args[0]

        for ip in devices_ip.objects.filter(device_domen=domen,access=True,no_rewrite=False):
            print "begin for %s" % ip.ipaddress

            try:
                ii = scan_iplist.objects.get(ipaddress=ip.ipaddress,device_domen=domen)

                session = Session(hostname=ip.ipaddress, community=ii.community, version=ii.snmp_ver)

                data = session.walk(lldpRemEntry)
                mac_list = []
                ports_json = {}
                ports = []
                for item in data:
                    port = int(item.oid.split(".")[-2], 10)
                    if item.snmp_type == "OCTETSTR":
                        mac = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                    else:
                        mac = item.value
                    ports.append({
                        'port': port,
                        'mac': mac}
                    )
                    mac_list.append(mac)

                ports_json["ports"] = ports
                r = devices_ip.objects.get(ipaddress=ip.ipaddress)
                r.lldp_neighbor_mac = mac_list
                r.ports = ports_json
                r.save()

            except:
                print "error %s" % ip.ipaddress


        print "ok"

