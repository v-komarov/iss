#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner.cmdgen import MibVariable

from iss.equipment.models import devices_lldp



ip_address_list = ['10.5.105.1']
community = "sibttklocal"
lldpLocPortTable = "1.0.8802.1.1.2.1.3.7"
lldpRemEntry = "1.0.8802.1.1.2.1.4.1.1"


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'


    def GetMultyValue(self,ip,oid):

        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(community),
                   UdpTransportTarget((ip, 161)),
                   ContextData(),
                   MibVariable(ObjectIdentity(oid)).addMibSource("/path/to/mibs"),
                   #cmdgen.MibVariable('SNMPv2-MIB', 'sysLocation', 0),
                   lexicographicMode=True,
                   maxRows=10000,
                   ignoreNonIncreasingOid=True
                   )
        )

        return varBinds



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
            """
            ### Название локальных портов
            for i in range(1,100):
                result = self.GetValue(ip,lldpLocPortTable+".1.4.%s" % i)
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
            """
            import commands
            data = commands.getoutput('snmpwalk -v2c -c sibttklocal 10.5.105.1 1.0.8802.1.1.2.1.4.1.1.5')
            x = 0
            step = data.find(":",x)+20
            while x <= len(data):
                a = data[data.find("4.1.1.5",x):data.find(" =",x)].split(".")[-2]
                #print data[data.find(":",x)+2:data.find(":",x)+19].replace(" ","").lower()
                x = x + step



            print "ok"

