$(document).ready(function() {

    $("table[group=accidents] tbody tr").bind("click",ClickEventRow);
    $("#editrow").hide(); // первоначально если строка не выделена, то кнопку редактирования прячем
    $("#editrow").bind("click",EditAccident);
    $("button#addaddr").bind("click",AddAccidentAddressList);

    $("#accidentstartdate").datepicker($.datepicker.regional['ru']);
    $("#accidentenddate").datepicker($.datepicker.regional['ru']);

    $("#runsearch").bind("click",RunSearch);
    $("#clearsearch").bind("click",ClearSearch);

    // Вызов формы списка ДРП
    $("tr td a[drp=yes]").bind("click",ListDRP);


    //$('table[group=accidents]').tableScroll({height:800});


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





// Выделение строки
function ClickEventRow(e) {

        $("table[group=accidents] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=accidents] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#editrow").show();

}





// Поиск
function RunSearch(e) {

    var search = $("#search").val();
    var jqxhr = $.getJSON("/monitor/events/jsondata?searchaccident="+search,
        function(data) {
            window.location=$("#menuaccidents a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/monitor/events/jsondata?searchaccident="+search,
        function(data) {
            window.location=$("#menuaccidents a").attr("href");
        })
}








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







// Редактирование аварии
function EditAccident(e) {

    var row_id = $("table[group=accidents] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getaccidentdata2="+row_id,
        function(data) {

            $("#accidentstartdate").val(data['accstartdate']);
            $("#accidentstarttime").val(data['accstarttime']);
            $("#accidentenddate").val(data['accenddate']);
            $("#accidentendtime").val(data['accendtime']);
            $("#accidentcat").val(data['acccat']);
            $("#accidenttype").val(data['acctype']);
            $("#accidentname").val(data['accname']);
            $("#accidentcomment").val(data['acccomment']);
            $("#accidentreason").val(data['accreason']);
            $("#accidentrepair").val(data['accrepair']);
            $("#accidentaddress").val("");
            $("#address-accident-list").empty();
            $("#accidentaddresscomment").val(data['accaddrcomment']);


            // Авария завершена
            if (data["accend"] == "yes") { $("#accidentend").prop("checked",true); }
            else { $("#accidentend").prop("checked",false); }

            // Включение в статистику
            if (data["accstat"] == "yes") { $("#accidentstat").prop("checked",true); }
            else { $("#accidentstat").prop("checked",false); }


            $.each(data['address']['address_list'], function(index,value){

                var v = value;

                t = "<dt addressid=\'"+v['addressid']+"\'><a href=\"#\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></dt>"
                +"<dd addressid=\'"+v['addressid']+"\' addresslabel=\'"+v['addresslabel']+"\'>"
                + v['addresslabel']
                + "</dd>"

                $("#address-accident-list").prepend(t);
                $("#address-accident-list dt a").bind("click",DeleteAccidentAddressList);

            });



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




        })

    AccidentData(row_id);

}







function AccidentData(row_id) {



            $("#accidentdata").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                // Убираем календарь (не знаю как предотвратить открытие)
                $("#accidentstartdate").datepicker("hide");
                },
                title:"Авария",
                closeOnEscape: false,
                buttons:[{ text:"Сохранить",click: function() {
                    if ($('#accidenttype').valid() && $('#accidentcat').valid() && $('#accidentname').valid()) {

                        // Данные
                        var accstartdate = $("#accidentstartdate").val();
                        var accstarttime = $("#accidentstarttime").val();
                        var accenddate = $("#accidentenddate").val();
                        var accendtime = $("#accidentendtime").val();
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
                        data.accstartdate = accstartdate;
                        data.accstarttime = accstarttime;
                        data.accenddate = accenddate;
                        data.accendtime = accendtime;
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
                        data.acc_id = $("table[group=accidents] tbody tr[marked=yes]").attr("row_id");
                        data.action = "edit-accident2";


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
                        //$("table[group=events]").attr("refresh","yes");



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




// Вывод ДРП по аварии
function ListDRP(e) {

    var row_id = $("tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getdrplist="+row_id,
        function(data) {

            // Предварительная очистка списка
            $("#accident-drp-list").empty();

            $.each(data['mess_list'], function(index,value){

                var v = value;

                t = "<dt>"+v["author"]+"<br># "+v["num_drp"]+" ("+v["datetime"]+")<br></dt>"
                +"<dd>"
                + v["message"] +"<br>"
                + "</dd>"

                $("#accident-drp-list").prepend(t);

            });

            // Предварительная очистка списка
            $("#accident-drp-files").empty();

            $.each(data['file_list'], function(index,value){

                var v = value;

                t = "<dt>"+v["author"]+"<br>"+v["datetime"]+"<br></dt>"
                +"<dd>"
                + "<a target='_blank' href='monitor/accident/filedata?id="+v["id"]+"'>"+v["filename"] + "</a><br>"
                + "</dd>"

                $("#accident-drp-files").prepend(t);

            });



            $("#drplist").dialog({
                open:function() {
                },
                  title:"ДРП " + data["accident_name"],
                closeOnEscape: false,
                  show: {
                    effect: "blind",
                    duration: 100
                  },
                  hide: {
                    effect: "blind",
                    duration: 100
                  },
                  buttons: [{text:"Закрыть", click: function() { $(this).dialog("close");  }}],
                  modal:true,
                  minWidth:400,
                  width:600,
                  height:400

            });
    })


}

