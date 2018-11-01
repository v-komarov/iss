#coding:utf8

import logging
import datetime
import json
from pytz import timezone

from kafka import KafkaConsumer,TopicPartition

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces, devices_ports, devices_slots, devices_combo
from iss.localdicts.models import logical_interfaces_prop_list,port_status,device_status,slot_status

import iss.dbconn

logger = logging.getLogger('ports')



prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_use = port_status.objects.get(name='Используется')
port_tech = port_status.objects.get(name='Технологический')
port_rez = port_status.objects.get(name='Резерв')
slot_use = slot_status.objects.get(name='Используется')
slot_rez = slot_status.objects.get(name='Резерв')

device_use = device_status.objects.get(name='Используется')

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)





kafka_server = iss.dbconn.KAFKA_SERVER
consumer = KafkaConsumer('port-mac',bootstrap_servers=kafka_server, auto_offset_reset='earliest')




class Command(BaseCommand):
    args = '< >'
    help = 'Отметка используемых портов на основании данных активности mac адресов'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка используемых портов устройств из данных mac адресов

        """


        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка пользовательских и технологических портов

        """
        for m in consumer:

            data = json.loads(m.value)

            ip = data["ip"]
            port = data["port"]
            mode = data["mode"]

            #print ip,port,mode

            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.filter(prop=prop, val=ip, logical_interface__name='manage').first()
                #### Определение серевого элемента
                ne = p.logical_interface.netelem

                ### Поиск связанного устройства
                device = ne.device.all().first()

                ### Обход портов устройства
                for p in devices_ports.objects.filter(device=device):
                    ### Проверка порта , исключение отмеченный через circuit
                    if p.num == port and p.author != "circuit":
                        p.status = port_use if mode == "use" else port_tech

                        print ip, device, p.num, p.status
                        logger.info("IP адрес устройства {} сетевой элемент {} порт {} статус {}".format(ip, ne.name, p.num, p.status))

                        p.datetime_update = krsk_tz.localize(datetime.datetime.now())
                        p.author = "port-mac"
                        p.save()


                for st in devices_slots.objects.filter(device=device):
                    ### Проверка слотов
                    if st.num == port:
                        st.status = slot_use

                        print ip, device, st.num, st.status
                        logger.info(
                            "IP адрес устройства {} сетевой элемент {} слот {} статус {}".format(ip, ne.name, st.num, st.status))
                        st.datetime_update = krsk_tz.localize(datetime.datetime.now())
                        st.author = "port-mac"
                        st.save()


                for p in devices_combo.objects.filter(device=device):
                    ### Проверка комбо
                    if p.num == port:
                        p.status_port = port_use if mode == "use" else port_tech

                        print ip, device, p.num, p.status_port
                        logger.info(
                            "IP адрес устройства {} сетевой элемент {} комбо {} статус {}".format(ip, ne.name, p.num, p.status_port))

                        p.datetime_update = krsk_tz.localize(datetime.datetime.now())
                        p.author = "port-mac"
                        p.save()


            ### ip адрес не найден
            else:
                logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=ip))


