#coding:utf8

import csv
import decimal
from django.core.management.base import BaseCommand, CommandError

from iss.localdicts.models import regions
from iss.regions.models import orders


krsk = regions.objects.get(name='Красноярск')
irk = regions.objects.get(name='Иркутск')
chi = regions.objects.get(name='Чита')




class Command(BaseCommand):
    args = '< >'
    help = 'Загрузка заказов ТМЦ по регионам'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """




        with open('iss/regions/csv/tmc_chi.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";", quotechar='"')
            next(spamreader, None)
            for row in spamreader:
                order = row[0]
                marka = row[1]
                name = row[2]
                ed = row[3]
                b2b_b2o = 0 if len(row[5]) == 0 else int(decimal.Decimal(row[5].replace(",",".")))
                investment = 0 if len(row[6]) == 0 else int(decimal.Decimal(row[6].replace(",",".")))
                to = 0 if len(row[7]) == 0 else int(decimal.Decimal(row[7].replace(",",".")))
                comment = row[8]

                count = b2b_b2o + investment + to

                region = chi


                print "%s %s %s %s %s" % (order,marka,name,ed, b2b_b2o)


                if not orders.objects.filter(order=order,region=region).exists():
                    orders.objects.create(
                        region = region,
                        order = order,
                        model = marka,
                        name = name,
                        ed = ed,
                        count = count,
                        price = 0,
                        rowsum = 0,
                        b2b_b2o = b2b_b2o,
                        investment = investment,
                        to = to,
                        comment = comment
                    )
