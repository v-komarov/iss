#coding:utf8

import logging
import csv
import datetime
from pytz import timezone

from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError

from elasticsearch import Elasticsearch

from iss.localdicts.models import address_city,address_street,address_house,address_companies,logical_interfaces_prop_list,device_status
from iss.inventory.models import devices_scheme,devices,netelems,logical_interfaces,logical_interfaces_prop


logger = logging.getLogger('loadding')

prop = logical_interfaces_prop_list.objects.get(name='ipv4')
devstatus = device_status.objects.get(name='Используется')
company = address_companies.objects.get(name='МР-Сибирь')


class Command(BaseCommand):
    args = '< >'
    help = 'Создание устройств и сетевых элементов Читинского региона'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """




        with open('iss/equipment/csv/loaddata_chi.csv') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=";")
            next(spamreader, None)
            for row in spamreader:
                ip = row[1]
                name = row[2]
                house = row[3]
                serial = row[4]
                modelid = row[7]
                cityid = row[5]
                streetid = row[6]


                if modelid and serial != "":

                    print ip,name,house,serial,modelid,cityid,streetid

                    #### Создание адреса
                    city = address_city.objects.get(pk=int(cityid,10))
                    street = address_street.objects.get(pk=int(streetid,10))

                    ### Проверка есть ли такой адрес
                    if address_house.objects.filter(city=city,street=street,house=house).exists():
                        addr = address_house.objects.filter(city=city,street=street,house=house)[0]
                    else:
                        addr = address_house.objects.create(
                            city=city,
                            street=street,
                            house=house
                        )

                    #### Проверка наличия оборудования по серийному номеру
                    model = devices_scheme.objects.get(pk=int(modelid,10))
                    if devices.objects.filter(serial=serial).exists():
                        dev = devices.objects.filter(serial=serial).first()
                    else:
                        dev = devices.objects.create(
                            name=model.name,
                            serial=serial,
                            company=company,
                            address=addr,
                            device_scheme=model,
                            status=devstatus
                        )

                        ### Создание портов, комбо, слотов
                        dev.mkports(author="was loaded data")
                        dev.mkslots(author="was loaded data")
                        dev.mkcombo(author="was loaded data")
                        dev.mkprop(author="was loaded data")

                    ### Проверка наличия сетевого элемента
                    if netelems.objects.filter(name=name).exists():
                        ne = netelems.objects.filter(name=name).first()
                    else:
                        ne = netelems.objects.create(name=name,author="was loaded data")

                    ### Проверка наличия интерфейса управления
                    if not ne.logical_interfaces_set.all().filter(name="manage").exists():
                        man = logical_interfaces.objects.create(name="manage",netelem=ne,comment='Управление')
                    else:
                        man = ne.logical_interfaces_set.all().filter(name="manage").first()


                    ### Проверка наличия ip адреса управления
                    if not logical_interfaces_prop.objects.filter(logical_interface=man,prop=prop,val=ip).exists():
                        logical_interfaces_prop.objects.create(
                            logical_interface=man,
                            prop=prop,
                            val=ip,
                            comment='Управление'
                        )

                    ### Проверка наличия связи устройств и сетевых элементов
                    if not dev.netelems_set.filter(pk=ne.id).exists():
                        ne.device.add(dev)