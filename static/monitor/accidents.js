$(document).ready(function() {

    $("table[group=accidents] tbody tr").bind("click",ClickEventRow);
    $("#editrow").hide(); // первоначально если строка не выделена, то кнопку редактирования прячем
    $("#editrow").bind("click",EditAccident);
    $("button#addaddr").bind("click",AddAccidentAddressList);

    $("#accidentstartdate").datepicker($.datepicker.regional['ru']);
    $("#accidentenddate").datepicker($.datepicker.regional['ru']);


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


            $("#accidentcat").val(data['acccat']);
            $("#accidenttype").val(data['acctype']);
            $("#accidentname").val(data['accname']);
            $("#accidentcomment").val(data['acccomment']);
            $("#accidentreason").val(data['accreason']);
            $("#accidentrepair").val(data['accrepair']);
            $("#accidentaddress").val("");
            $("#address-accident-list").empty();

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

                        address_arr = [];

                        $.each($("#address-accident-list dd"), function( index, value ) {
                            var row = {};
                            row.addressid = $(value).attr("addressid");
                            row.addresslabel = $(value).attr("addresslabel");
                            address_arr.push(row);
                        });

                        var data = {};
                        data.address_list = address_arr;
                        data.acccat = acccat;
                        data.acctype = acctype;
                        data.accname = accname;
                        data.acccomment = acccomment;
                        data.accend = accend;
                        data.accstat = accstat;
                        data.accreason = accreason;
                        data.accrepair = accrepair;
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


