#coding:utf8

import json
from django.core.management.base import BaseCommand, CommandError

from iss.inventory.models import devices




class Command(BaseCommand):
    args = '<tools ...>'
    help = 'stuff'




    def handle(self, *args, **options):

        # тестовая задача

        for row in devices.objects.all():
            if row.data.has_key("ipaddress"):
                print row.data["ipaddress"],row.data["name"]

