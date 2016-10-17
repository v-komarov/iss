from __future__ import unicode_literals

from django.db import models


class devices_lldp(models.Model):

    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_model = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)

    port_local_label = models.CharField(max_length=255,db_index=True,null=True)
    port_local_mac = models.CharField(max_length=255,db_index=True,null=True)
    port_local_index = models.IntegerField(db_index=True,default=False)
    port_local_up = models.BooleanField(db_index=True,default=True)

    port_neighbor_label = models.CharField(max_length=255,db_index=True,null=True)
    port_neighbor_mac = models.CharField(max_length=255, db_index=True, null=True)
    port_neighbor_index = models.IntegerField(db_index=True, default=False)
