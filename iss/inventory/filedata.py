#coding:utf-8

import pickle
import mimetypes

from iss.inventory.models import devices_scheme
from	django.http	import	HttpResponse
from	django.http import	HttpResponseRedirect
from StringIO import StringIO
from pprint import pformat
from iss.localdicts.models import address_house,device_status
from iss.inventory.models import devices



dev_use = device_status.objects.get(name="Используется")



### json схемы
def get_device_scheme(request):

    if request.method == "GET":

        sch_id = int(request.GET["sch"],10)

        sch = devices_scheme.objects.get(pk=sch_id)

        response = HttpResponse(content_type="text/plain")
        response['Content-Disposition'] = 'attachment; filename="%s.txt"' % sch.name.encode("utf-8")
        result = pformat(sch.scheme_device)
        response.write(result)
        return response



### Аудит портов выгрузка в формате csv
def get_audit_ports(request):

    if request.method == "GET":

        response_data = u"ADDRESS;MODEL;STATUS;SERIAL;NETELEM;MANAGE;PORTS;PORTS_USE;PORTS_RES;PORTS_TECH;COMBO;COMBO_USE;COMBO_RES;COMBO_TECH;\n"


        if request.session.has_key("address_id") and request.session["address_id"] != 'undefined':

            addr = address_house.objects.get(pk=int(request.session["address_id"],10))

            ### Когда определен только город
            if addr.city and addr.street == None and addr.house == None:
                data = devices.objects.filter(address__city = addr.city).order_by('address__street__name')

            ### Когда определен город и улица
            elif addr.city and addr.street and addr.house == None:
                data = devices.objects.filter(address__city = addr.city,address__street = addr.street).order_by('address__house')


            ### Когда определены город, улица, дом
            elif addr.city and addr.street and addr.house:
                data = devices.objects.filter(address__city=addr.city, address__street=addr.street, address__house=addr.house).all()

            else:
                data = []


        else:
            data = []


        for d in data:

            netelems = []
            for ne in d.get_netelems():
                netelems.append(ne['name'])


            response_data = response_data + u"{addr};{model};{status};{serial};{netelem};{manage};{ports};{ports_use};{ports_res};{ports_tech};{combo};{combo_use};{combo_res};{combo_tech};\n".format(
                addr=d.getaddress(),model=d.device_scheme.name if d.device_scheme else "",status=d.status,serial=d.serial,netelem=" ".join(netelems),
                manage=" ".join(d.get_manage_ip()),ports=d.get_ports_count(),ports_use=d.get_use_ports(),ports_res=d.get_reserv_ports(),
                ports_tech=d.get_tech_ports(),combo=d.get_combo_count(),combo_use=d.get_use_combo(),combo_res=d.get_reserv_combo(),
                combo_tech=d.get_tech_combo()
            )



        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="auditports.csv"'
        response.write(response_data)
        return response

