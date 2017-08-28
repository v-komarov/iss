#coding:utf-8


from	django.http	import	HttpResponse, HttpResponseRedirect


import xlwt
import tempfile
import os
from cStringIO import StringIO

from django.db.models import Q

from iss.exams.models import tests_results
from iss.exams.printform import QuestionsList, ProtocolPDF, ProtocolListPDF






### Вывод печатной формы списка вопросов тестирования
def QuestionsExam(request, result):

    res = tests_results.objects.get(pk=result)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
    buff = StringIO()
    result = QuestionsList(buff, res)
    response.write(result.getvalue())
    buff.close()

    return response






### Вывод печатной формы протокола
def ProtocolExam(request, result):

    res = tests_results.objects.get(pk=result)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="protocol.pdf"'
    buff = StringIO()
    result = ProtocolPDF(buff, res)
    response.write(result.getvalue())
    buff.close()

    return response







### Вывод результатов
def report(request):


    style_bold = xlwt.easyxf('font: bold 1;')

    book = xlwt.Workbook()

    sh = book.add_sheet(u"Результаты тестирования")
    sh.col(1).width = 15000
    sh.col(2).width = 15000
    sh.col(3).width = 15000
    sh.col(4).width = 15000

    ### Заголовок
    sh.write(0, 0, u"№п/п", style=style_bold)
    sh.write(0, 1, u"Название теста", style=style_bold)
    sh.write(0, 2, u"ФИО", style=style_bold)
    sh.write(0, 3, u"Должность", style=style_bold)
    sh.write(0, 4, u"Место работы", style=style_bold)
    sh.write(0, 5, u"Дата", style=style_bold)

    if request.session.has_key('reportlist'):

        filter =  [ "Q(id=%s)" % item for item in request.session['reportlist']]

        run = "tests_results.objects.filter({filter}).order_by('worker')".format(filter=" | ".join(filter))

        n = 1  ## Строка в листе
        for row in eval(run):
            sh.write(n, 0, n)
            sh.write(n, 1, row.test.name)
            sh.write(n, 2, row.worker)
            sh.write(n, 3, row.job)
            sh.write(n, 4, row.department)
            sh.write(n, 5, row.end.strftime('%d.%m.%Y'))

            n += 1

    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="report.xls"'
    book.save(response)
    return response





### Вывод печатной формы протокола для списка
def report2(request):


    if request.session.has_key('reportlist'):

        filter =  [ "Q(id=%s)" % item for item in request.session['reportlist']]

        run = "tests_results.objects.filter({filter}).order_by('worker')".format(filter=" | ".join(filter))

        res = eval(run)

    else:
        res = []


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="protocol.pdf"'
    buff = StringIO()
    result = ProtocolListPDF(buff, res)
    response.write(result.getvalue())
    buff.close()

    return response

