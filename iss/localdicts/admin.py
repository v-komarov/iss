#!coding:utf-8

from django.contrib import admin
from iss.localdicts.models import TzList,Status,Severity

class StatusAdmin(admin.ModelAdmin):
    pass

class SeverityAdmin(admin.ModelAdmin):
    pass


admin.site.register(TzList)
admin.site.register(Status,StatusAdmin)
admin.site.register(Severity,SeverityAdmin)

