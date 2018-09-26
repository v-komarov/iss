#coding:utf8

import logging
import datetime
import json
from pytz import timezone

from kafka import KafkaConsumer,TopicPartition

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces, devices_ports
from iss.localdicts.models import logical_interfaces_prop_list,port_status,device_status

import iss.dbconn

logger = logging.getLogger('ports')



prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_use = port_status.objects.get(name='Используется')
port_tech = port_status.objects.get(name='Технологический')
port_rez = port_status.objects.get(name='Резерв')
device_use = device_status.objects.get(name='Используется')

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)





kafka_server = iss.dbconn.KAFKA_SERVER
consumer = KafkaConsumer('circuit',bootstrap_servers=kafka_server, auto_offset_reset='earliest')




class Command(BaseCommand):
    args = '< >'
    help = 'Отметка используемых портов на основании данных circuit'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка используемых портов устройств из данных тэга circuit 

        """


        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка пользовательских портов

        """
        for m in consumer:

            d = m.value.replace("::",";").split(";")
            ip = d[1]
            port = d[2]

            #print ip, port

            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.get(prop=prop, val=ip)
                #### Определение серевого элемента
                ne = p.logical_interface.netelem

                ### Поиск связанного устройства
                device = ne.device.all().first()

                ### Обход портов устройства
                for p in devices_ports.objects.filter(device=device):
                    ### Проверка порта
                    if p.num == port:
                        p.status = port_use

                        print ip, device, p.num, p.status
                        logger.info("IP адрес устройства {} порт {} статус {}".format(ip, p.num, p.status))

                    p.datetime_update = krsk_tz.localize(datetime.datetime.now())
                    p.save()



            ### ip адрес не найден
            else:
                logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=ip))

