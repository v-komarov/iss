#coding:utf8

import logging
import datetime
import json
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces, devices_ports
from iss.localdicts.models import logical_interfaces_prop_list,port_status,device_status
from iss.equipment.models import client_mac_log,client_login_log

logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_use = port_status.objects.get(name='Используется')
port_tech = port_status.objects.get(name='Технологический')
port_rez = port_status.objects.get(name='Резерв')
device_use = device_status.objects.get(name='Используется')

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '< >'
    help = 'Отметка используемых портов'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка используемых портов устройств из данных json 

        """


        filename = args[0]

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка пользовательских портов

        """
        with open('iss/equipment/json/%s' % filename) as f:
            d = json.load(f)

            for ip in d["ports"].keys():
                ports = d["ports"][ip]

                print ip, ports

                ### Поиск по ip адресу на интерфейсе manager
                if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                    p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                    #### Определение серевого элемента
                    ne = p.logical_interface.netelem

                    ### Поиск связанного устройства
                    device = ne.device.all().first()

                    ### Обход портов устройства
                    for p in device.devices_ports_set.all():
                        ### Проверка порта
                        if int(p.num.decode("utf-8"),10) in ports:
                            p.status = port_use
                        else:
                            p.status = port_rez

                        p.datetime_update = krsk_tz.localize(datetime.datetime.now())
                        p.save()

                        print ip, device, p.num, p.status


                ### ip адрес не найден
                else:
                    logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=ip))


