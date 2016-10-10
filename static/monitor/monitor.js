$(document).ready(function() {

    $("#floatingCirclesG").attr("hidden","hidden");
    $("table[group=events]").removeAttr("hidden");


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("#uuid").bind("keyup",FindUuid);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);

    $("#clearfirstseen").bind("click",ClearFirstSeen);
    $("#clearlastseen").bind("click",ClearLastSeen);

    $("#runstatus").bind("click",FilterStatus);
    $("#runseverity").bind("click",FilterSeverity);
    $("#runmanager").bind("click",FilterManager);


    $("#showgroup").bind("click",ShowContainer);
    $("#hidegroup").bind("click",HideContainer);
    $("#addgroup").bind("click",AddContainer);
    $("#showmembers").bind("click",ShowMembers);
    $("#hidemembers").bind("click",HideMembers);
    $("#deletemembers").bind("click",DeleteMembers);
    $("#addrow").bind("click",AddRow);
    $("#editrow").bind("click",EditRow);
    $("#editmail").bind("click",EditMail);

    RowColor();


    // Фильтр статусов
    $("#filter-status").multiselect({
        header:true,
        noneSelectedText:"Выбор статусов",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#filter-status").multiselect("uncheckAll");
    var status = eval($("#filter-status").attr("selected_value"));
    status.forEach(function(item, i, arr) {
        $("#filter-status").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр статусов конец


    // Фильтр важности
    $("#filter-severity").multiselect({
        header:true,
        noneSelectedText:"Выбор важности",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#filter-severity").multiselect("uncheckAll");
    var severity = eval($("#filter-severity").attr("selected_value"));
    severity.forEach(function(item, i, arr) {
        $("#filter-severity").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр важности конец


    // Фильтр Менеджер
    $("#manager").multiselect({
        header:true,
        noneSelectedText:"Выбор источников",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#manager").multiselect("uncheckAll");
    var manager = eval($("#manager").attr("selected_value"));
    manager.forEach(function(item, i, arr) {
        $("#manager").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр Менеджер конец


     // Установка first_seen
     $( "#first_seen" ).bind("change paste keyup", function() {
        var first_seen = $("#first_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?first_seen="+first_seen,
            function(data) {
                window.location=$("#menumonitor a").attr("href");
            })
     });

     // Установка last_seen
     $( "#last_seen" ).bind("change paste keyup", function() {
        var last_seen = $("#last_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?last_seen="+last_seen,
            function(data) {
                window.location=$("#menumonitor a").attr("href");
            })
     });


    $('table[group=events] tbody tr td input[type=checkbox]').on("click",CheckBoxRow);

    $('table[group=events]').tableScroll({height:700});

    // Видимость кнопок
    $("#showgroup").hide();
    $("#editrow").hide();
    $("#editmail").hide();

    if ($("#hidegroup").is(":visible") == true) { $("#addgroup").show(); $("#addrow").hide(); $("#hidemembers").hide(); $("#deletemembers").hide();}
    else { $("#addgroup").hide(); $("#addrow").show(); }


    // Сброс строковых checkbox-ов
    $("table[group=events] tbody tr td input:checkbox").each(function(){
        $(this).prop( "checked", false );
    });






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







// Удаление выбранных элементов из контейнера
function DeleteMembers(e) {

    var id = [];
    var i = $("table[group=group] tbody tr[group=members] td input:checked");
    $.each( i, function( key, value ) {
        id.push("'"+$(value).closest("tr").attr("row_id")+"'");
    });

    var jqxhr = $.getJSON("/monitor/events/jsondata?delgroup=["+id+"]",
        function(data) {

            $("table[group=group] tbody tr[group=members] td input:checked").closest("tr").empty();
            $("info").text("Группировка "+$("table[group=group] tbody tr[group=members] td input").length+" элементов");
        })

}






// Свернуть группировку
function HideMembers(e) {

    $("table[group=group] tbody tr[group=members]").empty();
    $("#showmembers").show();
    $("#hidemembers").hide();
    $("#deletemembers").hide();
    $("#addgroup").show();

}






// Развернуть группировку
function ShowMembers(e) {
    var jqxhr = $.getJSON("/monitor/events/jsondata?getmembers=ok",
        function(data) {

            data['members'].forEach(function(item,i,arr){

                var icon = "";

                if (item["byhand"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-user\" aria-hidden=\"true\"></span>"; }
                if (item["agregator"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-align-justify\" aria-hidden=\"true\"></span>"; }
                if (item["bymail"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-envelope\" aria-hidden=\"true\"></span>"; }

                var t = "<tr group=members style=\"background-color:#C0C0C0;\" class=\"small\" row_id=\""+item["id"]+"\" marked=\"no\">"
                +"<td style=\"padding:0;\">"+icon+"</td>"
                +"<td style=\"padding:0;\"><input type=\"checkbox\" class=\"input\"></td>"
                +"<td style=\"padding:0;\"><a id=\"tooltip\" title='"+item['uuid']+"'>"+escape(item['uuid']).substr(0,4)+"...</a></td>"
                +"<td style=\"padding:0;\">"+item['first_seen']+"</td>"
                +"<td style=\"padding:0;\">"+item['last_seen']+"</td>"
                +"<td style=\"padding:0;\">"+item['status']+"</td>"
                +"<td style=\"padding:0;\">"+item['severity']+"</td>"
                +"<td style=\"padding:0;\">"+item['manager']+"</td>"
                +"<td style=\"padding:0;\">"+item['event_class']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_system']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_group']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_class']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_net_address']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_location']+"</td>"
                +"<td style=\"padding:0;\">"+item['element_identifier']+"</td>"
                +"<td style=\"padding:0;\">"+item['element_sub_identifier']+"</td>"
                +"</tr>";

                $("table[group=group] tbody").append(t);

            });

            $("#showmembers").hide();
            $("#hidemembers").show();
            $("#deletemembers").show();
            $("#addgroup").hide();

            $("table[group=group] tbody tr[group=members]").bind("click",ClickGroupRow);

        })
}






// Выделение строки содержания контейнера
function ClickGroupRow(e) {

        $("table[group=group] tbody tr[group=members]").css("background-color","#C0C0C0");
        $(this).css("background-color","#F0E68C");
        $("table[group=group] tbody tr[group=members]").attr("marked","no");
        $(this).attr("marked","yes");
}






// Добавление в группировку
function AddContainer(e) {

    var id = []
    var row_list = $("table[group=events] tbody tr[group=true]");
    $.each( row_list, function( key, value ) {
        id.push("'"+$(value).attr("row_id")+"'");
    });

    var jqxhr = $.getJSON("/monitor/events/jsondata?addgroup=["+id+"]",
        function(data) {
            window.location.reload();
        })

}








function ShowContainer(e) {
    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?containergroup="+row_id,
        function(data) {
            window.location.reload();
        })
}




function HideContainer(e) {

    var jqxhr = $.getJSON("/monitor/events/jsondata?containergroup=_____",
        function(data) {
            window.location.reload();
        })

}




function FilterStatus() {

    var message = $("#filter-status").multiselect("getChecked").map(function(){
       return this.value;
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?status=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}



function FilterSeverity() {

    var message = $("#filter-severity").multiselect("getChecked").map(function(){
       return this.value;
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?severity=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}



function FilterManager() {

    var message = $("#manager").multiselect("getChecked").map(function(){
       return "'"+this.value+"'";
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?manager=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}






function RowColor() {
    $("table[group=events] tbody tr[severity_id=0]").css("color","red");
    $("table[group=events] tbody tr[severity_id=1]").css("color","brown");
    $("table[group=events] tbody tr[severity_id=2]").css("color","#B8860B");
    $("table[group=events] tbody tr[severity_id=3]").css("color","#00008B");
    $("table[group=events] tbody tr[severity_id=4]").css("color","#006400");
}






// Выделение строки
function ClickEventRow(e) {

        $("table[group=events] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=events] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");
        if ($("#hidegroup").is(":visible") != true) {
            $("#showgroup").show();
        }
        if ($(this).attr("byhand") == "yes") { $("#editrow").show(); }
        else { $("#editrow").hide(); }
        if ($(this).attr("bymail") == "yes") { $("#editmail").show(); }
        else { $("#editmail").hide(); }

}



// фильтрация по uuid
function FindUuid(e) {

        if ( ($(this).val().length) != 0 ) {

            $("table[group=events] tbody tr").hide();
            $("table[group=events] tbody tr[uuid="+($(this).val())+"]").show();

        }

        else { $("table[group=events] tbody tr").show(); }

}






// Поиск
function RunSearch(e) {
    console.log("working");
    var search = $("#search").val();
    var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}



// Отмена FirstSeen
function ClearFirstSeen(e) {
    $("#first_seen").val("");
    $("#first_seen").attr("placeholder","");

    var value = "";
    var jqxhr = $.getJSON("/monitor/events/jsondata?first_seen="+value,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}




// Отмена FirstSeen
function ClearLastSeen(e) {
    $("#last_seen").val("");
    $("#last_seen").attr("placeholder","");

    var value = "";
    var jqxhr = $.getJSON("/monitor/events/jsondata?last_seen="+value,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}




// Строчные checkbox-ы
function CheckBoxRow(e) {
    //console.log($(this));
    if ($(this).prop('checked') == true) {
        $(this).closest("tr").attr("group",true);
        //console.log($(this).closest("tr").attr("group"));
    }
    else {
        $(this).closest("tr").attr("group",false);
        //console.log($(this).closest("tr").attr("group"));
    }
}

