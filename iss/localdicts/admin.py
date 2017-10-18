#!coding:utf-8

from django.contrib import admin
from iss.localdicts.models import TzList,Status,Severity,accident_group,accident_list,accident_cats,address_city,address_street,address_house,address_companies,email_templates,address_templates,slots,ports,interfaces,port_status,slot_status,device_status,logical_interfaces_prop_list, regions, proj_temp, blocks, proj_types, business, passing, rates

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
    ordering = ['name',]


class AddressStreetAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)
    search_fields = ['name']
    ordering = ['name',]


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



class DeviceStatusAdmin(admin.ModelAdmin):

    fields = ('name',)
    list_display = ('name',)



class LogicalInterfacePropAdmin(admin.ModelAdmin):

    fields = ('name','comment')
    list_display = ('name','comment')



class RegionsAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)



class ProjTempAdmin(admin.ModelAdmin):
    fields = ('name', 'template_project',)
    list_display = ('name',)


class BlocksAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)



class ProjTypesAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)



class BusinessAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)



class PassingAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)




class RatesAdmin(admin.ModelAdmin):
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
admin.site.register(device_status,DeviceStatusAdmin)
admin.site.register(logical_interfaces_prop_list,LogicalInterfacePropAdmin)
admin.site.register(regions, RegionsAdmin)
admin.site.register(proj_temp, ProjTempAdmin)
admin.site.register(blocks, BlocksAdmin)
admin.site.register(proj_types, ProjTypesAdmin)
admin.site.register(business, BusinessAdmin)
admin.site.register(passing, PassingAdmin)
admin.site.register(rates, RatesAdmin)


