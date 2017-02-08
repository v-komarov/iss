#coding:utf-8



import json
import commands


from django.http import HttpResponse

import iss.dbconn


username = iss.dbconn.ONYMA_USERNAME
password = iss.dbconn.ONYMA_PASSWORD





def get_apidata(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        if r.has_key("action") and rg("action") == 'get_balans_ls':

            ls = int(request.GET["ls"],10)
            balans = commands.getoutput("/usr/bin/php iss/onyma/soap/ls_get_balans.php %s %s %s" % (username,password,ls))

            result = {'result': balans}

            response_data = result



    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response





def get_apidata2(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get


        if r.has_key("action") and rg("action") == 'get_balans_dognum':

            dognum = int(request.GET["dognum"],10)
            balans = commands.getoutput("/usr/bin/php iss/onyma/soap/dognum_get_balans.php %s %s %s" % (username,password,dognum))

            response_data = "balans:%s;" % balans



    response = HttpResponse(response_data, content_type="text/plain")
    response['Access-Control-Allow-Origin'] = "*"
    return response
