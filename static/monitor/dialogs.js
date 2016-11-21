$(document).ready(function() {



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
    /*var service = eval($("#service_stoplist").attr("selected_value"));
    service.forEach(function(item, i, arr) {
        $("#service_stoplist").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });*/
    // Список услуг конец




});






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
                title:"Почтовое сообщение",
                buttons:[
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close")}}
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
                title:"Почтовое сообщение",
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
                    $(this).dialog("close")}}
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
                title:"Изменение события",
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
                    $(this).dialog("close")}}
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
        title:"Создание события",
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
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:700

    });

}











// Оповещение об аварии на MCC
function MessageMssBegin(e) {

/*
    $("#maillist").empty();
    $("#maillist").append($("<option value=\"\" selected></option>"));
    $("#mailtext subj").text("");
    $("#mailtext mailtext").text("");
    $("#mailtext dl attachement").empty();

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
*/
/*    var jqxhr = $.getJSON("/monitor/events/jsondata?getevent="+row_id,
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

*/
            $("#message-mss-begin").dialog({
                title:"Оповещение об аварии на MCC",
                buttons:[{ text:"Отправить",click: function() {
                    /*
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

                    } */

                }},
                    {text:"Закрыть",click: function() {
                    $(this).dialog("close")}}
                ],
                modal:true,
                minWidth:600,
                width:900

            });







  //      })


}







