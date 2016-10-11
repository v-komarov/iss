#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from pysnmp.hlapi import *


class Command(BaseCommand):
    args = '<snmp ...>'
    help = 'saving snmp data of devices'



    def handle(self, *args, **options):


        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public'),
                   UdpTransportTarget(('demo.snmplabs.com', 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
                   ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0')))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))

        print "ok"