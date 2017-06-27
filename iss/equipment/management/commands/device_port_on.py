#coding:utf8

import logging
import datetime
from pytz import timezone

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import logical_interfaces_prop, netelems, devices, logical_interfaces, devices_ports
from iss.localdicts.models import logical_interfaces_prop_list,port_status,device_status
from iss.equipment.models import client_mac_log,client_login_log

logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
onyma = logical_interfaces_prop_list.objects.get(name='onyma')
port_use = port_status.objects.get(name='Используется')
device_use = device_status.objects.get(name='Используется')

tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '< >'
    help = 'Проверка портов оборудования (которые пользоваиельские), проверка соответствующего интерфейса, привязка номера договора к интерфейсу'




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

        ### Случайная выборка пользовательских портов устройств
        for port in devices_ports.objects.filter(status=port_use).order_by("?")[:100]:
            ### Устройство
            device = port.device
            ### Выволняем для устройств в статусе "используется"
            if device.status == device_use:
                ### Поиск связанных сетевых элементов
                for ne in device.netelems_set.all():
                    ### Для каждого сетевого элемента поиск одноименных с портом логических интерфейсов
                    if not ne.logical_interfaces_set.filter(name=port.num).exists():
                        ### Создание логического интерфейса, если такого не существует
                        li = logical_interfaces.objects.create(
                            name = port.num,
                            netelem = ne,
                            comment = 'was created by robot'
                        )

                        li.ports.add(port)

                    ### Поиск ip адреса управления
                    if ne.logical_interfaces_set.filter(name="manage").exists():
                        manage = ne.logical_interfaces_set.filter(name="manage").first()

                        ### Поиск ip адреса управления
                        if logical_interfaces_prop.objects.filter(logical_interface=manage,prop=prop).exists():
                            p = logical_interfaces_prop.objects.filter(logical_interface=manage, prop=prop).first()
                            ip = p.val

                            #### Поиск mac адреса по номеру порта и ip адресу
                            if client_mac_log.objects.filter(ipaddress=ip,port=port.num).exists():
                                mac = client_mac_log.objects.filter(ipaddress=ip,port=port.num).order_by('-create_update').first().macaddress

                                ### Поиск по mac адресу номера договора
                                if client_login_log.objects.filter(macaddress=mac).exclude(onyma_dogid=0).exists():

                                    dogcode = client_login_log.objects.filter(macaddress=mac).exclude(onyma_dogid=0).first().onyma_dogcode
                                    print dogcode

                                    ### Проверка - существует ли уже такой договор на этом логическом интерфейсе
                                    li = ne.logical_interfaces_set.all().filter(name=port.num).first()

                                    if not li.check_dogcode(dogcode):
                                        ### Добавление договора
                                        logical_interfaces_prop.objects.create(
                                            logical_interface = li,
                                            prop = onyma,
                                            val = dogcode,
                                            comment = "was added by robot"
                                        )

                                        print u"Добавлен договор %s" % dogcode
                                else:
                                    logger.info(
                                        "Не найден номер договора сетевого элемента {ne} , ip адрес {ip}, port {port}, mac {mac}".format(
                                            ne=ne.name, ip=ip, port=port.num, mac=mac))



                            else:
                                logger.info("Не найден mac адрес сетевого элемента {ne} , ip адрес {ip}, port {port}".format(ne=ne.name,ip=ip,port=port.num))



                        else:
                            logger.info("Не найден ip адрес управления сетевого элемента {ne}".format(ne=ne.name))



                    else:
                        logger.info("Не найден интерфейс управления сетевого элемнта {ne}".format(ne=ne.name))




