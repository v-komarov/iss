# coding:utf-8

import json

from django.http import HttpResponse, HttpResponseRedirect

from iss.electro.models import devicestypes



def get_json(request):

    ### Timezone
    tz = request.session['tz'] if request.session.has_key('tz') else 'UTC'


    response_data = {}

    if request.method == "GET":

        r = request.GET
        rg = request.GET.get



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



        # Создание нового типа
        if data.has_key("action") and data["action"] == 'edit-devicetype':

            name = data["name"]
            parent = None if data["parent"] == "" else devicestypes.objects.get(pk=int(data["parent"],10))
            item_id = int(data["item_id"],10)

            dv = devicestypes.objects.get(pk=item_id)
            dv.name = name.strip()
            dv.parent = parent
            dv.save()

            response_data = {"result": "ok"}




    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    response['Access-Control-Allow-Origin'] = "*"
    return response
