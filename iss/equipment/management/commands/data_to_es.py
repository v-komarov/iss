#coding:utf8

import logging
import csv
import datetime
from pytz import timezone

from django.db.models import Q

from django.core.management.base import BaseCommand, CommandError

from elasticsearch import Elasticsearch

from iss.localdicts.models import address_city,address_street
from iss.inventory.models import devices_scheme


logger = logging.getLogger('loadding')




class Command(BaseCommand):
    args = '< >'
    help = 'Создание индекса в Elasticsearch'




    def handle(self, *args, **options):

        """

        :param args:
        :param options:
        :return:
        """

        """

        """
        es = Elasticsearch(['http://10.6.0.88:9200'])



        """
        ### Загрузка улиц
        for street in address_street.objects.all():
            data = {
                'id': street.id,
                'name': street.name
            }

            res = es.index(index="iss2", doc_type='street', id=street.id, body=data)
            es.indices.refresh(index="iss2")

        """










        """
        ### Загрузка городов
        for city in address_city.objects.all():

            c = city.name

            c = c.replace(u"пос.",u"")
            c = c.replace(u"пос. ",u"")
            c = c.replace(u"г.",u"")
            c = c.replace(u"г. ",u"")
            c = c.replace(u"пгт.",u"")
            c = c.replace(u"пгт. ",u"")
            c = c.replace(u"ст.",u"")
            c = c.replace(u"ст. ",u"")

            data = {
                'id': city.id,
                'name': c
            }

            res = es.index(index="iss2", doc_type='city', id=city.id, body=data)
            es.indices.refresh(index="iss2")
        """













        """
        q = {"query": {"fuzzy": {"name": "Телевызорная"}}}


        res = es.search(index="iss2", doc_type="street", body=q)

        for hit in res['hits']['hits']:
            print("%(name)s" % hit["_source"])
        """










        """
        ### Поиск названия населенных пунктов
        with open('iss/equipment/csv/irk_city_unique.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            next(spamreader, None)
            for row in spamreader:
                city = row[1]
                city = city.replace("ст. ","")
                city = city.replace("п. ","")

                q = {"query": {"match": {"name": {"query": city,"fuzziness":0}}}}
                #q = {"query": {"fuzzy": {"name": {"value": "краснорск", "boost":1.0, "fuzziness":0, "prefix_length":0, "max_expansions": 100 }}}}
                #q = {"query": {"term": {"name": "г.Красноярск" }}}


                res = es.search(index="iss2", doc_type="city", body=q)

                #print res
                result = []
                for hit in res['hits']['hits']:
                    r = "%s (%s)" % (hit["_source"]["name"],hit["_source"]["id"])
                    result.append(r)
                print "Поиск %s :" % city," ".join(result)

                ### Добавление в справочник
                if len(result) == 0:
                    print "Добавить %s" % city

        """











        ### Поиск названия улиц
        with open('iss/equipment/csv/irk_street_unique.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            next(spamreader, None)
            for row in spamreader:
                st = row[1]
                st = st.replace("пр. ","")
                st = st.replace("пр","")

                q = {"query": {"match": {"name": {"query": st,"fuzziness":0,"operator": "and"}}}}


                res = es.search(index="iss2", doc_type="street", body=q)

                #print res
                result = []
                for hit in res['hits']['hits']:
                    #r = u"%s (%s)" % (hit["_source"]["name"],hit["_source"]["id"])
                    result.append({
                        "id": hit["_source"]["id"],
                        "street": hit["_source"]["name"]
                    })
                if len(result) > 0:
                    #print st
                    #print result[0]["street"]
                    #print result[0]["id"]
                    print "{find};{street_id};".format(find=st,street_id=result[0]["id"])
                
                #if len(result) == 0:
                #    print row[1]
                #    if not address_street.objects.filter(name=row[1]).exists():
                #       address_street.objects.create(name=row[1])
                #elif len(result) == 1:
                #    print u"%s;%s;\n" % (row[1],result[0])
                #else:
                #    print u"%s;%s;\n" % (row[1],u" ".join(result))












        """
        for sch in devices_scheme.objects.all():
            data = {
                'id': sch.id,
                'name': sch.name,
                'ports': sch.get_ports_count(),
                'slots': sch.get_slots_count(),
                'combo': sch.get_combo_count()
            }

            res = es.index(index="iss2", doc_type='device_scheme', id=sch.id, body=data)
            es.indices.refresh(index="iss2")
        """

        #res = es.index(index="iss", doc_type='address', id=1, body={"name":"3 квартал"})
        #es.indices.refresh(index="iss")


        #q = {"query": {"fuzzy": {"name": {"value": "3", "boost":1.0, "fuzziness":6, "prefix_length":0, "max_expansions": 100 }}}}


        #res = es.search(index="iss", doc_type="address", body=q)

        #for hit in res['hits']['hits']:
        #    print("%(name)s" % hit["_source"])
