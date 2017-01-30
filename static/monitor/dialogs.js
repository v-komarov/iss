$(document).ready(function() {

    window.iss;

    $("ul.dropdown-menu li a[action=create-accident]").bind("click",Accident);
    $("ul.dropdown-menu li a[action=accident-iss]").bind("click",AccidentISS);
    $("button#addaddr").bind("click",AddAccidentAddressList);
    $("ul.dropdown-menu li a[action=message-accidentmmsbegin]").bind("click",MessageMssBegin);

    $("#write-address-data").bind("click",WriteAddressData);


    //// Валидация
    $("#eventform").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            event_class: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_system: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_group: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_class: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_net_address: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_location: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            element_identifier: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
          },

    });// Валидация



    $("#eventform table tbody tr td input").change(function(e) {
        $("#eventform").validate().element($(e.target));
    })





    //// Валидация
    $("#mailform").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            event_class: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_system: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_group: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_class: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_net_address: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            device_location: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            element_identifier: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
          },

    });// Валидация



    $("#mailform table tbody tr td input").change(function(e) {
        $("#mailform").validate().element($(e.target));
    })



/*
    //// Валидация
    $("#accidentform").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            acc-datetime-begin: {
                required: true
            },
            acc-cat-type: {
                required: true
            },
            acc-reason: {
                required: true
            },
            acc-cities: {
                required: true
            },
            acc-address-list: {
                required: true
            },
            acc-zkl: {
                required: true
            },
            acc-email-list: {
                required: true
            },
            acc-service-stoplist: {
                required: true
            },
          },

    });// Валидация



    $("#accidentform table tbody tr td input").change(function(e) {
        $("#accidentform").validate().element($(e.target));
    })

*/






    //// Валидация
    $("#message-mb").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            accidentcat: {
                required: true
            },
            accidenttype: {
                required: true
            },
            accidentname: {
                required: true,
                minlength: 5,
                maxlength: 100
            },
          },

    });// Валидация



    $("#message-mb table tbody tr td input").change(function(e) {
        $("#message-mb").validate().element($(e.target));
    })











    // Выбор почтового сообщения для отображения
    $("#maillist").change(function(e) {
        var mail_id = $(this).val()
        var event_id =  $("#mail table").attr("event_id");
        // Отображение содержимого письма
        if (mail_id != "") {

            var jqxhr = $.getJSON("/monitor/events/jsondata?getmail=ok&mail_id="+mail_id+"&event_id="+event_id,
                function(data) {
                    $("#mailtext subj").text(data["subject"]);
                    $("#mailtext mailtext").text(data["body"]);
                        $("#mailtext dl attachement").empty();

                        data['files'].forEach(function(item,i,arr){
                            $("#mailtext dl attachement").append("<dd><a href=\"/monitor/events/filedata?event_id="+$("#mail table").attr("event_id")+"&filename="+item+"\">"+item+"</a></dd>");
                        })

                })

        }

        else {
            $("#mailtext subj").text("");
            $("#mailtext mailtext").text("");
            $("#mailtext dl attachement").empty();
            }

    });



    // Со строками содержимого контейнера
    $(document).on({
        click:function() {
            $("table[group=group] tbody tr[group=members]").css("background-color","#C0C0C0");
            $(this).css("background-color","#F0E68C");
            $("table[group=group] tbody tr[group=members]").attr("marked","no");
            $(this).attr("marked","yes");

            if ($(this).attr("bymail") == "yes") {
                ShowMail();
            }

        }
    },"table[group=group] tbody tr[group=members]");





    // Выбор почтового сообщения для отображения (вариант для содержимого контейнера)
    $("#maillist2").change(function(e) {
        var mail_id = $(this).val()
        var event_id =  $("#mail2 table").attr("event_id");
        // Отображение содержимого письма
        if (mail_id != "") {

            var jqxhr = $.getJSON("/monitor/events/jsondata?getmail=ok&mail_id="+mail_id+"&event_id="+event_id,
                function(data) {
                    $("#mailtext2 subj").text(data["subject"]);
                    $("#mailtext2 mailtext").text(data["body"]);
                        $("#mailtext2 dl attachement").empty();

                        data['files'].forEach(function(item,i,arr){
                            $("#mailtext2 dl attachement").append("<dd><a href=\"/monitor/events/filedata?event_id="+$("#mail2 table").attr("event_id")+"&filename="+item+"\">"+item+"</a></dd>");
                        })

                })

        }

        else {
            $("#mailtext2 subj").text("");
            $("#mailtext2 mailtext").text("");
            $("#mailtext2 dl attachement").empty();
            }

    });



    /*
    // Список услуг
    $("#service_stoplist").multiselect({
        header:true,
        noneSelectedText:"Выбор услуг",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#service_stoplist").multiselect("uncheckAll");
    */






    // Поиск адреса
    $("#accidentaddress").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#accidentdata',
        position: 'top',
        select: function (event,ui) {
            $("#accidentaddress").val(ui.item.label);
            window.address_id = ui.item.value;
            window.address_label = ui.item.label;

            return false;
        },
        focus: function (event,ui) {
            $("#accidentaddress").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    })





});








function DeleteAccidentAddressList(e) {

    var address_id = $(this).closest("dt").attr("addressid");
    $("#address-accident-list dt[addressid="+address_id+"]").remove();
    $("#address-accident-list dd[addressid="+address_id+"]").remove();

}


function AddAccidentAddressList(e) {

    t = "<dt addressid=\'"+address_id+"\'><a href=\"#\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></dt>"
    +"<dd addressid=\'"+address_id+"\' addresslabel=\'"+address_label+"\'>"
    + address_label
    + "</dd>"

    $("#address-accident-list").prepend(t);

    $("#address-accident-list dt a").bind("click",DeleteAccidentAddressList);

}



// Изменение видимости строки адреса оборудования
function ChangeAccidentAddressList(e) {

    $("#address-accident-devices-list dt a").unbind("click");

    var showitem = $(this).closest("dt").attr("showitem");

    if ( showitem == "yes" ) {
        $(this).closest("dt").attr("showitem","no");
        $(this).closest("dt").next("dd").attr("showitem","no");
        $(this).children("span").toggleClass("glyphicon-eye-open",false);
        $(this).children("span").toggleClass("glyphicon-eye-close",true);
        $(this).closest("dt").next("dd").css("text-decoration","line-through");
    }

    else {
        $(this).closest("dt").attr("showitem","yes");
        $(this).closest("dt").next("dd").attr("showitem","yes");
        $(this).children("span").toggleClass("glyphicon-eye-open",true);
        $(this).children("span").toggleClass("glyphicon-eye-close",false);
        $(this).closest("dt").next("dd").css("text-decoration","none");
    }

    $("#address-accident-devices-list dt a").bind("click",ChangeAccidentAddressList);

}





function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}





function getCookie(name) {

    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






// Выбор аварии - новая или редактирование уже созданной
function Accident() {

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    var accident = $("table[group=events] tbody tr[row_id="+row_id+"]").attr("accident");

    // Взависимости от атрибута accident=yes или accident=no
    if (accident == "yes") {
        EditAccident(row_id);
    }
    else {
        CreateAccident();
    }

}








function CreateAccident() {

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getaccidentipaddress="+row_id,
        function(data) {


        // Очистка
        $("#accidentcat").val("");
        $("#accidenttype").val("");
        $("#accidentname").val("Недоступно оборудование г. ");
        $("#accidentcomment").val("");
        $("#accidentaddress").val("");
        $("#address-accident-list").empty();
        $("#accidentend").prop("checked",false);
        $("#accidentstat").prop("checked",false);
        $("#accidentdata").attr("action","create-accident");
        $("#accidentreason").val("");
        $("#accidentrepair").val("");
        $("#accidentaddresscomment").val("");

        $("accident-link").text("");

        // Предварительная очистка списка
        $("#address-accident-devices-list").empty();

        $.each(data['address_list'], function(index,value){

            var v = value;

            t = "<dt addressid=\'"+v['addressid']+"\' showitem=\"yes\"><a href=\"#\"><span class=\"glyphicon glyphicon-eye-open\" aria-hidden=\"true\"></span></a></dt>"
            +"<dd addressid=\'"+v['addressid']+"\' addresslabel=\'"+v['addresslabel']+"\' showitem=\'yes\'>"
            + v['addresslabel']
            + "</dd>"

            $("#address-accident-devices-list").prepend(t);
            $("#address-accident-devices-list dt a").bind("click",ChangeAccidentAddressList);

        });


        AccidentData();

    })

}








function EditAccident(row_id) {


    $("#accidentdata").attr("action","edit-accident");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getaccidentdata="+row_id,
        function(data) {

            $("#accidentcat").val(data['acccat']);
            $("#accidenttype").val(data['acctype']);
            $("#accidentname").val(data['accname']);
            $("#accidentcomment").val(data['acccomment']);
            $("#accidentreason").val(data['accreason']);
            $("#accidentrepair").val(data['accrepair']);
            $("#accidentaddress").val("");
            $("#address-accident-list").empty();
            $("#accidentaddresscomment").val(data['accaddrcomment']);

            // Номер аварии и ссылка на url ИСС
            //$("accident-link").text("Авария № "+data['accid']+" ");
            //if (data["accissid"] != 0) { $("accident-link").append("<a href=\"http://10.6.3.7/departs/rcu/works/edit_work_mss.php?id="+data["accissid"]+"\">Работа (в ИСС) № "+data["accissid"]+"</a>"); }


            // Открытие окна в ИСС
            //window.open("http://10.6.3.7/departs/rcu/works/edit_work_mss.php?id="+data["accissid"]);


            if (data["accend"] == "yes") { $("#accidentend").prop("checked",true); }
            else { $("#accidentend").prop("checked",false); }

            // Включение в статистику
            if (data["accstat"] == "yes") { $("#accidentstat").prop("checked",true); }
            else { $("#accidentstat").prop("checked",false); }

            // Список адресов оборудования
            // Предварительная очистка списка
            $("#address-accident-devices-list").empty();
            $.each(data['accdevaddress']['address_list'], function(index,value){

                var v = value;

                if ( v["showitem"] == "yes" ) {

                    t = "<dt addressid=\'"+v['addressid']+"\' showitem=\"yes\"><a href=\"#\"><span class=\"glyphicon glyphicon-eye-open\" aria-hidden=\"true\"></span></a></dt>"
                    +"<dd addressid=\'"+v['addressid']+"\' addresslabel=\'"+v['addresslabel']+"\' showitem=\'yes\'>"
                    + v['addresslabel']
                    + "</dd>"

                }

                else (

                    t = "<dt addressid=\'"+v['addressid']+"\' showitem=\"no\"><a href=\"#\"><span class=\"glyphicon glyphicon-eye-close\" aria-hidden=\"true\"></span></a></dt>"
                    +"<dd style=\"text-decoration:line-through;\" addressid=\'"+v['addressid']+"\' addresslabel=\'"+v['addresslabel']+"\' showitem=\'no\'>"
                    + v['addresslabel']
                    + "</dd>"

                )


                $("#address-accident-devices-list").prepend(t);
                $("#address-accident-devices-list dt a").bind("click",ChangeAccidentAddressList);

            });


            // Список адресов введенных вручную
            $.each(data['address']['address_list'], function(index,value){

                var v = value;

                t = "<dt addressid=\'"+v['addressid']+"\'><a href=\"#\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></dt>"
                +"<dd addressid=\'"+v['addressid']+"\' addresslabel=\'"+v['addresslabel']+"\'>"
                + v['addresslabel']
                + "</dd>"

                $("#address-accident-list").prepend(t);
                $("#address-accident-list dt a").bind("click",DeleteAccidentAddressList);

            });

        })

    AccidentData();

}







function AccidentData() {



            $("#accidentdata").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                title:"Авария",
                closeOnEscape: false,
                buttons:[{ text:"Сохранить",click: function() {
                    if ($('#accidenttype').valid() && $('#accidentcat').valid() && $('#accidentname').valid()) {

                        // Данные
                        var acccat = $("#accidentcat").val();
                        var acctype = $("#accidenttype").val();
                        var accname = $("#accidentname").val();
                        var acccomment = $("#accidentcomment").val();
                        var accreason = $("#accidentreason").val();
                        var accrepair = $("#accidentrepair").val();
                        var acc_addr = $("#address-accident-list dd");
                        if ($("#accidentend").prop("checked") == true) { var accend = "yes"; }
                        else { var accend = "no"; }
                        if ($("#accidentstat").prop("checked") == true) { var accstat = "yes"; }
                        else { var accstat = "no"; }
                        var accaddrcomment = $("#accidentaddresscomment").val();


                        address_arr = [];

                        $.each($("#address-accident-list dd"), function( index, value ) {
                            var row = {};
                            row.addressid = $(value).attr("addressid");
                            row.addresslabel = $(value).attr("addresslabel");
                            address_arr.push(row);
                        });


                        device_address_arr = [];

                        $.each($("#address-accident-devices-list dd"), function( index, value ) {
                            var row = {};
                            row.addressid = $(value).attr("addressid");
                            row.addresslabel = $(value).attr("addresslabel");
                            row.showitem = $(value).attr("showitem");
                            device_address_arr.push(row);
                        });


                        var data = {};
                        data.device_address = device_address_arr;
                        data.address_list = address_arr;
                        data.acccat = acccat;
                        data.acctype = acctype;
                        data.accname = accname;
                        data.acccomment = acccomment;
                        data.accend = accend;
                        data.accstat = accstat;
                        data.accreason = accreason;
                        data.accrepair = accrepair;
                        data.addrcomment = accaddrcomment;
                        data.event_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
                        data.action = $("#accidentdata").attr("action");


                        var csrftoken = getCookie('csrftoken');

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });





                        $.ajax({
                          url: "/monitor/events/jsondata/",
                          type: "POST",
                          dataType: 'json',
                          data:$.toJSON(data),
                            success: function(result) {
                                location.reload();
                            }

                        });


                        $(this).dialog("close");
                        $("table[group=events]").attr("refresh","yes");



                    }

                }},
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close");$("table[group=events]").attr("refresh","yes");}}
                ],
                modal:true,
                minWidth:400,
                width:500,
                height:550

            });



}






// Заполнение поля формы  аварии "Название" по клику "заполнить"
function WriteAddressData(e) {

        address_arr = [];

        $.each($("#address-accident-list dd"), function( index, value ) {
            var row = {};
            row.addressid = $(value).attr("addressid");
            address_arr.push(row);
        });

        $.each($("#address-accident-devices-list dd"), function( index, value ) {
            var row = {};
            row.addressid = $(value).attr("addressid");
            address_arr.push(row);
        });


        var data = {};
        data.address_list = address_arr;
        data.action = "writeaddressdata";


        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        $.ajax({
          url: "/monitor/events/jsondata/",
          type: "POST",
          dataType: 'json',
          data:$.toJSON(data),
            success: function(result) {

                $("#accidentname").val("Недоступно оборудование г. "+result['address']);

            }

        });



}









// Ссылка на аварию в ИСС
function AccidentISS(e) {

    // Проверка есть ли авария в данной строке таблицы
    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    var accident = $("table[group=events] tbody tr[row_id="+row_id+"]").attr("accident");

    if (accident == "yes") {
    // Если авария уже создана (и в ИСС тоже)
        var jqxhr = $.getJSON("/monitor/events/jsondata?getaccidentdata="+row_id,
            function(data) {

                // Открытие окна в ИСС
                window.open("http://10.6.3.7/departs/rcu/works/edit_work_mss.php?id="+data["accissid"]);

            })

        }

}







function ShowMail() {


    $("#maillist2").empty();
    $("#maillist2").append($("<option value=\"\" selected></option>"));
    $("#mailtext2 subj").text("");
    $("#mailtext2 mailtext").text("");
    $("#mailtext2 dl attachement").empty();

    var row_id = $("table[group=group] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getevent="+row_id,
        function(data) {

            $("#mail2 table").attr("event_id",data['id']);

            $("#mail2 table tbody tr td select#status").val(data['status']);
            $("#mail2 table tbody tr td select#severity").val(data['severity']);

            $("#mail2 table tbody tr td input#event_class").val(data['event_class']);
            $("#mail2 table tbody tr td input#device_system").val(data['device_system']);
            $("#mail2 table tbody tr td input#device_group").val(data['device_group']);
            $("#mail2 table tbody tr td input#device_class").val(data['device_class']);
            $("#mail2 table tbody tr td input#device_net_address").val(data['device_net_address']);
            $("#mail2 table tbody tr td input#device_location").val(data['device_location']);
            $("#mail2 table tbody tr td input#element_identifier").val(data['element_identifier']);
            $("#mail2 table tbody tr td input#element_sub_identifier").val(data['element_sub_identifier']);


            data['list_mail'].forEach(function(item,i,arr){
                $("#maillist2").append($("<option value="+item['id_mail']+">"+item['label_mail']+"</option>"));

            })


            $("#mail2").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                title:"Почтовое сообщение",
                buttons:[
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close"); $("table[group=events]").attr("refresh","yes"); }}
                ],
                modal:true,
                minWidth:400,
                width:700


            });


        })


}











function EditMail(e) {


    $("#maillist").empty();
    $("#maillist").append($("<option value=\"\" selected></option>"));
    $("#mailtext subj").text("");
    $("#mailtext mailtext").text("");
    $("#mailtext dl attachement").empty();

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getevent="+row_id,
        function(data) {

            $("#mail table").attr("event_id",data['id']);

            $("#mail table tbody tr td select#status").val(data['status']);
            $("#mail table tbody tr td select#severity").val(data['severity']);

            $("#mail table tbody tr td input#event_class").val(data['event_class']);
            $("#mail table tbody tr td input#device_system").val(data['device_system']);
            $("#mail table tbody tr td input#device_group").val(data['device_group']);
            $("#mail table tbody tr td input#device_class").val(data['device_class']);
            $("#mail table tbody tr td input#device_net_address").val(data['device_net_address']);
            $("#mail table tbody tr td input#device_location").val(data['device_location']);
            $("#mail table tbody tr td input#element_identifier").val(data['element_identifier']);
            $("#mail table tbody tr td input#element_sub_identifier").val(data['element_sub_identifier']);


            data['list_mail'].forEach(function(item,i,arr){
                $("#maillist").append($("<option value="+item['id_mail']+">"+item['label_mail']+"</option>"));

            })


            $("#mail").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                title:"Почтовое сообщение",
                closeOnEscape: false,
                buttons:[{ text:"Сохранить",click: function() {
                    if ($('#event_class').valid() && $('#device_system').valid() && $('#device_group').valid() && $('#device_class').valid() && $('#device_net_address').valid() && $('#device_location').valid() && $('#element_identifier').valid()) {

                        var event_id = $("#mail table").attr("event_id");

                        var status = $("#mail table tbody tr td select#status").val();
                        var severity = $("#mail table tbody tr td select#severity").val();

                        var event_class = $("#mail table tbody tr td input#event_class").val();
                        var device_system = $("#mail table tbody tr td input#device_system").val();
                        var device_group = $("#mail table tbody tr td input#device_group").val();
                        var device_class = $("#mail table tbody tr td input#device_class").val();
                        var device_net_address = $("#mail table tbody tr td input#device_net_address").val();
                        var device_location = $("#mail table tbody tr td input#device_location").val();
                        var element_identifier = $("#mail table tbody tr td input#element_identifier").val();
                        var element_sub_identifier = $("#mail table tbody tr td input#element_sub_identifier").val();

                        var csrftoken = getCookie('csrftoken');

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });



                        $.ajax({
                          url: "/monitor/events/jsondata/",
                          type: "POST",
                          dataType: 'text',
                          data:"{"
                            +"'event_id':'"+event_id+"',"
                            +"'action':'edit_event',"
                            +"'status':"+status+","
                            +"'severity':"+severity+","
                            +"'event_class':'"+event_class+"',"
                            +"'device_system':'"+device_system+"',"
                            +"'device_group':'"+device_group+"',"
                            +"'device_class':'"+device_class+"',"
                            +"'device_net_address':'"+device_net_address+"',"
                            +"'device_location':'"+device_location+"',"
                            +"'element_identifier':'"+element_identifier+"',"
                            +"'element_sub_identifier':'"+element_sub_identifier+"'"
                            +"}",
                            success: function(result) {
                                window.location=$("#menumonitor a").attr("href");
                            }

                        })

                    }

                }},
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close"); $("table[group=events]").attr("refresh","yes");}}
                ],
                modal:true,
                minWidth:400,
                width:700

            });







        })


}








// Изменение события , введенного вручную
function EditRow(e) {

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getevent="+row_id,
        function(data) {

            $("#event table").attr("event_id",data['id']);

            $("#event table tbody tr td select#status").val(data['status']);
            $("#event table tbody tr td select#severity").val(data['severity']);

            $("#event table tbody tr td input#event_class").val(data['event_class']);
            $("#event table tbody tr td input#device_system").val(data['device_system']);
            $("#event table tbody tr td input#device_group").val(data['device_group']);
            $("#event table tbody tr td input#device_class").val(data['device_class']);
            $("#event table tbody tr td input#device_net_address").val(data['device_net_address']);
            $("#event table tbody tr td input#device_location").val(data['device_location']);
            $("#event table tbody tr td input#element_identifier").val(data['element_identifier']);
            $("#event table tbody tr td input#element_sub_identifier").val(data['element_sub_identifier']);





            $("#event").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                title:"Изменение события",
                closeOnEscape: false,
                buttons:[{ text:"Сохранить",click: function() {
                    if ($('#event_class').valid() && $('#device_system').valid() && $('#device_group').valid() && $('#device_class').valid() && $('#device_net_address').valid() && $('#device_location').valid() && $('#element_identifier').valid()) {

                        var event_id = $("#event table").attr("event_id");

                        var status = $("#event table tbody tr td select#status").val();
                        var severity = $("#event table tbody tr td select#severity").val();

                        var event_class = $("#event table tbody tr td input#event_class").val();
                        var device_system = $("#event table tbody tr td input#device_system").val();
                        var device_group = $("#event table tbody tr td input#device_group").val();
                        var device_class = $("#event table tbody tr td input#device_class").val();
                        var device_net_address = $("#event table tbody tr td input#device_net_address").val();
                        var device_location = $("#event table tbody tr td input#device_location").val();
                        var element_identifier = $("#event table tbody tr td input#element_identifier").val();
                        var element_sub_identifier = $("#event table tbody tr td input#element_sub_identifier").val();



                        var csrftoken = getCookie('csrftoken');

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });



                        $.ajax({
                          url: "/monitor/events/jsondata/",
                          type: "POST",
                          dataType: 'text',
                          data:"{"
                            +"'event_id':'"+event_id+"',"
                            +"'action':'edit_event',"
                            +"'status':"+status+","
                            +"'severity':"+severity+","
                            +"'event_class':'"+event_class+"',"
                            +"'device_system':'"+device_system+"',"
                            +"'device_group':'"+device_group+"',"
                            +"'device_class':'"+device_class+"',"
                            +"'device_net_address':'"+device_net_address+"',"
                            +"'device_location':'"+device_location+"',"
                            +"'element_identifier':'"+element_identifier+"',"
                            +"'element_sub_identifier':'"+element_sub_identifier+"'"
                            +"}",
                            success: function(result) {
                                window.location=$("#menumonitor a").attr("href");
                            }

                        })

                    }

                }},
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close");$("table[group=events]").attr("refresh","yes");}}
                ],
                modal:true,
                minWidth:400,
                width:700

            });







        })





}





// Добавить строку события
function AddRow(e) {

    $("#event table tbody tr td input#event_class").val("");
    $("#event table tbody tr td input#device_system").val("");
    $("#event table tbody tr td input#device_group").val("");
    $("#event table tbody tr td input#device_class").val("");
    $("#event table tbody tr td input#device_net_address").val("");
    $("#event table tbody tr td input#device_location").val("");
    $("#event table tbody tr td input#element_identifier").val("");
    $("#event table tbody tr td input#element_sub_identifier").val("");

    $("#event").dialog({
        open:function() {
        $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
        $("table[group=events]").attr("refresh","no");
        },
        title:"Создание события",
        closeOnEscape: false,
        buttons:[{ text:"Сохранить",click: function() {
            if ($('#event_class').valid() && $('#device_system').valid() && $('#device_group').valid() && $('#device_class').valid() && $('#device_net_address').valid() && $('#device_location').valid() && $('#element_identifier').valid()) {
                var status = $("#event table tbody tr td select#status").val();
                var severity = $("#event table tbody tr td select#severity").val();

                var event_class = $("#event table tbody tr td input#event_class").val();
                var device_system = $("#event table tbody tr td input#device_system").val();
                var device_group = $("#event table tbody tr td input#device_group").val();
                var device_class = $("#event table tbody tr td input#device_class").val();
                var device_net_address = $("#event table tbody tr td input#device_net_address").val();
                var device_location = $("#event table tbody tr td input#device_location").val();
                var element_identifier = $("#event table tbody tr td input#element_identifier").val();
                var element_sub_identifier = $("#event table tbody tr td input#element_sub_identifier").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });



                $.ajax({
                  url: "/monitor/events/jsondata/",
                  type: "POST",
                  dataType: 'text',
                  data:"{"
                    +"'action':'create_event',"
                    +"'status':"+status+","
                    +"'severity':"+severity+","
                    +"'event_class':'"+event_class+"',"
                    +"'device_system':'"+device_system+"',"
                    +"'device_group':'"+device_group+"',"
                    +"'device_class':'"+device_class+"',"
                    +"'device_net_address':'"+device_net_address+"',"
                    +"'device_location':'"+device_location+"',"
                    +"'element_identifier':'"+element_identifier+"',"
                    +"'element_sub_identifier':'"+element_sub_identifier+"'"
                    +"}",
                    success: function(result) {
                        window.location=$("#menumonitor a").attr("href");
                    }

                })

            }

        }},
            {text:"Закрыть",click: function() {
            $(this).dialog("close");$("table[group=events]").attr("refresh","yes");}}
        ],
        modal:true,
        minWidth:400,
        width:700

    });

}














// Оповещение об аварии на MCC
function MessageMssBegin(e) {


    // Для формы отправки оповещения - отображение списка адресов
    $( "#acc-email-templates" ).change(function() {
        var address_list = $("#acc-email-templates option:selected").attr("address_list");
        $("#acc-email-list").val(address_list);
    });


    // Сообщение еще не создавалось
    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    var accident = $("table[group=events] tbody tr[row_id="+row_id+"]").attr("accident");
    var mcc_mail_begin = $("table[group=events] tbody tr[row_id="+row_id+"]").attr("mcc-mail-begin");
    // Авария не создавалась - ничего не делать
    if (accident != "yes") { return;}

    // Почтовое сообщение не создавалось
    if (mcc_mail_begin == "no") {

        var jqxhr = $.getJSON("/monitor/events/jsondata?mailaccidentdata="+row_id+"&mcc_mail_begin=no",
            function(data) {

                $("#acc-datetime-begin").val(data['acc_start']);
                $("#acc-cat-type").val(data['acccat']+","+data['acctype']);
                $("#acc-reason").val(data['accreason']);
                $("#acc-cities").val(data['acccities']);
                $("#acc-address-list").val(data['accaddresslist']);
                $("#acc-zkl").val(data['acczkl']);
                $("#acc-email-templates").val("");
                $("#acc-email-list").val("");
                $("#acc-repair-end").val("Уточняется");
                $("#acc-service-stoplist").val("");

            })



    }
    // Почтовое сообщение уже было создано
    else {

        var jqxhr = $.getJSON("/monitor/events/jsondata?mailaccidentdata="+row_id+"&mcc_mail_begin=yes",

            function(data) {


                $("#acc-datetime-begin").val(data['acc_start']);
                $("#acc-cat-type").val(data['acccattype']);
                $("#acc-reason").val(data['accreason']);
                $("#acc-cities").val(data['acccities']);
                $("#acc-address-list").val(data['accaddresslist']);
                $("#acc-zkl").val(data['acczkl']);
                $("#acc-email-templates").val(data['acc_email_templates']);
                $("#acc-email-list").val(data['acc_email_list']);
                $("#acc-repair-end").val(data['acc_repair_end']);
                $("#acc-service-stoplist").val(data['acc_service_stoplist']);

            })

    }


    var jqxhr = $.getJSON("/monitor/events/jsondata?issaccidentok="+row_id,
    function(data) {

        if (data["iss"] == "yes") {

            $("#message-mss-begin").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                title:"Оповещение об аварии на MCC",
                closeOnEscape: false,
                buttons:[{ text:"Отправить",click: function() {

                    if ($('#acc-datetime-begin').valid() && $('#acc-cat-type').valid() && $('#acc-reason').valid() && $('#acc-cities').valid() && $('#acc-address-list').valid() && $('#acc-zkl').valid() && $('#acc-email-list').valid() && $('#acc-service-stoplist').valid()) {


                        var acc_datetime_begin = $("#acc-datetime-begin").val();
                        var acc_cat_type = $("#acc-cat-type").val();
                        var acc_reason = $("#acc-reason").val();
                        var acc_cities = $("#acc-cities").val();
                        var acc_address_list = $("#acc-address-list").val();
                        var acc_zkl = $("#acc-zkl").val();
                        var acc_email_templates = $("#acc-email-templates").val();
                        var acc_email_list = $("#acc-email-list").val();
                        var acc_service_stoplist = $("#acc-service-stoplist").val();
                        var acc_repair_end = $("#acc-repair-end").val();


                        var data = {};
                        data.acc_datetime_begin = acc_datetime_begin;
                        data.acc_cat_type = acc_cat_type;
                        data.acc_reason = acc_reason;
                        data.acc_cities = acc_cities;
                        data.acc_address_list = acc_address_list;
                        data.acc_zkl = acc_zkl;
                        data.acc_email_templates = acc_email_templates;
                        data.acc_email_list = acc_email_list;
                        data.acc_service_stoplist = acc_service_stoplist;
                        data.acc_repair_end = acc_repair_end;
                        data.event_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
                        data.action = "create-mcc-message-email";




                        var csrftoken = getCookie('csrftoken');

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                        });



                        $.ajax({
                          url: "/monitor/events/jsondata/",
                          type: "POST",
                          dataType: 'json',
                          data:$.toJSON(data),
                            success: function(result) {
                                location.reload();
                            }

                        });


                        $(this).dialog("close");
                        $("table[group=events]").attr("refresh","yes");




                    }

                }},
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close");$("table[group=events]").attr("refresh","yes");}}
                ],
                modal:true,
                minWidth:600,
                width:900

            });

        }
        else { alert("Авария не зарегистрирована в ИСС!"); }

    })


}







