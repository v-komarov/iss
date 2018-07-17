#coding:utf8

import datetime
from pytz import timezone
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from iss.blocks.models import block_managers, pay_period, contracts
from django.contrib.auth.models import User

import pandas as pd


### Соответствие переодичности оплаты
per = {
    u"разовый": 4,
    u"месяц": 1,
    u"квартал": 2,
    u"полугодие": 5,
    u"рамочный": 6
}



author = User.objects.get(username='vak') ### От чьего имени добавляем договор

manager = User.objects.get(username='oshalygina') ### Кто ответственный по договору



tz = 'Asia/Krasnoyarsk'
krsk_tz = timezone(tz)


class Command(BaseCommand):
    args = '< >'
    help = 'Загрузка договоров управляющих компаний'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """


        df = pd.read_excel('iss/blocks/csv/2017.xlsx',header=None,index_col=None)
        df.dropna(subset=[5], inplace=True)


        # Заполнение юридических адресов компаний
        for index, row in df.iterrows():

            if block_managers.objects.filter(inn__icontains=row[5]).exists():

                date_begin = krsk_tz.localize(datetime.datetime.strptime('01.01.2018','%d.%m.%Y')) if pd.isnull(row[17]) else krsk_tz.localize(datetime.datetime.strptime(row[17],'%d.%m.%Y')) ### Начало действия договора
                date_end = krsk_tz.localize(datetime.datetime.strptime('31.12.2018','%d.%m.%Y'))

                ### периодичность оплаты
                per_id = 6
                for k,v in per.items():
                    if pd.isnull(row[27]):
                        per_id = 6
                        break
                    elif row[27].find(k) != -1:
                        per_id = per[k]
                        break

                p = pay_period.objects.get(pk=per_id) ### Переодичность
                num = row[2] ## Номер договора
                goon = False if pd.isnull(row[32]) else True ## Пролонгация договора

                comment = "" if pd.isnull(row[33]) else row[33] ### Комментарий
                init = comment if pd.isnull(row[28]) else u"%s\nИнициатор: %s" % (comment,row[28]) ### Инициатор

                ### Добавление договора
                company = block_managers.objects.filter(inn__icontains=row[5]).first()

                contracts.objects.create(
                    company = company,
                    num = num,
                    date_begin = date_begin,
                    date_end = date_end,
                    goon = goon,
                    money = Decimal(0),
                    period = p,
                    user = author,
                    manager = manager,
                    comment = init
                )

                print row[2],row[5],p,date_begin,init

