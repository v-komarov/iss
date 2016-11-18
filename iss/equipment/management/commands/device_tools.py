#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import agregators,scan_iplist,devices_ip,footnodes


class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        """
        filename = args[0]
        domen = args[1]


        with open(filename, 'r') as f:
            for row in f.readlines():
                scan_iplist.objects.create(ipaddress=row[:-1],device_domen=domen)

        f.close()
        """

        """
            Заполнение агрегаторов
        """

        fn = footnodes.objects.all()[0]

        for a in agregators.objects.all():

            ip = a.ipaddress

            if devices_ip.objects.filter(ipaddress=ip).count() == 1:
                d = devices_ip.objects.get(ipaddress=ip)
                a.footnode = fn
                a.chassisid = d.chassisid
                a.domen = d.device_domen
                a.name = d.device_name
                a.descr = d.device_descr
                a.location = d.device_location
                a.serial = d.device_serial
                a.save()


