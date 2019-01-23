#coding:utf8

from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from django.db.models.functions import Length, Upper, Lower

from iss.localdicts.models import address_city
from iss.localdicts.models import address_street
from iss.localdicts.models import address_house
from iss.blocks.models import buildings, block_managers
import re
import pandas as pd





def address_devices_ports(address):
    """Определение количества коммутаторов доступа и число занятых портов"""
    d = {}
    n,p = 0,0

    for dev in address.devices_set.all():
        n += 1
        p = p + dev.getzkl()
    d["devices"] = n
    d["ports"] = p
    return d





class Command(BaseCommand):
    args = '< >'
    help = 'Выгрузка данных по управляющим компаниям, коммутаторам доступа, занятым портам'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        filename = args[0]

        with open("iss/blocks/csv/%s" % filename, 'w') as f:

            f.write("КОМПАНИЯ;ГОРОД;УЛИЦА;ДОМ;КОЛ-ВО ОБОРУД.;ЗАНЯТЫХ ПОРТОВ\n")
            ## Список компаний
            for com in block_managers.objects.order_by("name"):
                for house in com.buildings_set.all():
                    d = address_devices_ports(house.address)
                    if not d["devices"] == 0:
                        street = house.address.street.name.encode('utf-8')
                        city = house.address.city.name.encode('utf-8')
                        h = house.address.house.encode('utf-8')
                        print com.name,city,street,h,d["devices"],d["ports"]
                        data = "{};{};{};{};{};{}\n".format(com.name.encode('utf-8'),city,street,h,d['devices'],d['ports'])
                        f.write(data)

