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




### --- Печастная форма списка вопросов ---
def	QuestionsList(buff, res):



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


    """
    data = [['№\nпп','Наименование\nматериалов','Ед.\nизм.','Коли-\nчество','Примечание'],
	    ['1','2','3','4','5'],
	    ]
    n = 1
    for item in spec:
	data.append([n,Paragraph(item[2],style["MyStyle2"]),item[3],item[4],''])
	n = n + 1



    t=Table(data,colWidths=[10*mm,90*mm,20*mm,20*mm,40*mm])
    t.setStyle([('FONTNAME',(0,0),(-1,1),'PTB'),
		('FONTSIZE',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,1),'CENTER'),
		('VALIGN',(0,0),(-1,1),'MIDDLE'),
		('ALIGN',(0,2),(-1,-1),'LEFT'),
		('FONTNAME',(0,2),(-1,-1),'PT'),
		('VALIGN',(0,2),(-1,-1),'TOP'),
		('GRID',(0,0),(-1,-1),0.25,colors.black),
		])

    Tdata = [['','Номер\nдокумента','Дата\nсоставления'],
	    ['ВНУТРЕННИЙ ЗАКАЗ',order[0],order[1]]]


    TableHead=Table(Tdata)
    TableHead.setStyle([('FONTNAME',(0,0),(-1,-1),'PTB'),
		('FONTSIZE',(0,0),(-1,-1),10),
		('ALIGN',(0,0),(-1,-1),'CENTER'),
		('VALIGN',(0,0),(-1,-1),'MIDDLE'),
		('GRID',(1,0),(-1,-1),0.25,colors.black),
		])

    """
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


    """
    elements.append(TableHead)
    elements.append(Paragraph('Шифр затрат : %s' % order[5].encode("utf-8"),style["MyStyle0"]))
    elements.append(t)
    elements.append(Paragraph('Получатель подпись:__________________ расшифровка подписи: %s %s.%s.' % (executer.j['name1'].encode("utf-8"),executer.j['name2'][:1].encode("utf-8"),executer.j['name3'][:1].encode("utf-8")),style["MyStyle0"]))
    """

    doc.build(elements)

    return buff
