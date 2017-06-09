#coding:utf-8



import json
import commands
import urllib
from pprint import pformat


from django.http import HttpResponse

import iss.dbconn


username = iss.dbconn.ONYMA_USERNAME
password = iss.dbconn.ONYMA_PASSWORD







### Функции внутреннего использования
def get_dogcodebylogin(loginlist):
    """
    :param loginlist:
    :return: json
    """

    result = commands.getoutput("/usr/bin/php iss/onyma/soap/get_dogcode_by_login.php %s %s %s" % (username, password, loginlist))

    return result





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



        ### Создание договора с предопределенными значениями
        # дата подключения pdogdate=now()
        # идентификатор группы pgid

        if r.has_key("action") and rg("action") == 'dog_create':
            pgid = int(request.GET["pgid"],10)
            dogcode = request.GET["dogcode"]
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            result = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/dog_create.php %s %s %s %s" % (username2, password2, pgid, dogcode))

            response_data = result



        ### Установка договору даты начала

        if r.has_key("action") and rg("action") == 'dog_set_date':
            dogid = int(request.GET["dogid"], 10)
            dogdate = request.GET["dogdate"]
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            result = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/dog_set_dogdate.php %s %s %s %s" % (username2, password2, dogid, dogdate))

            response_data = result



        ### Установка ФИО договора

        if r.has_key("action") and rg("action") == 'dog_set_fio':
            dogid = int(request.GET["dogid"], 10)
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            lastname = urllib.unquote(request.GET["lastname"])
            firstname = urllib.unquote(request.GET["firstname"])
            secondname = urllib.unquote(request.GET["secondname"])

            cmd = "/usr/bin/php iss/onyma/soap/dog_set_fio.php %s %s %s %s %s %s" % (username2, password2, dogid, lastname, firstname, secondname)

            result = commands.getoutput(cmd.encode("utf-8"))

            response_data = result




        ### Установка номера телефона договора

        if r.has_key("action") and rg("action") == 'dog_set_phone':
            dogid = int(request.GET["dogid"], 10)
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            phone = urllib.unquote(request.GET["phone"])

            cmd = "/usr/bin/php iss/onyma/soap/dog_set_phone.php %s %s %s %s" % (
            username2, password2, dogid, phone)

            result = commands.getoutput(cmd.encode("utf-8"))

            response_data = result



        ### Установка адреса договора 2

        if r.has_key("action") and rg("action") == 'dog_set_address2':
            dogid = int(request.GET["dogid"], 10)
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            city = urllib.unquote(request.GET["city"]).replace(" ","#")
            street = urllib.unquote(request.GET["street"]).replace(" ","#")
            house = urllib.unquote(request.GET["house"]).replace(" ","#")
            room = urllib.unquote(request.GET["room"]).replace(" ","#")

            cmd = "/usr/bin/php iss/onyma/soap/dog_set_address.php %s %s %s %s %s %s %s" % (
                username2, password2, dogid, city, street, house, room)

            result = commands.getoutput(cmd.encode("utf-8"))

            response_data = result




        ### Установка адреса договора (пробелы заменены подчеркиванием)

        if r.has_key("action") and rg("action") == 'dog_set_address':
            dogid = int(request.GET["dogid"], 10)
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            city = urllib.unquote(request.GET["city"]).replace("_","#")
            street = urllib.unquote(request.GET["street"]).replace("_","#")
            house = urllib.unquote(request.GET["house"]).replace("_","#")
            room = urllib.unquote(request.GET["room"]).replace("_","#")

            cmd = "/usr/bin/php iss/onyma/soap/dog_set_address.php %s %s %s %s %s %s %s" % (
                username2, password2, dogid, city, street, house, room)

            result = commands.getoutput(cmd.encode("utf-8"))

            response_data = result





        ### Установка номера договора

        if r.has_key("action") and rg("action") == 'dog_set_dognum':
            dogid = int(request.GET["dogid"], 10)
            username2 = request.GET["username"]
            password2 = request.GET["password"]
            dognum = urllib.unquote(request.GET["dognum"])

            cmd = "/usr/bin/php iss/onyma/soap/dog_set_dognum.php %s %s %s %s" % (
                username2, password2, dogid, dognum)

            result = commands.getoutput(cmd.encode("utf-8"))

            response_data = result




        ## Запрос данных по номеру договора - учетное имя, тарифный план, название ресурса
        if r.has_key("action") and rg("action") == 'get_user_services_dognum':
            dognum = request.GET["dognum"]
            data = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/get_user_services.php %s %s %s" % (username, password, dognum))

            response_data = data




        ## Запрос данных по номеру договора - id договора
        if r.has_key("action") and rg("action") == 'get_dogid':
            dognum = request.GET["dognum"]
            data = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/get_dogid.php %s %s %s" % (username, password, dognum))

            response_data = data




        ## Запрос  id тарифного плана по названию
        if r.has_key("action") and rg("action") == 'get_tmid':
            tmname = urllib.unquote(request.GET["tmname"]).replace(" ","#")


            cmd = "/usr/bin/php iss/onyma/soap/get_tmid.php %s %s %s" % (username, password, tmname)
            data = commands.getoutput(cmd.encode("utf-8"))

            response_data = data





        ## Запрос данных по номеру договора - id договора
        if r.has_key("action") and rg("action") == 'test':

            response_data = "1"





        ## Запрос данных по номеру договора - учетное имя, тарифный план, название ресурса
        if r.has_key("action") and rg("action") == 'get_user_services_dogid':
            dogid = request.GET["dogid"]
            data = commands.getoutput(
                "/usr/bin/php iss/onyma/soap/get_user_services2.php %s %s %s" % (username, password, dogid))

            response_data = data




        # вывод списка доменов
        if r.has_key("action") and rg("action") == 'get_domain_list':
            domains = commands.getoutput("/usr/bin/php iss/onyma/soap/get_domain_list.php %s %s" % (username, password))

            response_data = domains




    response = HttpResponse(response_data, content_type="text/plain; charset=utf-8")
    response['Access-Control-Allow-Origin'] = "*"
    return response







