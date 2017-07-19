#coding:utf8

import csv
import decimal
from django.core.management.base import BaseCommand, CommandError

from iss.regions.models import orders






class Command(BaseCommand):
    args = '< >'
    help = 'Перенос теста из comment в tz'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        for row in orders.objects.all():
            if row.comment != "" and row.tz == "":
                row.tz = row.comment
                row.comment = ""
                row.save()




