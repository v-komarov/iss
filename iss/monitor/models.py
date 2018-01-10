#coding:utf-8

from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



import datetime
from iss.localdicts.models import Status,Severity,accident_cats,accident_list





class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,db_index=True,default="")
    settings = JSONField(default={})


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()






### События
class events(models.Model):

    id = models.CharField(max_length=255,primary_key=True, default=uuid.uuid4, editable=False)
    evid = models.CharField(max_length=255, default="", db_index=True)
    source = models.CharField(max_length=255,db_index=True,default="")
    datetime_evt = models.DateTimeField(db_index=True,null=True,auto_now=True)
    uuid = models.CharField(max_length=255,db_index=True,null=True,default=uuid.uuid4,)
    first_seen = models.DateTimeField(db_index=True,null=True)
    update_time = models.DateTimeField(db_index=True,null=True)
    last_seen = models.DateTimeField(db_index=True,null=True)
    event_class = models.CharField(max_length=255,db_index=True,null=True)
    severity_id = models.ForeignKey(Severity,db_index=True,null=True)
    manager = models.CharField(max_length=255,db_index=True,null=True)
    device_system = models.CharField(max_length=255,db_index=True,null=True)
    device_group = models.CharField(max_length=255,db_index=True,null=True)
    device_class = models.CharField(max_length=255,db_index=True,null=True)
    device_net_address = models.CharField(max_length=255,db_index=True,null=True)
    device_location = models.CharField(max_length=255,db_index=True,null=True)
    element_identifier = models.CharField(max_length=255,db_index=True,null=True)
    element_sub_identifier = models.CharField(max_length=255,null=True)
    status_id = models.ForeignKey(Status,db_index=True,null=True)
    update_row = models.DateTimeField(auto_now=True,null=True)

    data = JSONField(default={})
    agregator = models.BooleanField(db_index=True,default=False)
    agregation = models.BooleanField(db_index=True,default=False)

    byhand = models.BooleanField(db_index=True,default=False)
    bymail = models.BooleanField(db_index=True,default=False)

    summary = models.CharField(max_length=255,db_index=True,null=True)

    accident = models.BooleanField(db_index=True,default=False)
    accident_end = models.BooleanField(db_index=True,default=False)

    mcc_mail_begin = models.BooleanField(db_index=True,default=False) ### Было создано или нет сообщение в МСС

    ### дата и время начала и завершения события
    started_date = models.DateTimeField(db_index=True,null=True)
    finished_date = models.DateTimeField(db_index=True,null=True)







### Исторические события
class events_history(models.Model):
    events_id = models.CharField(max_length=255, default=uuid.uuid4, db_index=True)

    id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    source = models.CharField(max_length=255, default="")
    datetime_evt = models.DateTimeField(null=True, auto_now=True)
    uuid = models.CharField(max_length=255, null=True, default=uuid.uuid4, )
    first_seen = models.DateTimeField(null=True)
    update_time = models.DateTimeField(null=True)
    last_seen = models.DateTimeField(null=True)
    event_class = models.CharField(max_length=255, null=True)
    severity_id = models.ForeignKey(Severity, null=True)
    manager = models.CharField(max_length=255, null=True)
    device_system = models.CharField(max_length=255, null=True)
    device_group = models.CharField(max_length=255, null=True)
    device_class = models.CharField(max_length=255, null=True)
    device_net_address = models.CharField(max_length=255, null=True)
    device_location = models.CharField(max_length=255, null=True)
    element_identifier = models.CharField(max_length=255, null=True)
    element_sub_identifier = models.CharField(max_length=255, null=True)
    status_id = models.ForeignKey(Status, null=True)
    update_row = models.DateTimeField(auto_now=True, null=True)

    data = JSONField(default={})

    summary = models.CharField(max_length=255, null=True)

    ### дата и время начала и завершения события
    started_date = models.DateTimeField(db_index=True, null=True)
    finished_date = models.DateTimeField(db_index=True, null=True)






### Аварии
class accidents(models.Model):
    create_datetime = models.DateTimeField(db_index=True,null=True,auto_now_add=True)
    update_datetime = models.DateTimeField(db_index=True,null=True,auto_now=True)
    acc_name = models.CharField(max_length=250,default="")
    acc_comment = models.TextField(default="")
    acc_cat = models.ForeignKey(accident_cats)
    acc_type = models.ForeignKey(accident_list)
    acc_event = models.OneToOneField(events,on_delete=models.SET_NULL,null=True)
    acc_address = JSONField(default={})
    acc_address_devices = JSONField(default={})
    acc_address_comment = models.CharField(max_length=100,default="")
    acc_iss_id = models.IntegerField(default=None,null=True)
    acc_start = models.DateTimeField(db_index=True,null=True)
    acc_end = models.DateTimeField(db_index=True,null=True)
    acc_reason = models.TextField(default="")
    acc_repair = models.TextField(default="")
    acc_reports_id = models.IntegerField(default=None,null=True)
    acc_stat = models.BooleanField(db_index=True, default=False) ### Включать в статистику
    acc_addr_dict = JSONField(default={}) ### Словарь данных адресов
    acc_events_list = JSONField(default={}) ### Список событий, на основании которых сформирована авария
    author = models.CharField(max_length=100,default="")


    ### Список ip адресов , связанных с этой аварией
    def get_event_ip_list(self):
        ip_list = [self.acc_event.device_net_address]
        ### Определение наличие группировки событий
        if self.acc_event.data.has_key("containergroup") and self.acc_event.agregator == True:
            ### По каждому событию в группировке поиск ip адреса
            for item in self.acc_event.data["containergroup"]:
                e = events.objects.get(pk=item)
                ip_list.append(e.device_net_address)


        return ip_list




### Оповещения
class messages(models.Model):
    datetime_message = models.DateTimeField(db_index=True,null=True,auto_now_add=True)
    accident = models.ForeignKey(accidents,db_index=True,null=True)
    data = JSONField(default={})
    send_done = models.BooleanField(db_index=True, default=False)
    mail_body = models.TextField(default=None,null=True)
    author = models.CharField(max_length=100,default="")





### Список ДРП
class drp_list(models.Model):
    datetime_drp = models.DateTimeField(db_index=True, null=True, auto_now_add=True)
    data_files = JSONField(default={}) ### Хранение файлов
    message_drp = models.TextField(default="")
    accident = models.ForeignKey(accidents)
    num_drp = models.IntegerField(default=1)
    author = models.CharField(max_length=100, default="")

