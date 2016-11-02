from __future__ import unicode_literals

from django.db import models




class devices_ip(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_descr = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    device_name = models.CharField(max_length=255, db_index=True, null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)

class devices_lldp(models.Model):
    device_ip = models.ForeignKey('devices_ip',on_delete=models.CASCADE,default=None,db_index=True,null=True)
    port_local_mac = models.CharField(max_length=255,db_index=True,null=True)
    port_local_index = models.IntegerField(db_index=True,default=False)
    port_neighbor_mac = models.CharField(max_length=255, db_index=True, null=True, default=None)
    port_status = models.BooleanField(db_index=True,default = False)

