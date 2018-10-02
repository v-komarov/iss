#!coding:utf-8

from django.contrib import admin
from iss.regions.models import store_list, status_avr, avr_commission


class StoreAdmin(admin.ModelAdmin):

    fields = ('region','comment')
    list_display = ('name', 'region', 'comment')


class StatusAVRAdmin(admin.ModelAdmin):

    fields = ('name','emails', 'allow', 'stuff', 'price')
    list_display = ('id', 'name', 'emails', 'allow', 'stuff', 'price')


class CommissionAVRAdmin(admin.ModelAdmin):

    fields = ('name','position', 'sign')
    list_display = ('id', 'name', 'position', 'sign')



admin.site.register(store_list, StoreAdmin)
admin.site.register(status_avr, StatusAVRAdmin)
admin.site.register(avr_commission, CommissionAVRAdmin)


