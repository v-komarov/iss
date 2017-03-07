#coding:utf-8

import pickle
import mimetypes

from iss.inventory.models import devices_scheme
from	django.http	import	HttpResponse
from	django.http import	HttpResponseRedirect
from StringIO import StringIO
from pprint import pformat



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


