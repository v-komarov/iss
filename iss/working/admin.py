#!coding:utf-8
from django.contrib import admin
from iss.working.models import marks


class MarksAdmin(admin.ModelAdmin):

    fields = ('name', 'order')
    list_display = ('name', 'order')
    ordering = ['order',]


admin.site.register(marks, MarksAdmin)