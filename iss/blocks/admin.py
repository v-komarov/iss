#!coding:utf-8

from django.contrib import admin
from iss.blocks.models import pay_period


class PayAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('id', 'name')


admin.site.register(pay_period, PayAdmin)


