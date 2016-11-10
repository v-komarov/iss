#coding:utf8

from django.core.management.base import BaseCommand, CommandError
from iss.equipment.models import agregators,scan_iplist


class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        filename = args[0]
        domen = args[1]


        with open(filename, 'r') as f:
            for row in f.readlines():
                scan_iplist.objects.create(ipaddress=row[:-1],device_domen=domen)

        f.close()
