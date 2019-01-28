# coding:utf-8

import json

from django.http import HttpResponse, HttpResponseRedirect

from iss.electro.models import devicestypes, placements




def get_json(request):

    ### Timezone
    tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'


    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get

        ### Фильтр по справочнику размещения
        if r.has_key("action") and rg("action") == 'filter-placement':
            search = request.GET["search"].strip()

            if search == "" and request.session.has_key("filter-placement"):
                del request.session["filter-placement"]
            else:
                request.session["filter-placement"] = search

            response_data = {"result": "ok"}



        ### Фильтр по справочнику типов устройств
        if r.has_key("action") and rg("action") == 'filter-devicetype':
            search = request.GET["search"].strip()

            if search == "" and request.session.has_key("filter-devicetype"):
                del request.session["filter-devicetype"]
            else:
                request.session["filter-devicetype"] = search

            response_data = {"result": "ok"}





    if request.method == "POST":


        data = eval(request.body)

        # Создание нового типа
        if data.has_key("action") and data["action"] == 'new-devicetype':

            name = data["name"]
            parent = None if data["parent"] == "" else devicestypes.objects.get(pk=int(data["parent"],10))


            devicestypes.objects.create(
                name = name.strip(),
                parent = parent
            )

            response_data = {"result": "ok"}



        # Редактирование типа
        if data.has_key("action") and data["action"] == 'edit-devicetype':

            name = data["name"]
            parent = None if data["parent"] == "" else devicestypes.objects.get(pk=int(data["parent"],10))
            item_id = int(data["item_id"],10)

            dv = devicestypes.objects.get(pk=item_id)
            dv.name = name.strip()
            dv.parent = parent
            dv.save()

            response_data = {"result": "ok"}




        # Создание нового размещения
        if data.has_key("action") and data["action"] == 'new-placement':

            name = data["name"]
            parent = None if data["parent"] == "" else placements.objects.get(pk=int(data["parent"],10))


            placements.objects.create(
                name = name.strip(),
                parent = parent
            )

            response_data = {"result": "ok"}



        # Редактирование размещения
        if data.has_key("action") and data["action"] == 'edit-placement':

            name = data["name"]
            parent = None if data["parent"] == "" else placements.objects.get(pk=int(data["parent"],10))
            item_id = int(data["item_id"],10)

            pl = placements.objects.get(pk=item_id)
            pl.name = name.strip()
            pl.parent = parent
            pl.save()

            response_data = {"result": "ok"}





    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
