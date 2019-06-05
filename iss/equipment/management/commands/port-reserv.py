#coding:utf8

import logging
import datetime
from django.utils import timezone
from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import devices, devices_ports, devices_slots, devices_combo
from iss.localdicts.models import port_status,device_status,slot_status


logger = logging.getLogger('ports')



port_rez = port_status.objects.get(name='Резерв')
port_use = port_status.objects.get(name='Используется')
port_tech = port_status.objects.get(name='Технологический')
slot_use = slot_status.objects.get(name='Используется')
slot_rez = slot_status.objects.get(name='Резерв')

device_use = device_status.objects.get(name='Используется')


predel = timezone.now() - datetime.timedelta(days=180)



class Command(BaseCommand):
    args = '< >'
    help = 'Отметка портов которые не используются 6 месяцев и более'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """
        Отметка резервных портов, комбо, слотов

        """

        ### Обход устройств
        for device in devices.objects.filter(status=device_use):


            ### Обход портов устройства
            for p in devices_ports.objects.filter(Q(device=device) & (Q(status=port_use) | Q(status=port_tech)) & Q(datetime_update__lte=predel)):

                print device, device.serial, p.num, p.status, p.datetime_update

                p.datetime_update = timezone.now()
                p.status = port_rez
                p.author = "port-reserv"
                p.comment = "havent used for 6 months"
                p.save()

                logger.info(u"Устройство {} серийный номер {} порт {} статус {}".format(device.name, device.serial, p.num, p.status))


            ### Обход слотов
            for st in devices_slots.objects.filter(Q(device=device) & Q(status=slot_use) & Q(datetime_update__lte=predel)):

                print device, device.serial, st.num, st.status, st.datetime_update
                st.datetime_update = timezone.now()
                st.status = slot_rez
                st.author = "port-reserv"
                st.comment = "havent used for 6 months"
                st.save()

                logger.info(u"Устройство {} серийный номер {} слот {} статус {}".format(device.name, device.serial, st.num, st.status))



            ### Обход комбо
            for p in devices_combo.objects.filter(Q(device=device) & (Q(status_port=port_use) | Q(status_port=port_tech)) & Q(datetime_update__lte=predel)):

                print device, device.serial, p.num, p.status_port, p.datetime_update

                p.datetime_update = timezone.now()
                p.status_port = port_rez
                p.author = "port-reserv"
                p.comment = "havent used for 6 months"
                p.save()

                logger.info(u"Устройство {} серийный номер {} порт {} статус {}".format(device.name, device.serial, p.num, p.status_port))


