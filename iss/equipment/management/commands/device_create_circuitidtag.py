#coding:utf8

import logging
import datetime
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces
from iss.localdicts.models import logical_interfaces_prop_list,port_status
from iss.equipment.models import client_mac_log,client_login_log

logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_use = port_status.objects.get(name='Используется')


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<Creating circuitidtag>'
    help = 'circuitidtag'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Установка номера порта для использования расстановки onyma_dogcode по логическим интерфейсам

        """

        ### Выбор ip адресов устройств
        for log in client_mac_log.objects.distinct('macaddress'):
            rec = client_mac_log.objects.filter(macaddress=log.macaddress).order_by('-create_update').first()
            print rec.macaddress,rec.port
            client_login_log.objects.filter(port="",macaddress=rec.macaddress,ipaddress="").update(port=rec.port,ipaddress=rec.ipaddress)
