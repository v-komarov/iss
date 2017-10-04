#coding:utf-8


from	reportlab.pdfgen	import	canvas
from	reportlab.lib.units	import	mm
from	reportlab.pdfbase	import	pdfmetrics
from	reportlab.pdfbase	import	ttfonts
from	reportlab.lib		import	colors
from	reportlab.lib.pagesizes	import	letter, A4, landscape

from	reportlab.platypus.tables	import	Table, TableStyle
from	reportlab.platypus.doctemplate	import	SimpleDocTemplate
from	reportlab.platypus.paragraph	import	Paragraph
from	reportlab.lib.styles		import	ParagraphStyle,getSampleStyleSheet
from	reportlab.platypus		import	Frame,Spacer

from	reportlab.platypus		import	Image




### --- Печатная протокола ---
def	ProtocolPDF(buff, res):



    Font1 = ttfonts.TTFont('PT', 'fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB', 'fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI', 'fonts/PTS56F.ttf')


    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)


    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3*mm, spaceBefore=20*mm, alignment=1))
    style.add(ParagraphStyle(name='MyStyle1', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3*mm, spaceBefore=0*mm, alignment=1))

    style.add(ParagraphStyle(name='MyStyle0', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=5*mm, spaceBefore=5*mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle2', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=1*mm, spaceBefore=1*mm, alignment=0))
    
    doc = SimpleDocTemplate(buff, topMargin=10*mm, bottomMargin=10*mm, leftMargin=20*mm, rightMargin=10*mm)


    elements = []

    elements.append(Paragraph(u'Протокол',style["MyStyle"]))
    elements.append(Paragraph(u'проверки знаний правил по охране труда при работе на высоте',style["MyStyle1"]))
    elements.append(Paragraph(u'№ _____________________',style["MyStyle1"]))

    elements.append(Paragraph(u'Дата проверки: %s' % res.end.strftime("%d.%m.%Y"), style["MyStyle2"]))
    elements.append(Paragraph(u'Причина проверки: ____________________________________________________________________________________', style["MyStyle2"]))

    elements.append(Paragraph(u'Комиссия: <font face="PTB">ЗАО "СибТрансТелеКом"</font> в составе:', style["MyStyle2"]))
    elements.append(Paragraph(u'председатель комиссии: <font face="PTB">Бусыгин Павел Генрихович</font> - главный энергетик ЭО', style["MyStyle2"]))
    elements.append(Paragraph(u'члены комиссии: <font face="PTB">Бочериков Андрей Павлович</font> - начальник СЭМС; <font face="PTB">Тучин Юрий Михайлович</font> - инженер ЭПУ СЭМС', style["MyStyle2"]))
    elements.append(Paragraph(u'провела проверку знаний правил по охране труда при работе на высоте, и других нормативно-технических документов в соответствии с занимаемой должностью.', style["MyStyle2"]))

    elements.append(Paragraph(u'Проверяемый',style["MyStyle"]))
    elements.append(Paragraph(u'Фамилия, имя, отчество: <font face="PTB">%s</font>' % res.worker, style["MyStyle2"]))
    elements.append(Paragraph(u'Место работы: <font face="PTB">%s</font>' % res.department, style["MyStyle2"]))
    elements.append(Paragraph(u'Должность: <font face="PTB">%s</font>' % res.job, style["MyStyle2"]))
    elements.append(Paragraph(u'Дата предыдущей проверки: ____________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'оценка, группа по безопасности на высоте: ____________________________________________________________', style["MyStyle2"]))


    elements.append(Paragraph(u'Результаты проверки знаний:',style["MyStyle"]))
    elements.append(Paragraph(u'Правила охраны труда при работе на высоте_________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'Правилам безопастности при эксплуатации КС и устройств АБ______________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'Инструкции по безопастности для электромонтеров контактной сети______________________________', style["MyStyle2"]))

    elements.append(Paragraph(u'Заключение комиссии',style["MyStyle"]))
    elements.append(Paragraph(u'Общаяя оценка:__________________________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'Группа по безопасности на высоте:_____________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'Продолжительность стажировки:________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'_____________________________________________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'Дата следующей проверки:______________________________________________________________________________', style["MyStyle2"]))

    elements.append(Paragraph(u'Подписи:',style["MyStyle"]))
    elements.append(Paragraph(u'Председатель комиссии_________________________________________________________________П.Г. Бусыгин', style["MyStyle2"]))
    elements.append(Paragraph(u'Члены комиссии__________________________________________________________________________А.П. Бочериков', style["MyStyle2"]))
    elements.append(Paragraph(u'____________________________________________________________________________________________Ю.М. Тучин', style["MyStyle2"]))
    elements.append(Paragraph(u'', style["MyStyle2"]))
    elements.append(Paragraph(u'С заключением ознакомлен______________________________________________________________________________', style["MyStyle2"]))


    doc.build(elements)

    return buff








### --- Печатная форма списка вопросов ---
def QuestionsList(buff, res):

    Font1 = ttfonts.TTFont('PT', 'fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB', 'fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI', 'fonts/PTS56F.ttf')

    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)

    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3 * mm,
                             spaceBefore=20 * mm, alignment=1))
    style.add(ParagraphStyle(name='MyStyle1', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3 * mm,
                             spaceBefore=0 * mm, alignment=1))

    style.add(ParagraphStyle(name='MyStyle0', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=5 * mm,
                             spaceBefore=5 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle2', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=1 * mm,
                             spaceBefore=1 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle3', wordWrap=True, fontName='PT', fontSize=8, spaceAfter=1 * mm,
                             spaceBefore=1 * mm, alignment=0))

    doc = SimpleDocTemplate(buff, topMargin=10 * mm, bottomMargin=10 * mm, leftMargin=20 * mm, rightMargin=10 * mm)


    elements = []

    elements.append(Paragraph(u'Приложение 1 к протоколу № _________ (список вопросов)', style["MyStyle1"]))


    if res.data.has_key("questions_dict"):
        if (len(res.data["questions_dict"])) > 0:

            ### Формирование таблицы
            data = [[u'№пп', u'Результат', u'Вопрос'],]

            n = 1
            for item in res.data["questions_dict"]:
                data.append([n, u'Ошибка' if int(item.keys()[0], 10) in res.data["mistakes"] else u'Верно', Paragraph(item.values()[0], style["MyStyle3"]), ])
                n = n + 1

            t = Table(data, colWidths=[10 * mm, 20 * mm, 160 * mm])
            t.setStyle([('FONTNAME', (0, 0), (-1, -1), 'PTB'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, 1), 'MIDDLE'),
                        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 1), (-1, -1), 'PT'),
                        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ])



            elements.append(t)


    doc.build(elements)

    return buff









### --- Печатная протокола списком охрана труда бланк ---
def ProtocolListPDF(buff, res):
    Font1 = ttfonts.TTFont('PT', 'fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB', 'fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI', 'fonts/PTS56F.ttf')

    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)

    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3 * mm,
                             spaceBefore=20 * mm, alignment=1))
    style.add(ParagraphStyle(name='MyStyle1', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=0 * mm,
                             spaceBefore=6 * mm, alignment=1))

    style.add(ParagraphStyle(name='MyStyle0', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=5 * mm,
                             spaceBefore=5 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle2', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=0 * mm,
                             spaceBefore=4 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle3', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=0 * mm,
                             spaceBefore=0 * mm, alignment=0))

    style.add(ParagraphStyle(name='litle', wordWrap=True, fontName='PT', fontSize=4, spaceAfter=0 * mm,
                             spaceBefore=0 * mm, alignment=1))


    doc = SimpleDocTemplate(buff, topMargin=10 * mm, bottomMargin=10 * mm, leftMargin=20 * mm, rightMargin=10 * mm)

    elements = []

    elements.append(Paragraph(u'________________________________________________', style["MyStyle"]))
    elements.append(Paragraph(u'ПРОТОКОЛ № ___________', style["MyStyle1"]))
    elements.append(Paragraph(u'Заседания комиссии по проверки знаний по охране труда работников', style["MyStyle1"]))
    elements.append(Paragraph(u'"____" ___________________ 201 __г.', style["MyStyle2"]))

    elements.append(Paragraph(u'   В соответствии с приказом _________________________________________________ комиссия в составе:', style["MyStyle2"]))

    elements.append(Paragraph(u'Председателя _____________________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'членов: _____________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'Представителей:', style["MyStyle3"]))
    elements.append(Paragraph(u'администрации Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'органов местного самоуправления', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'государственной инспекции труда Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'провела проверку знаний требований охраны труда работников по <font face="PTB">Программе обучения работников _____________________________________________ по охране труда, утвержденной</font>', style["MyStyle3"]))
    elements.append(Paragraph(u'_______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(наименование программы обучения по охране труда)', style["litle"]))
    elements.append(Paragraph(u'в объеме _____________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(количество часов)', style["litle"]))



    if len(res) > 0:

        ### Формирование таблицы
        data = [[u'№пп', u'ФИО', u'Должность',
                 u'Наименование\nподразделения\n(цех, участок,\nотдел, лабора-\nтория, мастер-\nская и т.д.)',
                 u'Результат\nпроверки\n знаний (сдал,\nне сдал) №\nвыданного\nудостоверения',
                 u'Причина\nпроверки\nзнаний\n(очередная,\nвнеочередная\n и т.д.)',
                 u'Подпись\nпроверяемого',
                 ],
                [u'1', u'2', u'3', u'4', u'5', u'6', u'7'],
                ]

        n = 1
        for item in res:
            data.append([n,
                         Paragraph(item.worker, style["MyStyle3"]),
                         Paragraph(item.job, style["MyStyle3"]),
                         Paragraph(item.department, style["MyStyle3"]),
                         Paragraph(u'Сдал', style["MyStyle3"]) if item.passed else Paragraph(u'Не сдал', style["MyStyle3"]),
                         ])
            n = n + 1

        #t = Table(data, colWidths=[10 * mm, 40 * mm, 30 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm], repeatRows=1)
        t = Table(data, colWidths=[10 * mm, 40 * mm, 30 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm])
        t.setStyle([('FONTNAME', (0, 0), (-1, -1), 'PTB'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, 2), 'MIDDLE'),
                    ('ALIGN', (1, 2), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'PT'),
                    ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ])

        elements.append(t)


    elements.append(Paragraph(u'Председатель комиссии __________________________________________________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'члены комиссии: _____________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'Представители:', style["MyStyle3"]))
    elements.append(Paragraph(u'администрации Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'органов местного самоуправления', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'государственной инспекции труда Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))



    doc.build(elements)

    return buff








### --- Печатная протокола списком охрана труда Крпасноярск---
def ProtocolListPDF3(buff, res):
    Font1 = ttfonts.TTFont('PT', 'fonts/PTC55F.ttf')
    Font2 = ttfonts.TTFont('PTB', 'fonts/PTC75F.ttf')
    Font3 = ttfonts.TTFont('PTI', 'fonts/PTS56F.ttf')

    pdfmetrics.registerFont(Font1)
    pdfmetrics.registerFont(Font2)
    pdfmetrics.registerFont(Font3)

    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='MyStyle', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=3 * mm,
                             spaceBefore=20 * mm, alignment=1))
    style.add(ParagraphStyle(name='MyStyle1', wordWrap=True, fontName='PTB', fontSize=12, spaceAfter=0 * mm,
                             spaceBefore=6 * mm, alignment=1))

    style.add(ParagraphStyle(name='MyStyle0', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=5 * mm,
                             spaceBefore=5 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle2', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=0 * mm,
                             spaceBefore=4 * mm, alignment=0))
    style.add(ParagraphStyle(name='MyStyle3', wordWrap=True, fontName='PT', fontSize=10, spaceAfter=0 * mm,
                             spaceBefore=0 * mm, alignment=0))

    style.add(ParagraphStyle(name='litle', wordWrap=True, fontName='PT', fontSize=4, spaceAfter=0 * mm,
                             spaceBefore=0 * mm, alignment=1))


    doc = SimpleDocTemplate(buff, topMargin=10 * mm, bottomMargin=10 * mm, leftMargin=20 * mm, rightMargin=10 * mm)

    elements = []

    elements.append(Paragraph(u'Закрытое акционерное общество  "СибТрансТелеКом"', style["MyStyle"]))
    elements.append(Paragraph(u'ПРОТОКОЛ № ___________', style["MyStyle1"]))
    elements.append(Paragraph(u'Заседания комиссии по проверки знаний по охране труда работников', style["MyStyle1"]))
    elements.append(Paragraph(u'"____" ___________________ 201 __г.', style["MyStyle2"]))

    elements.append(Paragraph(u'   В соответствии с приказом генерального директора от 27 июня 2017 г. № 30 комиссия в составе:', style["MyStyle2"]))

    elements.append(Paragraph(u'Председателя: Бочерикова Андрея Павловича - заместителя Технического директора - Начальника службы эксплуатации магистральной сети', style["MyStyle2"]))
    #elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'членов:', style["MyStyle3"]))
    elements.append(Paragraph(u'1. Бусыгина Павла Генриховича, главного энергетика экспертного отдела', style["MyStyle3"]))
    elements.append(Paragraph(u'2. Тучина Юрия Михайловича, инженера электропитающих установок', style["MyStyle3"]))

    #elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))
    #elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    #elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'Представителей:', style["MyStyle3"]))
    elements.append(Paragraph(u'администрации Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'органов местного самоуправления', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'государственной инспекции труда Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , должность)', style["litle"]))

    elements.append(Paragraph(u'провела проверку знаний требований охраны труда работников по <font face="PTB">Программе обучения работников ЗАО "СибТрансТелеКом" по охране труда, утвержденной</font>', style["MyStyle3"]))
    elements.append(Paragraph(u'_______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(наименование программы обучения по охране труда)', style["litle"]))
    elements.append(Paragraph(u'в объеме _____________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(количество часов)', style["litle"]))



    if len(res) > 0:

        ### Формирование таблицы
        data = [[u'№пп', u'ФИО', u'Должность',
                 u'Наименование\nподразделения\n(цех, участок,\nотдел, лабора-\nтория, мастер-\nская и т.д.)',
                 u'Результат\nпроверки\n знаний (сдал,\nне сдал) №\nвыданного\nудостоверения',
                 u'Причина\nпроверки\nзнаний\n(очередная,\nвнеочередная\n и т.д.)',
                 u'Подпись\nпроверяемого',
                 ],
                [u'1', u'2', u'3', u'4', u'5', u'6', u'7'],
                ]

        n = 1
        for item in res:
            data.append([n,
                         Paragraph(item.worker, style["MyStyle3"]),
                         Paragraph(item.job, style["MyStyle3"]),
                         Paragraph(item.department, style["MyStyle3"]),
                         Paragraph(u'Сдал', style["MyStyle3"]) if item.passed else Paragraph(u'Не сдал', style["MyStyle3"]),
                         ])
            n = n + 1

        #t = Table(data, colWidths=[10 * mm, 40 * mm, 30 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm], repeatRows=1)
        t = Table(data, colWidths=[10 * mm, 40 * mm, 30 * mm, 25 * mm, 25 * mm, 25 * mm, 25 * mm])
        t.setStyle([('FONTNAME', (0, 0), (-1, -1), 'PTB'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, 2), 'MIDDLE'),
                    ('ALIGN', (1, 2), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 1), (-1, -1), 'PT'),
                    ('VALIGN', (0, 1), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ])

        elements.append(t)


    elements.append(Paragraph(u'Председатель комиссии Бочериков Андрей Павлович _____________________________________', style["MyStyle2"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'члены комиссии: 1. Бусыгин Павел Генрихович ____________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'2. Тучин Юрий Михайлович ________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'Представители:', style["MyStyle3"]))
    elements.append(Paragraph(u'администрации Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'органов местного самоуправления', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))

    elements.append(Paragraph(u'государственной инспекции труда Красноярского края', style["MyStyle3"]))
    elements.append(Paragraph(u'______________________________________________________________________________________________________', style["MyStyle3"]))
    elements.append(Paragraph(u'(Ф.И.О. , подпись)', style["litle"]))



    doc.build(elements)

    return buff


