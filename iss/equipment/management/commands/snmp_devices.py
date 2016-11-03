#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from easysnmp import Session
from iss.equipment.models import devices_lldp,devices_ip
import binascii

ip_address_list = ['10.5.105.1','10.5.105.2','10.5.105.3','10.5.102.2']
#ip_address_list = ['10.4.119.1','10.4.125.1','10.204.112.41','10.204.112.42','10.204.112.43','10.204.112.44','10.204.112.45','10.204.112.46','10.204.112.47']
community = "sibttklocal"
lldpLocPortTable = "1.0.8802.1.1.2.1.3.7.1.3"
lldpRemEntry = "1.0.8802.1.1.2.1.4.1.1.7"
portStatus = "1.3.6.1.2.1.2.2.1.8"
#lldpRemEntry  = "1.0.8802.1.1.2.1.4.1.1.5"


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'




    def handle(self, *args, **options):

        devices_ip.objects.all().delete()
        devices_lldp.objects.all().delete()

        for ip in ip_address_list:
            print "begin for %s" % ip
            session = Session(hostname=ip, community=community, version=2)

            name = session.get(('sysName', '0'))
            descr = session.get(('sysDescr', '0'))
            location = session.get(('sysLocation', '0'))

            d = devices_ip.objects.create(
                ipaddress = ip,
                device_name = name.value,
                device_descr = descr.value,
                device_location = location.value,
                device_domen = "zenoss_krsk"
            )

            data = session.walk(lldpLocPortTable)
            for item in data:
                port = int(item.oid.split(".")[-1],10)
                mac = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                devices_lldp.objects.create(
                    port_local_index = port,
                    port_local_mac = mac,
                    device_ip = d
                )
                """
                print '{oid}.{oid_index} {snmp_type} = {value}'.format(
                    oid=item.oid,
                    oid_index=item.oid_index,
                    snmp_type=item.snmp_type,
                    value = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                )
                """

            data = session.walk(lldpRemEntry)
            for item in data:
                port = int(item.oid.split(".")[-2], 10)
                mac = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                rec = devices_lldp.objects.get(device_ip=d,port_local_index=port)
                rec.port_neighbor_mac = mac
                rec.save()
                """
                print '{oid}.{oid_index} {snmp_type} = {value}'.format(
                    oid=item.oid,
                    oid_index=item.oid_index,
                    snmp_type=item.snmp_type,
                    value = ':'.join(['%0.2x' % ord(_) for _ in item.value])
                )
                """

            data = session.walk(portStatus)
            for item in data:

                port = int(item.oid_index.split(".")[-1], 10)
                if devices_lldp.objects.filter(device_ip=d,port_local_index=port).count() == 1:
                    rec = devices_lldp.objects.get(device_ip=d, port_local_index=port)
                    if item.value == u'1':
                        rec.port_status = True
                        rec.save()
                """
                print '{oid}.{oid_index} {snmp_type} = {value}'.format(
                    oid=item.oid,
                    oid_index=item.oid_index,
                    snmp_type=item.snmp_type,
                    value=item.value
                )
                """

        print "ok"

