#coding:utf8

import csv
import decimal
from django.core.management.base import BaseCommand, CommandError

from iss.regions.models import store_rest, store_in, store_out, store_rest_log, store_carry, store_list






class Command(BaseCommand):
    args = '< >'
    help = 'Очистка всех записей складов'




    def handle(self, *args, **options):


        agry = args[0]


        """

        :param args:
        :param options:
        :return:
        """
        ### Дополнительный контроль для очистки
        if agry == "yes":

            store_rest_log.objects.all().delete()
            store_carry.objects.all().delete()
            store_in.objects.all().delete()
            store_out.objects.all().delete()
            store_rest.objects.all().delete()
            store_list.objects.all().delete()


            print "done"




