#coding:utf8

import json
from django.core.management.base import BaseCommand, CommandError
from iss.inventory.models import devices,devices_scheme



class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        ### Формирование справочника devices_scheme

        for row in devices.objects.all():
            if len(row.data["descr"]) < 50:
                if devices_scheme.objects.filter(name=row.data["descr"]).count() == 0:
                    devices_scheme.objects.create(name=row.data["descr"])



