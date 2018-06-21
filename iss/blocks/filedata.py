#coding:utf-8


from	django.http	import	HttpResponse, HttpResponseRedirect


import xlwt
import tempfile
import os
import StringIO
import cStringIO
import datetime
import mimetypes
import json
from decimal import Decimal
import pickle
import urllib


from operator import itemgetter

import pandas as pd
from pandas import ExcelFile

from matplotlib import rc
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY, MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


from snakebite.client import Client

from iss.blocks.models import block_managers, files, comments_logs



mimetypes.init()
mimetypes.add_type('application/xslt+xml','.xslx')








### Загрузка файлов по компании
def uploadfile(request):

    company_id = request.POST["company_id"]

    company = block_managers.objects.get(pk=int(company_id, 10))


    filename = request.FILES['fileuploadhdfs'].name
    filedata = request.FILES['fileuploadhdfs'].read()


    rec = files.objects.create(
        company = company,
        filename = filename.strip(),
        user = request.user
    )

    comments_logs.objects.create(
        manager=company,
        user=request.user,
        comment=u"Загружен файл {filename}".format(filename=rec.filename),
        log=True
    )

    ### Запись во временный файл
    tf = tempfile.NamedTemporaryFile(delete=False)
    f = open(tf.name, 'w')
    f.write(filedata)
    f.close()


    run = 'curl -i -X PUT -T %s -L "http://10.6.0.135:50070/webhdfs/v1/blocks/%s?user.name=root&op=CREATE&overwrite=true&replication=2"' % (tf.name, rec.id)

    os.system(run)


    ### Удаление временного файла
    os.remove(tf.name)


    return HttpResponse("""
    <html><head><script type="text/javascript">
        window.top.ClearUpload();
        window.top.GetListHdfsFiles();
        window.top.GetListLogs();
    </script></head></html>
    """)








### Получение загруженного файла по компании
def gethdfsfile(request):

    if request.method == "GET":
        file_id = request.GET["file_id"]
        file_name = request.GET["file_name"]

        file_name = urllib.unquote(file_name).encode("utf-8")

        ### временный файл
        tfile = "/tmp/{file_id}".format(file_id=file_id)


        client = Client('10.6.0.135', 9000)
        for x in client.copyToLocal(['/blocks/%s' % file_id], tfile):
            print x

        f = open(tfile, 'r')
        data = f.read()
        f.close()

        ### Удаление временного файла
        os.remove(tfile)

        content_type =  mimetypes.types_map[".%s" % file_name.split('.')[-1]]

        response = HttpResponse(data, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        return response



