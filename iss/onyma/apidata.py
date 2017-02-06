#coding:utf-8

#coding:utf-8

import json
import commands


from django.http import HttpResponse

from iss.equipment.models import devices_ip,footnodes,agregators






def get_apidata(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        if r.has_key("action") and rg("action") == 'get_balans_ls':

            ls = int(request.GET["ls"],10)
            balans = commands.getoutput("/usr/bin/php iss/onyma/soap/ls_get_balans.php %s" % ls)

            result = {'result': balans}

            response_data = result



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
