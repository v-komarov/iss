#coding:utf8

from django.core.management.base import BaseCommand, CommandError


from django.db.models import Func, F, Value, IntegerField
from django.db.models.functions import Length, Upper

from iss.localdicts.models import address_city
from iss.localdicts.models import address_street
from iss.localdicts.models import address_house
from iss.blocks.models import block_managers
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

        """
        ### Словарь прямого соответствия улиц
        uls = {
            'Солнечный Бульвар': 'Солнечный',
            'Калинина': 'Калинина',
            '9 Мая': '9 Мая',
            'мкр. Авиаторов':'Авиаторов',
            '52 Квартал':'52 Квартал'

        }


        df = pd.read_csv('iss/blocks/csv/companies.csv',sep=';',header=None,index_col=0)


        # Заполнение юридических адресов компаний
        for index, row in df.iterrows():

            city = row[7].split(',')[0].split()[-1].strip()
            ### Город
            if address_city.objects.filter(name__icontains=city).exists():
                ci = address_city.objects.get(name__icontains=city)
            else:
                ci = address_city.objects.create(name=city)


            ### Определение улицы
            ul = row[7].split(',')[1].split()[-1]
            if uls.has_key(ul):
                street = address_street.objects.get(name=uls[ul])
            else:
                ul = ul.split('.')[-1] if ul.find('.') != -1 else ul
                street = address_street.objects.filter(name__icontains=ul)[0]


            house = ''
            if len(row[7].split(',')) > 2:
                house = row[7].split(',')[2].split('.')[1].replace('"', '').replace(' ', '')
                lit = re.search('стр. (\w*)', row[7]).group(1) if re.search('стр. (\w*)', row[7]) else ''
                house = "%s/%s" % (house, lit) if lit != '' else house

            if address_house.objects.filter(city=ci, street=street, house=house.lower()).exists():

                address = address_house.objects.filter(city=ci, street=street, house=house.lower())[0]
                #print address.city, address.street, address.house
                #mng = block_managers.objects.get(www_id=index)
                #mng.address_law = address
                #mng.save()

            else:
                print index, row[7], ul
                #print ci,street,house
        """


        """
        ### Для заполнения юридического адреса управляющих компаний

        ### Определение названия улиц с использованием nltk
        import nltk
        from nltk.tokenize import MWETokenizer
        import string
        from nltk.corpus import stopwords

        tokenizer = MWETokenizer([
            (u'9', u'Мая'), (u'60', u'лет', u'СССР'), (u'Пионерская', u'Правда'),
            (u'78', u'Добровольческой', u'бригады'), (u'3',u'Августа'),
            (u'60', u'лет', u'Октября'), (u'Конституции', u'СССР', u'Маршала', u'Площадь')
        ], separator=' ')

        df = pd.read_csv('iss/blocks/csv/companies.csv',sep=';',header=None,index_col=0)

        for index, row in df.iterrows():

            city = row[7].split(',')[0].split()[-1].strip()
            ### Город
            if address_city.objects.filter(name__icontains=city).exists():
                ci = address_city.objects.get(name__icontains=city)
            else:
                ci = address_city.objects.create(name=city)

            ### Определение улицы
            ul = " ".join(row[7].split(',')[1].split('.')).decode("utf-8")
            tokens = nltk.word_tokenize(ul)
            tokens = tokenizer.tokenize(tokens)

            tokens = [i for i in tokens if (i not in string.punctuation)]
            stop_words = stopwords.words('russian')
            stop_words.extend([
                u'ул', u'б-р', u'пр-кт', u'пер', u'проезд',u'Е.',u'Д.', u'Героя', u'Академика',
                u'Е', u'Д', u'Софьи', u'Ладо', u'Н', u'П', u'И', u'Б', u'В', u'газеты', u'Советского',
                u'Алеши', u'Союза', u'Сергея', u'А', u'Анатолия', u'Я', u'Ивана', u'Ады', u'Мате', u'М',
                u'Карла', u'Петра', u'Космонавта', u'д', u'З', u'образования', u'Михаила', u'Дмитрия', u'СССР', u'Писателя',
                u'Наб.'
            ])
            tokens = [i for i in tokens if (i not in stop_words)]

            ### Определение дома
            house = ''
            if len(row[7].split(',')) > 2:
                house = row[7].split(',')[2].split('.')[1].replace('"', '').replace(' ', '')
                lit = re.search('стр. (\w*)', row[7]).group(1) if re.search('стр. (\w*)', row[7]) else ''
                lit2 = re.search('лит. (\w*)', row[7]).group(1) if re.search('лит. (\w*)', row[7]) else ''
                house = "%s%s" % (house, lit2)
                house = "%s/%s" % (house, lit) if lit != '' else house



            # Поиск улиц в справочнике
            if address_street.objects.filter(name__icontains=tokens[0]).exists():

                street = address_street.objects.filter(name__icontains=tokens[0]).order_by(Length('name').asc()).first()


                ### Поиск адреса
                if address_house.objects.filter(city=ci, street=street, house=house.lower()).exists():

                    address = address_house.objects.filter(city=ci, street=street, house=house.lower()).first()
                    #print address.city, address.street, address.house
                    mng = block_managers.objects.get(www_id=index)
                    mng.address_law = address
                    mng.save()

                else:
                    print "Адрес не найден!", index, row[7], house
                    mng = block_managers.objects.get(www_id=index)
                    mng.address_law = None
                    mng.save()

                    # Добавление отсутствующего адреса
                    address_house.objects.create(city=ci,street=street,house=house.lower())



            else:
                print "Не найдена", ul
                address_street.objects.create(name=tokens[0])



            #print "%s\t%s" % (tokens[0], ul)
        """





        ### Для заполнения физического адреса управляющих компаний

        ### Определение названия улиц с использованием nltk
        import nltk
        from nltk.tokenize import MWETokenizer
        import string
        from nltk.corpus import stopwords

        tokenizer = MWETokenizer([
            (u'9', u'Мая'), (u'60', u'лет', u'СССР'), (u'Пионерская', u'Правда'),
            (u'78', u'Добровольческой', u'бригады'), (u'3',u'Августа'),
            (u'60', u'лет', u'Октября'), (u'Конституции', u'СССР', u'Маршала', u'Площадь')
        ], separator=' ')

        df = pd.read_csv('iss/blocks/csv/companies.csv',sep=';',header=None,index_col=0)

        for index, row in df.iterrows():

            if type(row[8])==type(str()):


                city = row[8].split(',')[0].split()[-1].strip()

                ### Город
                if address_city.objects.filter(name__icontains=city).exists():
                    ## Исключения
                    if city == "Бор":
                        ci = address_city.objects.get(name=city)
                    else:
                        ci = address_city.objects.get(name__contains=city)
                else:
                    print "Город не найден"
                    ci = address_city.objects.create(name=city)

                ### Определение улицы
                ul = " ".join(row[7].split(',')[1].split('.')).decode("utf-8")
                tokens = nltk.word_tokenize(ul)
                tokens = tokenizer.tokenize(tokens)

                tokens = [i for i in tokens if (i not in string.punctuation)]
                stop_words = stopwords.words('russian')
                stop_words.extend([
                    u'ул', u'б-р', u'пр-кт', u'пер', u'проезд',u'Е.',u'Д.', u'Героя', u'Академика',
                    u'Е', u'Д', u'Софьи', u'Ладо', u'Н', u'П', u'И', u'Б', u'В', u'газеты', u'Советского',
                    u'Алеши', u'Союза', u'Сергея', u'А', u'Анатолия', u'Я', u'Ивана', u'Ады', u'Мате', u'М',
                    u'Карла', u'Петра', u'Космонавта', u'д', u'З', u'образования', u'Михаила', u'Дмитрия', u'СССР', u'Писателя',
                    u'Наб.'
                ])
                tokens = [i for i in tokens if (i not in stop_words)]

                ### Определение дома
                house = ''
                if len(row[7].split(',')) > 2:
                    house = row[7].split(',')[2].split('.')[1].replace('"', '').replace(' ', '')
                    lit = re.search('стр. (\w*)', row[7]).group(1) if re.search('стр. (\w*)', row[7]) else ''
                    lit2 = re.search('лит. (\w*)', row[7]).group(1) if re.search('лит. (\w*)', row[7]) else ''
                    house = "%s%s" % (house, lit2)
                    house = "%s/%s" % (house, lit) if lit != '' else house



                # Поиск улиц в справочнике
                if address_street.objects.filter(name__icontains=tokens[0]).exists():

                    street = address_street.objects.filter(name__icontains=tokens[0]).order_by(Length('name').asc()).first()


                    ### Поиск адреса
                    if address_house.objects.filter(city=ci, street=street, house=house.lower()).exists():

                        address = address_house.objects.filter(city=ci, street=street, house=house.lower()).first()
                        #print address.city, address.street, address.house
                        mng = block_managers.objects.get(www_id=index)
                        mng.address = address
                        mng.save()

                    else:
                        print "Адрес не найден!", index, row[7], house
                        mng = block_managers.objects.get(www_id=index)
                        mng.address = None
                        mng.save()

                        # Добавление отсутствующего адреса
                        address_house.objects.create(city=ci,street=street,house=house.lower())



                else:
                    print "Не найдена", ul
                    #address_street.objects.create(name=tokens[0])



                #print "%s\t%s" % (tokens[0], ul)
