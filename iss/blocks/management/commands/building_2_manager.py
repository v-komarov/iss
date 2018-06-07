#coding:utf8

from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from django.db.models.functions import Length, Upper, Lower

from iss.localdicts.models import address_city
from iss.localdicts.models import address_street
from iss.localdicts.models import address_house
from iss.blocks.models import buildings, block_managers
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


        ### Привязка дома к управляющей компании


        df = pd.read_csv('iss/blocks/csv/buildings.csv',sep=';',header=0,index_col=0)
        df.dropna(subset=['formalname_city','formalname_street','house_number'], inplace=True)

        for index, row in df.iterrows():

            city = row["formalname_city"].decode("utf-8")
            if city in (u"Красноярск",u"Овсянка",u"Слизнево",u"Молодежный",u"Дивногорск") and not pd.isnull(row["management_organization_id"]):

                id_house = index # id дома
                print int(row["management_organization_id"])
                if block_managers.objects.filter(www_id=int(row["management_organization_id"])).exists():
                    print "Компания найдена"
                    manager = block_managers.objects.get(www_id=int(row["management_organization_id"]))
                    print manager, id_house
                    house = buildings.objects.get(www_id=id_house)
                    house.block_manager = manager
                    house.save()
                else:
                    print "Компания не найдена!"


