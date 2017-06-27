#coding:utf8

import logging
import csv
import datetime
from pytz import timezone

from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import devices_ports,logical_interfaces_prop
from iss.localdicts.models import logical_interfaces_prop_list,port_status

logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_res = port_status.objects.get(name='Резерв')
port_tech = port_status.objects.get(name='Технологический')
port_use = port_status.objects.get(name='Используется')


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<Technical port>'
    help = 'Technical port'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка технологических портов

        """
        with open('iss/equipment/csv/tag.csv') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            #next(spamreader, None)
            for row in spamreader:
                ip = row[0]
                port = row[1]
                adminup = row[2]
                operup = row[3]

                status = port_use if operup == '1' else port_res
                print ip,port,status

                ### Поиск по ip адресу на интерфейсе manager
                if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                    p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                    #### Определение серевого элемента
                    ne = p.logical_interface.netelem

                    ### Поиск связанного устройства
                    device = ne.device.all().first()

                    if device.devices_ports_set.filter(num=port).count() == 1:
                       p =  device.devices_ports_set.get(num=port)
                       p.status = status
                       p.comment = ''
                       p.datetime_update=krsk_tz.localize(datetime.datetime.now())
                       p.save()

                       print "Установлен технологический порт {port} по адресу {ipaddress}".format(port=port,ipaddress=ip)

                    elif device.devices_combo_set.filter(num=port).count() == 1:
                        p = device.devices_combo_set.get(num=port)
                        p.status_port = status
                        p.comment = ''
                        p.datetime_update = krsk_tz.localize(datetime.datetime.now())
                        p.save()

                        print "Установлен технологический combo порт {port} по адресу {ipaddress}".format(port=port, ipaddress=ip)

                    else:
                        logger.info("Порт {port} не найден на устройстве {ipaddress}".format(port=port,ipaddress=ip))

                ### ip адрес не найден
                else:
                    logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=ip))

