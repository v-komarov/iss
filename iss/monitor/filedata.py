#coding:utf-8

import pickle

from iss.monitor.models import events
from	django.http	import	HttpResponse
from	django.http import	HttpResponseRedirect
from StringIO import StringIO




def get_filedata(request):

    if request.method == "GET":
        event_id = request.GET["event_id"]
        filename = request.GET["filename"]

        e = events.objects.get(pk=event_id)
        mails = e.data["mails"]
        for m in mails:
            if m.has_key("attachment"):

                for a in m["attachment"]:

                    if a["file_name"] == filename:
                        response = HttpResponse(content_type=a["mime_type"])
                        response['Content-Disposition'] = 'attachment; filename="%s"' % a["file_name"]
                        result = pickle.loads(a["file_data"])
                        response.write(result.getvalue())
                        return response


        return HttpResponse("None")