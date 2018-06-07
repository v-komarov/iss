#coding:utf8

from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from django.db.models.functions import Length, Upper, Lower

from iss.localdicts.models import address_city
from iss.localdicts.models import address_street
from iss.localdicts.models import address_house
from iss.blocks.models import buildings
import re
import pandas as pd





class Command(BaseCommand):
    args = '< >'
    help = 'Загрузка данных с сайта реформа жкх'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """


        ### Загрузка данных по домам, без адреса


        df = pd.read_csv('iss/blocks/csv/buildings.csv',sep=';',header=0,index_col=0)
        df.dropna(subset=['formalname_city','formalname_street','house_number'], inplace=True)

        for index, row in df.iterrows():

            city = row["formalname_city"].decode("utf-8")
            if city in (u"Красноярск",u"Овсянка",u"Слизнево",u"Молодежный",u"Дивногорск"):

                www_id = index
                numstoreys = row["floor_count_max"] if not pd.isnull(row["floor_count_max"]) else 0 # Этажность
                numentrances = row["entrance_count"] if not pd.isnull(row["entrance_count"]) else 0 # количество подъездов
                numfloars = row["living_quarters_count"] if not  pd.isnull(row["living_quarters_count"]) else 0 # Количество квартир

                print www_id, int(numstoreys), int(numentrances), int(numfloars)

                buildings.objects.create(
                    www_id = www_id,
                    numstoreys = numstoreys,
                    numentrances = numentrances,
                    numfloars = numfloars
                )

