#coding:utf-8

import json
import pickle
import datetime

import base64
from io import BytesIO

from decimal import Decimal

from pytz import timezone
from pprint import pformat

from snakebite.client import Client


from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from django.db.models import Count, Q, Avg, Sum
from django.contrib.auth.models import User

from iss.blocks.models import block_managers, buildings, comments_logs, contracts, pay_period, files
from iss.localdicts.models import address_house













def get_json(request):

    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get




        ### Фильтр по городу улице дому
        if r.has_key("action") and rg("action") == 'filter-addresslist':

            city = request.GET["city"].strip()
            street = request.GET["street"].strip()
            house = request.GET["house"].strip()


            if city != "" or street != "" or house != "":
                request.session["filter_addresslist"] = pickle.dumps({ 'city': city, 'street': street, 'house': house })

            if city == "" and street == "" and house == "":
                if request.session.has_key("filter_addresslist"):
                    del request.session["filter_addresslist"]


            response_data = {"result": "ok"}





        ### Очистка фильтр по городу улице дому
        if r.has_key("action") and rg("action") == 'filter-addresslist-clear':


            if request.session.has_key("filter_addresslist"):
                del request.session["filter_addresslist"]

            response_data = {"result": "ok"}



        ### Фильтр по городу улице дому по компании
        if r.has_key("action") and rg("action") == 'filter-company':

            city = request.GET["city"].strip()
            street = request.GET["street"].strip()
            house = request.GET["house"].strip()
            company = request.GET["company"].strip()


            request.session["filter_company"] = pickle.dumps({ 'city': city, 'street': street, 'house': house, 'company': company })

            if city == "" and street == "" and house == "" and company == "":
                if request.session.has_key("filter_company"):
                    del request.session["filter_company"]


            response_data = {"result": "ok"}





        ### Очистка фильтр по городу улице дому по компании
        if r.has_key("action") and rg("action") == 'filter-company-clear':


            if request.session.has_key("filter_company"):
                del request.session["filter_company"]

            response_data = {"result": "ok"}







        ### Фильтр по договорам
        if r.has_key("action") and rg("action") == 'filter-contract':

            inn = request.GET["inn"].strip()
            manager = request.GET["manager"].strip()
            company = request.GET["company"].strip()


            request.session["filter_contract"] = pickle.dumps({ 'manager': manager, 'inn': inn, 'company': company })

            if inn == "" and company == "" and manager == "":
                if request.session.has_key("filter_contract"):
                    del request.session["filter_contract"]


            response_data = {"result": "ok"}





        ### Очистка фильтр по договорам
        if r.has_key("action") and rg("action") == 'filter-contract-clear':


            if request.session.has_key("filter_contract"):
                del request.session["filter_contract"]

            response_data = {"result": "ok"}





        ### Cписок логов карточки компании
        if r.has_key("action") and rg("action") == 'get-company-list-logs':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            log_list = []
            for row in comments_logs.objects.filter(manager=company,log=True).order_by("-datetime_create"):
                log_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": log_list }




        ### Карточка компании: список коментариев
        if r.has_key("action") and rg("action") == 'get-company-list-comments':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            comment_list = []
            for row in comments_logs.objects.filter(manager=company,log=False).order_by("-datetime_create"):
                comment_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": comment_list }






        ### Карточка компании: список договоров
        if r.has_key("action") and rg("action") == 'get-company-list-contracts':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            contract_list = []
            for row in contracts.objects.filter(company=company).order_by("-datetime_create"):
                contract_list.append({
                    "contract_id": row.id,
                    "num": row.num,
                    "date_begin": row.date_begin.strftime("%d.%m.%Y"),
                    "date_end": row.date_end.strftime("%d.%m.%Y"),
                    "goon": u"Да" if row.goon else u"Нет",
                    "money": "%.2f" % row.money,
                    "period": row.period.name,
                    "manager": row.manager.get_full_name(),
                    "author": row.user.get_full_name(),
                    "create": row.datetime_create.strftime("%d.%m.%Y"),
                    "comment": row.comment
                })


            response_data = {"result": "ok", "data": contract_list }





        ### Карточка компании: данные по одному договору
        if r.has_key("action") and rg("action") == 'get-company-contract-one':
            contract_id = request.GET["contract-id"]
            contract = contracts.objects.get(pk=int(contract_id,10))

            rec = {
                    "contract_id": contract.id,
                    "num": contract.num,
                    "date_begin": contract.date_begin.strftime("%d.%m.%Y"),
                    "date_end": contract.date_end.strftime("%d.%m.%Y"),
                    "goon": "yes" if contract.goon else "no",
                    "money": "%.2f" % contract.money,
                    "period": contract.period.id,
                    "manager": contract.manager.id,
                    "comment": contract.comment
            }


            response_data = {"result": "ok", "rec": rec }





        ### Удаление договора
        if r.has_key("action") and rg("action") == 'contract-delete':
            contract_id = request.GET["contract_id"]
            contract = contracts.objects.get(pk=int(contract_id,10))
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            comments_logs.objects.create(
                manager = company,
                user = request.user,
                comment = u"Удален договор {num} ({author} {create})".format(num=contract.num, author=contract.user.get_full_name(), create=contract.datetime_create.strftime("%d.%m.%Y")) ,
                log=True
            )
            contract.delete()



            response_data = {"result": "ok"}





        ### Карточка компании: список загруженных файлов
        if r.has_key("action") and rg("action") == 'get-company-list-hdfs-files':
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))
            file_list = []
            for row in files.objects.filter(company=company).order_by("-datetime_load"):
                file_list.append({
                    "file_id": row.id,
                    "filename": row.filename,
                    "author": row.user.get_full_name(),
                    "create": row.datetime_load.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": file_list }






        ### Карточка компании: удаление загруженного файла
        if r.has_key("action") and rg("action") == 'company-file-delete':
            file_id = request.GET["file_id"]
            company_id = request.GET["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))


            fob = files.objects.get(pk=file_id)


            comments_logs.objects.create(
                manager=company,
                user=request.user,
                comment=u"Удален файл {filename}".format(filename=fob.filename),
                log=True
            )

            fob.delete()

            client = Client('10.6.0.135', 9000)
            for x in client.delete(['/blocks/%s' % file_id,], recurse=True):
                print x


            response_data = { "result": "ok" }






        #### Поиск по компании
        if r.has_key("term") and rg("term") != "":
            term = request.GET["term"]
            obj = []

            data = block_managers.objects.filter(Q(name__icontains=term) | Q(inn__icontains=term))

            for row in data:

                obj.append(
                    {
                        "label": u"{name} (ИНН {inn})".format(name=row.name, inn=row.inn),
                        "value": row.id
                    }
                )

            response_data = obj






        ### Cписок логов карточки дома
        if r.has_key("action") and rg("action") == 'get-house-list-logs':
            house_id = request.GET["house"]
            house = buildings.objects.get(pk=int(house_id, 10))
            log_list = []
            for row in comments_logs.objects.filter(house=house,log=True).order_by("-datetime_create"):
                log_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": log_list }





        ### Карточка дома: список коментариев
        if r.has_key("action") and rg("action") == 'get-house-list-comments':
            house_id = request.GET["house"]
            house = buildings.objects.get(pk=int(house_id, 10))
            comment_list = []
            for row in comments_logs.objects.filter(house=house,log=False).order_by("-datetime_create"):
                comment_list.append({
                    "comment": row.comment,
                    "user": row.user.get_full_name(),
                    "date": row.datetime_create.strftime("%d.%m.%Y")
                })


            response_data = {"result": "ok", "data": comment_list }






    if request.method == "POST":


        data = eval(request.body)



        ### Сохранение карточки компании
        if data.has_key("action") and data["action"] == 'company-common-save':


            company_id = data["company_id"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            address_id = data["address"]
            address_law_id = data["address_law"]

            address = address_house.objects.get(pk=int(address_id,10))
            address_law = address_house.objects.get(pk=int(address_law_id,10))

            name = data["name"].strip()
            inn = data["inn"].strip()
            phone = data["phone"].strip()
            email = data["email"].strip()
            contact = data["contact"].strip()



            company.name = name
            company.inn = inn
            company.phone = phone
            company.email = email
            company.contact = contact
            company.address = address
            company.address_law = address_law

            company.save()

            comments_logs.objects.create(
                manager = company,
                user = request.user,
                comment = u"Сохранены данные карточки компании",
                log=True
            )



            response_data = {"result": "ok"}





        ### Добавление компании
        if data.has_key("action") and data["action"] == 'company-common-create':

            id_www = int(data["id_www"].strip(),10)

            address_id = data["address"]
            address_law_id = data["address_law"]

            address = address_house.objects.get(pk=int(address_id,10))
            address_law = address_house.objects.get(pk=int(address_law_id,10))

            name = data["name"].strip()
            inn = data["inn"].strip()
            phone = data["phone"].strip()
            email = data["email"].strip()
            contact = data["contact"].strip()

            ### Проверка есть ли уже такой id_www
            if not block_managers.objects.filter(www_id=id_www).exists() and not block_managers.objects.filter(inn=inn).exists():

                new = block_managers.objects.create(
                    www_id=id_www,
                    name=name,
                    inn=inn,
                    phone=phone,
                    email=email,
                    contact=contact,
                    address=address,
                    address_law=address_law
                )


                comments_logs.objects.create(
                    manager = new,
                    user = request.user,
                    comment = u"Создана карточка компании",
                    log=True
                )

                response_data = {"result": "ok", "id": new.id}

            else:

                response_data = {"result": "error"}




        ### Добавление коментария компании
        if data.has_key("action") and data["action"] == 'company-comment-add':

            company_id = data["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            comment = data["comment"].strip()

            if comment != "":


                comments_logs.objects.create(
                    manager = company,
                    user = request.user,
                    comment = comment
                )




            response_data = {"result": "ok"}




        ### Добавление договора компании
        if data.has_key("action") and data["action"] == 'contract-create':

            company_id = data["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            contracts.objects.create(
                company = company,
                num = data["num"].strip(),
                date_begin = datetime.datetime.strptime(data["date_begin"],"%d.%m.%Y"),
                date_end=datetime.datetime.strptime(data["date_end"], "%d.%m.%Y"),
                goon = True if data["goon"] == "yes" else False,
                money = Decimal(data["money"]),
                period = pay_period.objects.get(pk=int(data["period"],10)),
                manager = User.objects.get(pk=int(data["manager"],10)),
                user = request.user,
                comment = data["comment"].strip()
            )



            response_data = {"result": "ok"}





        ### Сохранение договора компании
        if data.has_key("action") and data["action"] == 'contract-edit':

            company_id = data["company"]
            company = block_managers.objects.get(pk=int(company_id, 10))

            contract_id = data["contract_id"]
            contract = contracts.objects.get(pk=int(contract_id, 10))

            contract.num = data["num"].strip()
            contract.date_begin = datetime.datetime.strptime(data["date_begin"],"%d.%m.%Y")
            contract.date_end=datetime.datetime.strptime(data["date_end"], "%d.%m.%Y")
            contract.goon = True if data["goon"] == "yes" else False
            contract.money = Decimal(data["money"])
            contract.period = pay_period.objects.get(pk=int(data["period"],10))
            contract.manager = User.objects.get(pk=int(data["manager"],10))
            contract.comment = data["comment"].strip()
            contract.save()

            comments_logs.objects.create(
                manager = company,
                user = request.user,
                comment = u"Сохранены данные договора {num} ({author} {create})".format(num=contract.num, author=contract.user.get_full_name(), create=contract.datetime_create.strftime("%d.%m.%Y")) ,
                log=True
            )


            response_data = {"result": "ok"}




        ### Сохранение карточки дома
        if data.has_key("action") and data["action"] == 'house-common-save':


            house_id = data["house"]
            house = buildings.objects.get(pk=int(house_id, 10))

            address_id = data["address"]
            address = address_house.objects.get(pk=int(address_id,10))

            company_id = data["manager"]
            company = block_managers.objects.get(pk=int(company_id,10))

            numstoreys = data["numstoreys"].strip()
            numentrances = data["numentrances"].strip()
            numfloars = data["numfloars"].strip()
            access = data["access"].strip()


            house.numstoreys = numstoreys
            house.numentrances = numentrances
            house.numfloars = numfloars
            house.access = access
            house.address = address
            house.block_manager = company

            house.save()

            comments_logs.objects.create(
                house = house,
                user = request.user,
                comment = u"Сохранены данные карточки дома",
                log=True
            )



            response_data = {"result": "ok"}





        ### Создание карточки дома
        if data.has_key("action") and data["action"] == 'house-common-create':

            id_www = int(data["id_www"].strip(),10)

            address_id = data["address"]
            address = address_house.objects.get(pk=int(address_id,10))

            company_id = data["manager"]
            company = block_managers.objects.get(pk=int(company_id,10))

            numstoreys = int(data["numstoreys"].strip(),10)
            numentrances = int(data["numentrances"].strip(),10)
            numfloars = int(data["numfloars"].strip(),10)
            access = data["access"].strip()


            ### Проверка уникальности www_id
            if not block_managers.objects.filter(www_id=id_www).exists():

                new = buildings.objects.create(
                    www_id=id_www,
                    numstoreys=numstoreys,
                    numentrances=numentrances,
                    numfloars=numfloars,
                    access=access,
                    address=address,
                    block_manager=company
                )


                comments_logs.objects.create(
                    house = new,
                    user = request.user,
                    comment = u"Создана карточка дома",
                    log=True
                )



                response_data = {"result": "ok", "id": new.id}

            else:
                response_data = {"result": "error"}





        ### Добавление коментария дома
        if data.has_key("action") and data["action"] == 'house-comment-add':

            house_id = data["house"]
            house = buildings.objects.get(pk=int(house_id, 10))

            comment = data["comment"].strip()

            if comment != "":


                comments_logs.objects.create(
                    house = house,
                    user = request.user,
                    comment = comment
                )




            response_data = {"result": "ok"}






    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response


