#!coding:utf-8

from django.contrib import admin
from iss.regions.models import store_list, status_avr


class StoreAdmin(admin.ModelAdmin):

    fields = ('region','comment')
    list_display = ('name', 'region', 'comment')


class StatusAVRAdmin(admin.ModelAdmin):

    fields = ('name','emails', 'allow', 'stuff', 'price')
    list_display = ('id', 'name', 'emails', 'allow', 'stuff', 'price')





admin.site.register(store_list, StoreAdmin)
admin.site.register(status_avr, StatusAVRAdmin)


