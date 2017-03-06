#!coding:utf-8

from django.contrib import admin
from iss.localdicts.models import TzList,Status,Severity,accident_group,accident_list,accident_cats,address_city,address_street,address_house,address_companies,email_templates,address_templates,slots,ports,interfaces,port_status,slot_status

class StatusAdmin(admin.ModelAdmin):
    pass

class SeverityAdmin(admin.ModelAdmin):
    pass


class AccidentGroupAdmin(admin.ModelAdmin):

    fields = ('name', 'name_short')
    list_display = ('name', 'name_short')
    list_filter = ('name',)


class AccidentListAdmin(admin.ModelAdmin):

    fields = ('name', 'name_short','accident_group')
    list_display = ('name', 'name_short','accident_group')
    list_filter = ('name',)


class AccidentCatsAdmin(admin.ModelAdmin):

    fields = ('name', 'cat','accident')
    list_display = ('name', 'cat','accident')
    list_filter = ('name',)


class AddressCityAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)
    search_fields = ['name']


class AddressStreetAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)
    search_fields = ['name']



class AddressHouseAdmin(admin.ModelAdmin):

    fields = ('city','street','house','iss_address_id')
    list_display = ('city','street','house','iss_address_id')
    search_fields = ['street','city','house']
    list_filter = ('city','street')




class AddressCompaniesAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)




#class DevicesTypeAdmin(admin.ModelAdmin):
#
#    fields = ('name',)
#    list_display = ('name',)




class EmailTemplatesAdmin(admin.ModelAdmin):

    fields = ('name','address_list','template')
    list_display = ('name','address_list')



class AddressTemplatesAdmin(admin.ModelAdmin):

    fields = ('name','template')
    list_display = ('name',)



class SlotsAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)


class PortsAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)



class InterfacesAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)



class PortStatusAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)



class SlotStatusAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)




admin.site.register(TzList)
admin.site.register(Status,StatusAdmin)
admin.site.register(Severity,SeverityAdmin)
admin.site.register(accident_group,AccidentGroupAdmin)
admin.site.register(accident_list,AccidentListAdmin)
admin.site.register(accident_cats,AccidentCatsAdmin)
admin.site.register(address_city,AddressCityAdmin)
admin.site.register(address_street,AddressStreetAdmin)
admin.site.register(address_house,AddressHouseAdmin)
admin.site.register(address_companies,AddressCompaniesAdmin)
#admin.site.register(devices_type,DevicesTypeAdmin)
admin.site.register(email_templates,EmailTemplatesAdmin)
admin.site.register(address_templates,AddressTemplatesAdmin)
admin.site.register(ports,PortsAdmin)
admin.site.register(slots,SlotsAdmin)
admin.site.register(interfaces,InterfacesAdmin)
admin.site.register(port_status,PortStatusAdmin)
admin.site.register(slot_status,SlotStatusAdmin)

