#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from pysnmp.hlapi import *

from iss.equipment.models import devices_lldp



ip_address_list = ['10.5.105.1']
community = "sibttklocal"
lldpLocPortTable = "1.0.8802.1.1.2.1.3.7"
lldpRemEntry = "1.0.8802.1.1.2.1.4.1.1"


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'


    def GetValue(self,ip,oid):

        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(community),
                   UdpTransportTarget((ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity(oid)))
        )

        return varBinds




    def handle(self, *args, **options):

        for ip in ip_address_list:

            devices_lldp.objects.filter(ipaddress=ip).delete()

            ### Название локальных портов
            for i in range(1,100):
                result = self.GetValue(ip,lldpLocPortTable+".1.4.%s" % i)
                for name, val in result:
                    if val.prettyPrint() == "No Such Instance currently exists at this OID":
                        break
                    print val.prettyPrint()

            ### Статус локальных портов
            for i in range(1,100):
                result = self.GetValue(ip,lldpLocPortTable+".1.2.%s" % i)
                for name, val in result:
                    if val.prettyPrint() == "No Such Instance currently exists at this OID":
                        break
                    print val.prettyPrint()

            ### MAC локальных портов
            for i in range(1,100):
                result = self.GetValue(ip,lldpLocPortTable+".1.3.%s" % i)
                for name, val in result:
                    if val.prettyPrint() == "No Such Instance currently exists at this OID":
                        break
                    print val.prettyPrint()

            ### Название портов соседей
            for i in range(1,50):
                result = self.GetValue(ip,"1.0.8802.1.1.2.1.4.1.1")
                for name, val in result:
                    if val.prettyPrint() == "No Such Instance currently exists at this OID":
                        break
                    print val.prettyPrint()


            print "ok"