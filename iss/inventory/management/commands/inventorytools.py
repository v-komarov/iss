#coding:utf8

import csv
import json
from django.core.management.base import BaseCommand, CommandError
from iss.inventory.models import devices,devices_scheme,netelems,logical_interfaces,logical_interfaces_prop
from iss.localdicts.models import device_status,logical_interfaces_prop_list


class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        """
        for row in devices.objects.filter(serial='12345678'):

            print row
            row.clearenv()
            #if len(row.data["descr"]) < 50:
            #    if devices_scheme.objects.filter(name=row.data["descr"]).count() == 0:
            #        devices_scheme.objects.create(name=row.data["descr"])
        """

        ### Установка модели для устройств по ip адресам
        """
        a = {}

        with open('aaa.csv','rb') as csvfile2:

            spamreader2 = csv.reader(csvfile2, delimiter=';')

            for row in spamreader2:
                a[row[0]] = row[1]



        with open('zzz.csv', 'rb') as csvfile:

            #namelist = []

            spamreader = csv.reader(csvfile, delimiter=';')

            for row in spamreader:
                device_name = row[0].rstrip()
                if a.has_key(device_name):
                    scheme_id = a[device_name]
                    scheme = devices_scheme.objects.get(pk=scheme_id)
                    ipaddress = row[2]
                    devices.objects.filter(data__ipaddress=ipaddress).update(device_scheme=scheme)
        """

        ## Создание таблиц портов, слотов, комбо, свойств
        """
        for item in devices.objects.exclude(device_scheme=None):
            if not item.devices_ports_set.exists():
                item.mkports()
                print "ports",item
            if not item.device_link.exists():
                item.mkslots()
                print "slots",item
            if not item.devices_combo_set.exists():
                item.mkcombo()
                print "combo",item
            if not item.devices_properties_set.exists():
                item.mkprop()
                print "properties",item
        """

        """
        ## Создание сетевых элементов и связка с железом
        for item in devices.objects.exclude(device_scheme=None):
            if item.data.has_key("name") and item.data.has_key("ipaddress"):
                netelem_name = "%s (%s)" % (item.data["name"],item.data["ipaddress"])
                if not netelems.objects.filter(name=netelem_name).exists():
                    print netelem_name
                    ne = netelems.objects.create(name = netelem_name)
                    ne.device.add(item)
        """

        """
        ### Установка статуса устройства
        status = device_status.objects.get(pk=1)
        devices.objects.exclude(device_scheme=None).update(status=status)
        """

        ## Создание интерфейса управления
        prop = logical_interfaces_prop_list.objects.get(name='ipv4')
        for item in devices.objects.exclude(device_scheme=None):
            if item.data.has_key("name") and item.data.has_key("ipaddress"):
                ne = item.netelems_set.all()[0]
                print ne

                if not logical_interfaces.objects.filter(name='manage',netelem=ne).exists():
                    inter = logical_interfaces.objects.create(
                        name = 'manage',
                        netelem = ne,
                        comment = 'Управление'
                    )
                #else:
                    #inter = logical_interfaces.objects.get(name='manage',netelem=ne)
                    #logical_interfaces_prop.objects.filter(logical_interface=inter).delete()

                    logical_interfaces_prop.objects.create(
                        logical_interface = inter,
                        prop = prop,
                        val = item.data["ipaddress"],
                        comment='Управление'
                    )
