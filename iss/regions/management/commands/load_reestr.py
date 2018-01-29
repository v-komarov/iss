#coding:utf8

import csv
import decimal
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import numpy as np

from django.contrib.auth.models import User
from iss.localdicts.models import regions, address_city
from iss.regions.models import reestr_proj, reestr_proj_comment
from iss.localdicts.models import init_reestr_proj, stages

krsk = regions.objects.get(name='Красноярск')
#irk = regions.objects.get(name='Иркутск')
#chi = regions.objects.get(name='Чита')




class Command(BaseCommand):
    args = '< >'
    help = 'Загрузка ререстра по регионам'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        df = pd.read_excel("iss/regions/xls/reestr.xlsx")

        user = User.objects.get(username="oshalygina")

        for index,row in df.iterrows():

            kod = row[4]


            other = row[7]
            cod = kod.split('/')


            print '/'.join(cod)

            pr = reestr_proj.objects.filter(proj_kod__icontains=cod[1],id__gte=250,id__lte=345)
            pr =  pr.first() if pr.exists() else None

            if pr:
                comment = pr.comment + " %s" % other
                pr.comment = comment
                pr.save()



