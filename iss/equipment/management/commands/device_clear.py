#coding:utf8

import logging
import json
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer,TopicPartition
from transliterate import translit, get_available_language_codes

from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Upper

from iss.inventory.models import devices, devices_scheme, netelems, logical_interfaces_prop_list, device_status, logical_interfaces, logical_interfaces_prop, devices_removal, devices_statuses



logger = logging.getLogger('devices')





### Определение наиболее "древнего" устройства
def Oldest(dev1,dev2):

    if dev1.datetime_create == None:
        return dev1

    if dev2.datetime_create == None:
        return dev2

    if dev1.datetime_create >= dev2.datetime_create:
        return dev2
    else:
        return dev1




class Command(BaseCommand):
    args = '<devices ...>'
    help = 'clear devices and netelems'

    """
    Удаление устройств и сетевых элементов
    
    Правила удаления:
    
    1. Удаление устройств без связи с сетевым элементом
    2. Удаление сетевых элементов без связи с устройством
    3. Удаление устройств с отсутствием набора портов
    4. Удаление дублей устройств у одного сетевого элемента. 
       Критерий - время создания устройства.
       Удаляется более раннее созданное устройство.
    
    """

    def handle(self, *args, **options):


        n = 1
        n2 = 1
        ### Удаление устройств без связи с сетевым элементом
        for dev in devices.objects.all():

            ### Проверка есть ли связанный сетевой элемент
            if not dev.netelems_set.all().exists():
                devices_statuses.objects.filter(device=dev).delete()
                devices_removal.objects.filter(device=dev).delete()
                dev.clearenv()
                print u"Устройство {} serial: {} не связано с сетевым элементом : удаление портов, слотов, комбо".format(dev.name, dev.serial)
                logger.info(u"Устройство {} serial: {} не связано с сетевым элементом : удаление портов, слотов, комбо".format(dev.name, dev.serial))


            ### Удаление устройств с пустым набором портов
            if dev.get_ports_count() == 0 and dev.get_combo_count() == 0 and dev.get_slots_count() == 0:
                n += 1
                dev.clearenv()
                dev.delete()
                print u"Устройство {} serial: {} не имеет набора портов слотов или комбо : удаление {}".format(dev.name, dev.serial, n)
                logger.info(u"Устройство {} serial: {} не имеет набора портов слотов или комбо : удаление {}".format(dev.name, dev.serial, n))


        ### Удаление сетевых элементов без связи с устройством
        for net in netelems.objects.all():

            ### Проверка есть ли связанные устройства
            if not net.device.all().exists():
                n2 += 1
                for li in logical_interfaces.objects.filter(netelem=net):
                    li.ports.clear()
                    logical_interfaces_prop.objects.filter(logical_interface=li).delete()
                    li.delete()
                net.delete()
                print u"Сетевой элемент {} не имеет связанного устройства : удаление {}".format(net.name, n2)
                logger.info(u"Сетевой элемент {} не имеет связанного устройства : удаление {}".format(net.name, n2))



        ### Удаление дубля устройств у сетевого элемента
        for net in netelems.objects.all():

            ### Проверка сколько связанных устройств
            if net.device.all().count() > 1:

                ### таких элементов два и более

                ### Проверка по серийным номерам
                dev1 = net.device.all()[0]
                dev2 = net.device.all()[1]

                ### Определение наиболее раннего добавленного устройства
                old = Oldest(dev1,dev2)

                ### Удаление связи между старым устройством и сетевым элементом
                net.device.remove(old)

                print u"Удален дубль {} сетевого элемента {}".format(old.name, net.name)
                logger.info(u"Удален дубль {} сетевого элемента {}".format(old.name, net.name))

