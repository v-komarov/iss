#!coding:utf-8
from django.contrib import admin

from iss.equipment.models import scan_iplist

class ScanIpList(admin.ModelAdmin):

    fields = ('ipaddress', 'device_domen', 'community', 'snmp_ver')
    list_display = ('ipaddress', 'device_domen', 'community', 'snmp_ver')
    list_filter = ('device_domen','community', 'snmp_ver')
    search_fields = ['ipaddress']



admin.site.register(scan_iplist,ScanIpList)

