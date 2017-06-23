#coding:utf8

import logging
import datetime
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces
from iss.localdicts.models import logical_interfaces_prop_list,port_status
from iss.equipment.models import client_mac_log

logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
port_use = port_status.objects.get(name='Используется')


tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '<Checking devices ports >'
    help = 'checking'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Проверка портов устройств на использование,
        создание интерфейсов, связность физического порта и интерфейса

        """

        ### Выбор ip адресов устройств
        for ip in client_mac_log.objects.distinct('ipaddress'):
            rec = client_mac_log.objects.filter(ipaddress=ip.ipaddress).order_by('-create_update').first()
            print rec.ipaddress,rec.macaddress,rec.port

            ### Поиск по ip адресу на интерфейсе manager
            if logical_interfaces_prop.objects.filter(prop=prop, val=rec.ipaddress, logical_interface__name='manage').exists():
                p = logical_interfaces_prop.objects.get(prop=prop, val=rec.ipaddress)
                #### Определение серевого элемента
                ne = p.logical_interface.netelem

                ### Поиск связанного устройства
                device = ne.device.all().first()

                ### Проверка наличие порта у устройства
                if device.devices_ports_set.filter(num=rec.port).exists():

                    device_port = device.devices_ports_set.get(num=rec.port)
                    ### Перевод порта в статус ИСПОЛЬЗУЕТСЯ и запись в комментарий mac адрес
                    print u"перевод в статус используется порта %s" % rec.port
                    device_port.status = port_use
                    device_port.comment = rec.macaddress
                    device_port.datetime_update = krsk_tz.localize(datetime.datetime.now())
                    device_port.save()



                    ### Проверка наличия одноименного с портом сетевого элемента логического интерфейса, связь между интерфейсом и портом
                    if not ne.logical_interfaces_set.filter(name=rec.port).exists():
                        print u"создание логического интерфейса %s" % rec.port
                        ### Создание логического интерфейса
                        li = logical_interfaces.objects.create(
                            name = rec.port,
                            netelem = ne,
                            comment = rec.macaddress
                        )
                        li.ports.add(device_port)

                elif device.devices_combo_set.filter(num=rec.port).exists():

                    device_combo = device.devices_combo_set.get(num=rec.port)
                    ### Перевод порта в статус ИСПОЛЬЗУЕТСЯ и запись в комментарий mac адрес
                    print u"перевод в статус используется combo %s" % rec.port
                    device_port.status_port = port_use
                    device_port.comment = rec.macaddress
                    device_port.datetime_update = krsk_tz.localize(datetime.datetime.now())
                    device_port.save()


                else:
                    logger.info("Порт {port} не найден на устройстве {ipaddress}".format(port=rec.port,ipaddress=rec.ipaddress))


            ### ip адрес не найден
            else:
                logger.info("IP адрес {ipaddress} не найден!".format(ipaddress=rec.ipaddress))
