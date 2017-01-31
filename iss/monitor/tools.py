#coding:utf-8

import pickle
import mimetypes

from iss.monitor.models import events,drp_list
from django.http	import	HttpResponse
from django.http import	HttpResponseRedirect


from iss.monitor.models import events,accidents


### Возвращает список ip адресов по id группы
def groupevents_ip(event_id):

    ev = events.objects.get(pk=event_id)

    ipaddress = []
    for item in ev.device_net_address.split(","):
        ipaddress.append(item.strip())

    if ev.agregator == True:
        if ev.data.has_key("containergroup"):
            for rid in ev.data["containergroup"]:
                for i in events.objects.get(pk=rid).device_net_address.split(","):
                    ipaddress.append(i.strip())

    return ipaddress



