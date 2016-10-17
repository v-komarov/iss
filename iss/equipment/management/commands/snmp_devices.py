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



    def handle(self, *args, **options):

        for ip in ip_address_list:

            devices_lldp.objects.filter(ipaddress=ip).delete()

            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(community),
                       UdpTransportTarget((ip, 161)),
                       ContextData(),
                       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
                       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
            )

            if errorIndication:
                print(errorIndication)
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                descr = varBinds[0]
                location = varBinds[1]

                i = 1
                over = False
                while not over:
                    ### Название портов
                    errorIndication, errorStatus, errorIndex, varBinds = next(
                        getCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((ip, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity(lldpLocPortTable+".1.4.%s" % i)),
                               ObjectType(ObjectIdentity(lldpLocPortTable+".1.3.%s" % i)),
                               ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.8.%s" % i)))
                    )
                    i = i + 1



                    for name,val in varBinds:
                        if val.prettyPrint() == "No Such Instance currently exists at this OID":
                            over = True
                        else:
                            print val.prettyPrint()

                over = False
                while not over:
                    ### Название портов
                    errorIndication, errorStatus, errorIndex, varBinds = next(
                        getCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((ip, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity(lldpLocPortTable + ".1.4.%s" % i)),
                               ObjectType(ObjectIdentity(lldpLocPortTable + ".1.3.%s" % i)),
                               ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.8.%s" % i)))
                    )
                    i = i + 1

                    for name, val in varBinds:
                        if val.prettyPrint() == "No Such Instance currently exists at this OID":
                            over = True
                        else:
                            print val.prettyPrint()

                over = False
                while not over:
                    ### Название портов
                    errorIndication, errorStatus, errorIndex, varBinds = next(
                        getCmd(SnmpEngine(),
                               CommunityData(community),
                               UdpTransportTarget((ip, 161)),
                               ContextData(),
                               ObjectType(ObjectIdentity(lldpLocPortTable + ".1.4.%s" % i)),
                               ObjectType(ObjectIdentity(lldpLocPortTable + ".1.3.%s" % i)),
                               ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.8.%s" % i)))
                    )
                    i = i + 1

                    for name, val in varBinds:
                        if val.prettyPrint() == "No Such Instance currently exists at this OID":
                            over = True
                        else:
                            print val.prettyPrint()

            print "ok"