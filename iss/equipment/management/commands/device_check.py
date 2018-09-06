#coding:utf8

import logging
import json
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer,TopicPartition
from transliterate import translit, get_available_language_codes

from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions import Upper

from iss.inventory.models import devices
from iss.localdicts.models import address_house, address_city, address_street

import iss.dbconn

logger = logging.getLogger('devices')



kafka_server = iss.dbconn.KAFKA_SERVER
elsearch_server = iss.dbconn.ELASTICSEARCH


consumer = KafkaConsumer('devices',bootstrap_servers=kafka_server, auto_offset_reset='earliest')
es = Elasticsearch(elsearch_server)



def find_model(d):

    """
     Поиск модели

    """
    q = {"query": {"match_phrase": {"synonyms": d["model"]}}}
    res = es.search(index="iss2", doc_type="device", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]
        return result
        #break
    else:
        print u"ElasticSearch Не найден: %s" % d["model"]
        logger.info(u"ElasticSearch Не найден {} {}".format(d["model"], d["ip"]))

        return False




def find_city(city):

    """
    Поиск города в ElasticSearch

    :param d:
    :return:
    """

    q = {"query": {"match_phrase": {"synonyms": city}}}
    res = es.search(index="iss2", doc_type="city", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]

        print "city_id %s" % result
        return address_city.objects.get(pk=int(result,10))

    else:
        print u"ElasticSearch Не найден: %s" % city
        logger.info(u"ElasticSearch Не найден город {}".format(city))

        return False






def find_street(street):

    """
    Поиск улицы в ElasticSearch

    :param d:
    :return:
    """

    q = {"query": {"match_phrase": {"synonyms": street}}}
    res = es.search(index="iss2", doc_type="street", body=q)
    for hit in res['hits']['hits']:
        result = "%(id)s" % hit["_source"]
        print "street_id %s" % result
        return address_street.objects.get(pk=int(result,10))

    else:
        print u"ElasticSearch Не найден: %s" % street
        logger.info(u"ElasticSearch Не найдена улица {}".format(street))

        return False




def find_address(d):

    """
    Поиск адреса

    :param d:
    :return:
    """

    address = d["location"].split("/")

    ### Случай полного адреса
    if len(address) == 4:

        city_obj = find_city(address[1])
        street_obj = find_city(address[2])
        house = translit(address[3], 'ru').upper()

        if not city_obj == False and not street_obj == False:

            if address_house.objects.all().annotate(house_upper=Upper("house")).filter(city=city_obj, street=street_obj, house_upper=house).exists():
                address = address_house.objects.all().annotate(house_upper=Upper("house")).filter(city=city_obj, street=street_obj, house_upper=house).first()

                return address





    ### Адрес из города и улицы
    elif len(address) == 3:

        city_obj = find_city(address[1])
        street_obj = find_city(address[2])

        if not city_obj == False and not street_obj == False:

            if address_house.objects.filter(city=city_obj, street=street_obj, house=None).exists():
                address = address_house.objects.filter(city=city_obj, street=street_obj, house=None).first()

                return address





    ### Адрес из города
    elif len(address) == 2:

        city_obj = find_city(address[1])

        if not city_obj == False:

            if address_house.objects.filter(city=city_obj, street=None, house=None).exists():
                address = address_house.objects.filter(city=city_obj, street=None, house=None).first()

                return address



    print u"Не найден адрес: %s" % d["location"]
    logger.info(u"Не найден адрес {}".format(d["location"]))

    return False






class Command(BaseCommand):
    args = '<devices ...>'
    help = 'check data of device'

    """
    Читает топик devices с данными zenoss устройств,
    проверяет соответствие в базе данных инвентори 
    """

    def handle(self, *args, **options):

        for m in consumer:
            d = json.loads(m.value)
            model = find_model(d)
            address = find_address(d)

