#coding:utf8

import logging
import datetime
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces
from iss.localdicts.models import logical_interfaces_prop_list,port_status
from iss.equipment.models import client_login_log

logger = logging.getLogger('loadding')

onyma = logical_interfaces_prop_list.objects.get(name='onyma')
prop = logical_interfaces_prop_list.objects.get(name='ipv4')

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<Mark logical interface by onyma>'
    help = 'mark onyma'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка портов номерами договоров Онима на логических интерфейсах

        """

        for login in client_login_log.objects.exclude(onyma_dogid=0).exclude(port="").exclude(ipaddress=""):
            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=login.ipaddress, logical_interface__name='manage').exists():
                intf = logical_interfaces_prop.objects.get(prop=prop, val=login.ipaddress)
                #### Определение серевого элемента
                ne = intf.logical_interface.netelem
                ### Определение есть ли договор на конкретном логическом интерфейсе
                if not ne.netelem_set.all().filter(name=login.port).exists():
                    lf = ne.netelem_set.all().filter(name=login.port).first()
                    logical_interfaces_prop.objects.create(
                        logical_interface=lf,
                        prop=onyma,
                        val=login.onyma_dogcode,
                        comment='Договор'
                    )
                else:
                    logger.info("Не найден логический интерфейс {port} {ipaddress}".format(ipaddress=login.ipaddress,port=login.port))