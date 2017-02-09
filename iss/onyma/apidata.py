#coding:utf-8



import json
import commands
import os
import datetime
import ssl
import SOAPpy
from SOAPpy import WSDL, structType, headerType, arrayType



from django.http import HttpResponse

import iss.dbconn


username = iss.dbconn.ONYMA_USERNAME
password = iss.dbconn.ONYMA_PASSWORD




### Вывод в формате json
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






### Вывод в текстовом формате
def get_apidata2(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get

        ## Запрос остатка на лицевом счете по номеру договора
        if r.has_key("action") and rg("action") == 'get_balans_dognum':

            dognum = int(request.GET["dognum"],10)
            balans = commands.getoutput("/usr/bin/php iss/onyma/soap/dognum_get_balans.php %s %s %s" % (username,password,dognum))

            response_data = "balans:%s;" % balans


        ### Запрос списка групп (городов)
        if r.has_key("action") and rg("action") == 'get_groups':
            groups = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/get_groups.php %s %s" % (username,password))

            result = ""
            for item in json.loads(groups)["row"]:
                result = result + "name:{name},id:{id};".format(name=item["g_name"].encode("utf-8"),id=item["gid"])
            response_data = result



    response = HttpResponse(response_data, content_type="text/plain")
    response['Access-Control-Allow-Origin'] = "*"
    return response







