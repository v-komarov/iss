#!coding:utf-8

from django.contrib import admin
from iss.regions.models import store_list


class StoreAdmin(admin.ModelAdmin):

    fields = ('region','comment')
    list_display = ('name', 'region', 'comment')



admin.site.register(store_list, StoreAdmin)


