from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import ArrayField



class devices_ip(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_descr = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    device_name = models.CharField(max_length=255, db_index=True, null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)
    chassisid = models.CharField(max_length=255,db_index=True,null=True)
    lldp_neighbor_mac = ArrayField(models.CharField(max_length=100),blank=True,default=[],null=True,db_index=True)


class device_access_error(models.Model):
    ipaddress = models.GenericIPAddressField(max_length=255,db_index=True,null=True)
    device_domen = models.CharField(max_length=255, db_index=True, null=True, default=None)


