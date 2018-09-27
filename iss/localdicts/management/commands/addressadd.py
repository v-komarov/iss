#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q
from django.db.models.functions import Upper, Lower
from django import template


from iss.localdicts.models import address_house, address_city, address_street, address_companies









class Command(BaseCommand):
    args = '<...>'
    help = 'adding address'

    """
    Добавление адресов по наименованиям города, улицы, номера дома (разделенных двоеточием№ )
    
    """


    def handle(self, *args, **options):

        # Файл с даенными csv
        filename = args[0]


        with open(filename,"r") as f:
            for row in f.readlines():
                a = row.strip().split(":")

                city_str = a[0]
                street_str = a[1]
                house = a[2].decode("utf-8").lower().encode("utf-8")

                city = address_city.objects.get(name=city_str)
                street = address_street.objects.get(name=street_str)


                ## Проверка существования адреса
                if address_house.objects.all().annotate(house_lower=Lower("house")).filter(city=city,street=street,house_lower=house).exists():

                    print a[0], a[1], a[2].decode("utf-8").lower().encode("utf-8"), "**адрес существует**"

                else:
                    ## Создание адреса

                    address_house.objects.create(
                        city = city,
                        street = street,
                        house = house
                    )

                    print a[0], a[1], a[2].decode("utf-8").lower().encode("utf-8"), "**адрес создан**"
