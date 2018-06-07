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


        ### Загрузка данных по домам

        ### Определение названия улиц с использованием nltk
        import nltk
        from nltk.tokenize import MWETokenizer
        import string
        from nltk.corpus import stopwords

        tokenizer = MWETokenizer([
            (u'9', u'Мая'), (u'60', u'лет', u'СССР'), (u'Пионерская', u'Правда'),
            (u'78', u'Добровольческой', u'бригады'), (u'3',u'Августа'),
            (u'60', u'лет', u'Октября'), (u'Конституции', u'СССР'), (u'Маршела',u'Малиновского'),
            (u'7-я',u'Продольная'), (u'7-я',u'Полярная'), (u'11-я',u'Продольная'),
        ], separator=' ')



        df = pd.read_csv('iss/blocks/csv/buildings.csv',sep=';',header=0,index_col=0)
        df.dropna(subset=['formalname_city','formalname_street','house_number'], inplace=True)

        for index, row in df.iterrows():

            city = row["formalname_city"].decode("utf-8")
            if city in (u"Красноярск",u"Овсянка",u"Слизнево",u"Молодежный",u"Дивногорск"):

                ### Город
                if address_city.objects.filter(name__icontains=city).exists():
                    ## Исключения
                    if city in (u"Бор",):
                        ci = address_city.objects.get(name=city)
                    else:
                        ci = address_city.objects.get(name__contains=city)
                    #print ci.name,city,"город найден!"
                else:
                    print "Город не найден!",city
                    ci = address_city.objects.create(name=city)







                ### Определение улицы
                ul = row["formalname_street"].decode("utf-8").replace("."," ")

                tokens = nltk.word_tokenize(ul)
                tokens = tokenizer.tokenize(tokens)

                tokens = [i for i in tokens if (i not in string.punctuation)]
                stop_words = stopwords.words('russian')
                stop_words.extend([
                    u'Героя', u'Академика', u'Юрия',
                    u'Софьи', u'Ладо', u'газеты', u'Советского',
                    u'Алеши', u'Союза', u'Сергея', u'Анатолия', u'Ивана', u'Ады', u'Мате',
                    u'Карла', u'Петра', u'Космонавта', u'образования', u'Михаила', u'Дмитрия', u'СССР', u'Писателя',
                    u'Маршела', u'Любы', u'П', u'И', u'Н', u'Лиды', u'Дружинника', u'Бориса', u'Братьев', u'Зои'
                ])
                tokens = [i for i in tokens if (i not in stop_words)]



                ### Определение дома
                tokenizer2 = MWETokenizer([
                ], separator=' ')

                house = row["house_number"].decode("utf-8")
                #house = "%s%s" % (house.lower(),row["letter"].lower().decode("utf-8")) if not pd.isnull(row["letter"]) else house

                tokens2 = nltk.word_tokenize(house)
                tokens2 = tokenizer2.tokenize(tokens2)

                tokens2 = [i for i in tokens2 if (i not in string.punctuation)]
                stop_words2 = stopwords.words('russian')
                stop_words2.extend([
                    u'кор', u'\'', u'дом', u'01.05.14г', u'корпус', u'литер', u'дубль', u'корпусА',
                ])
                tokens2 = [i for i in tokens2 if (i not in stop_words2)]

                house1 = tokens2[0]
                if len(tokens2)>1:
                    house2 = tokens2[1].replace("8,9","/8").replace("'","").replace("`","")
                    ### Поиск чисел
                    if not re.findall("\d+", house2) == []:
                        house1 = "%s/%s" % (house1,house2)
                    else:
                        house1 = "%s%s" % (house1,house2)


                ### Номер строения
                block = row["block"].decode("utf-8") if not pd.isnull(row["block"]) else ""



                if re.match(r"\d+", block):
                    house1 = "%s/%s" % (house1, block)
                elif re.match(r"\w+", block):
                    house1 = "%s%s" % (house1, block)

                #print house1.lower()


                # Поиск улиц в справочнике
                if address_street.objects.filter(name__icontains=tokens[0]).exists():

                    street = address_street.objects.filter(name__icontains=tokens[0]).order_by(Length('name').asc()).first()


                    ### Поиск адреса
                    if address_house.objects.annotate(house2=Lower('house')).filter(city=ci, street=street, house2=house1.lower()).exists():
                        print "Адрес найден"
                        address = address_house.objects.annotate(house2=Lower('house')).filter(city=ci, street=street, house2=house1.lower()).order_by(Length('house').asc()).first()

                        mng = buildings.objects.get(www_id=index)
                        mng.address = address
                        mng.save()


                    else:
                        print "Адрес не найден!"
                        mng = buildings.objects.get(www_id=index)
                        mng.address = None
                        mng.save()

                        # Добавление отсутствующего адреса
                        address_house.objects.create(city=ci,street=street,house=house1.lower())



                else:
                    print "Не найдена", tokens[0], ul
                    address_street.objects.create(name=ul)






