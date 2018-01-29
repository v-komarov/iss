#coding:utf8

import urllib,urllib2

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.db.models import Q
from django import template


from iss.localdicts.models import address_house









class Command(BaseCommand):
    args = '<...>'
    help = 'check full address and create'



    def handle(self, *args, **options):

        for addr in address_house.objects.exclude(street=None).exclude(city=None):
            print addr.city, addr.street
            addr.common_address()


