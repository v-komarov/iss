#coding:utf8

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

import nltk
from nltk.tokenize import MWETokenizer
import string
from nltk.corpus import stopwords
from django.contrib.auth.models import User
from pytz import timezone
from iss.localdicts.models import regions, address_city
from iss.regions.models import avr, avr_logs, status_avr

import iss.settings as settings

krsk_timezone = timezone("Asia/Krasnoyarsk")



krsk = regions.objects.get(name='Красноярск')
irk = regions.objects.get(name='Иркутск')
chi = regions.objects.get(name='Чита')


status = status_avr.objects.get(pk=1)


class Command(BaseCommand):
    args = '< >'
    help = 'Начальная загрузка актов АВР по регионам'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """






        df = pd.read_excel("iss/regions/csv/avr.xlsx", header=None, sheet_name=0, skiprows=[0])
        df.fillna("",inplace=True)
        #print df.head()
        for index, row in df.iterrows():
            region_find = row[1]
            city_find = row[2]
            objnet = row[3] # Объект сети
            address = row[5]
            comment = row[4]
            date_avr = row[7]
            date_carry = row[8] # дата выезда
            department = row[9] # подразделение
            staff_find = row[10] # МОЛ

            if city_find != "" and staff_find != "":

                tokenizer = MWETokenizer([
                    (u'Новый', u'Уоян'), (u'Новая', u'Чара'),
                ], separator=' ')

                ### Поиск по названию города
                tokens = nltk.word_tokenize(city_find)
                tokens = tokenizer.tokenize(tokens)

                tokens = [i for i in tokens if (i not in string.punctuation)]
                stop_words = stopwords.words('russian')
                stop_words.extend([
                    u'п', u'г',
                ])
                tokens = [i for i in tokens if (i not in stop_words)]

                if address_city.objects.filter(name__icontains=tokens[0]).exists():
                    city = address_city.objects.filter(name__icontains=tokens[0]).first()
                    print city
                else:
                    city = False
                    print u"Город %s не найден!" % city_find

                ### Поиск МОЛ по фамилии

                if User.objects.filter(last_name=staff_find.split()[0]).exists():
                    staff = User.objects.filter(last_name=staff_find.split()[0]).first()
                    print staff
                else:
                    staff = False
                    print u"Пользователь %s не найден!" % staff_find.split()[0]

                if city and staff:

                    user = User.objects.get(pk=1)

                    try:
                        date_work = krsk_timezone.localize(date_carry)
                    except:
                        date_work = None


                    ### Создание записей в базе
                    avr_obj = avr.objects.create(
                        region = irk,
                        city = city,
                        objnet = objnet,
                        address=address,
                        datetime_avr = krsk_timezone.localize(date_avr),
                        datetime_work = date_work,
                        status = status,
                        staff = staff,
                        author = user

                    )

                    ### Добавление коментариев
                    avr_logs.objects.create(
                        avr = avr_obj,
                        user = user,
                        action = department,
                        log = False
                    )

                    avr_logs.objects.create(
                        avr = avr_obj,
                        user = user,
                        action = comment,
                        log = False
                    )