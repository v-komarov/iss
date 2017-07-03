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

        for street in address_street.objects.all():
            data = {
                'id': street.id,
                'name': street.name
            }

            res = es.index(index="iss2", doc_type='street', id=street.id, body=data)
            es.indices.refresh(index="iss2")
            #print res['created']


        """


        """
        for city in address_city.objects.all():
            data = {
                'id': city.id,
                'name': city.name
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

        q = {"query": {"match": {"name": {"query": "маркса","fuzziness":1}}}}
        #q = {"query": {"fuzzy": {"name": {"value": "краснорск", "boost":1.0, "fuzziness":0, "prefix_length":0, "max_expansions": 100 }}}}
        #q = {"query": {"term": {"name": "г.Красноярск" }}}


        res = es.search(index="iss2", doc_type="street", body=q)

        #print res
        for hit in res['hits']['hits']:
            #print hit
            print "%(name)s" % hit["_source"]
            #print "%s" % hit["_id"]




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
