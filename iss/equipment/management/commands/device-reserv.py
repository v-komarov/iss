#coding:utf8

import logging
import datetime
from django.utils import timezone
from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import devices, devices_ports, devices_slots, devices_combo, devices_statuses
from iss.localdicts.models import port_status,device_status,slot_status


logger = logging.getLogger('devices')



port_rez = port_status.objects.get(name='Резерв')
port_use = port_status.objects.get(name='Используется')
port_tech = port_status.objects.get(name='Технологический')
slot_use = slot_status.objects.get(name='Используется')
slot_rez = slot_status.objects.get(name='Резерв')

device_use = device_status.objects.get(name='Используется')
device_store = device_status.objects.get(name='Хранение')

predel = timezone.now() - datetime.timedelta(days=90)



class Command(BaseCommand):
    args = '< >'
    help = 'Установка статуса резерв для устройст если порты , слоты , комбо не используются'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Установка статуса резерв для устройст если порты , слоты , комбо не используются

        """

        ### Обход устройств
        for device in devices.objects.filter(status=device_use):

            # Проверка портов
            ports = devices_ports.objects.filter(Q(device=device) & (Q(status=port_use) | Q(status=port_tech))).count()

            # Проверка слотов
            slots = devices_slots.objects.filter(Q(device=device) & Q(status=slot_use)).count()

            # Проверка комбо
            combo = devices_combo.objects.filter(Q(device=device) & (Q(status_port=port_use) | Q(status_port=port_tech))).count()

            if (ports + slots + combo) == 0:
                """Установка статуса резерв для устройства"""
                devices_statuses.objects.create(
                    device=device,
                    author="device-reserv",
                    comment="dosnt have any fact of using",
                    status=device_store
                )

                device.status = device_store
                device.save()

                logger.info(u"Устройство {} серийный номер {} установлен статус {}".format(device.name, device.serial, device.status))



        """
        Проверка резервных устройств и подготовка их к удалению
        
        """
        for device in devices.objects.filter(status=device_store):
            # Проверка даты установки последнего статуса
            if devices_statuses.objects.filter(status=device_store).exists():
                if devices_statuses.objects.filter(status=device_store).order_by("datetime_create").last() < predel:
                    # Удаление связи с сетевым элементом
                    for ne in device.netelems_set.all():
                        ne.device.remove(device)
                    #device.relations.through.objects.all().delete()

                    logger.info(u"Устройство {} серийный номер {} подготовлено к удалению".format(device.name, device.serial))
