$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // маска ввода
    $("form#reestr-proj-edit #id_proj_kod").mask("99/9999999/99999999/99", {placeholder:" "});

    // Виджет для даты
    $("dl dd #id_date_service").datepicker($.datepicker.regional['ru']);
    $("div#exec-window input#id_date1").datepicker($.datepicker.regional['ru']);
    $("div#exec-window input#id_date2").datepicker($.datepicker.regional['ru']);

    // Список загруженных файлов
    GetListHdfsFiles();
    // Список коментариев
    GetListComments();
    // Список логов
    GetListLogs();
    // Список истории стадий
    GetListStages();
    // Список исполнителей и дат
    GetListTasks();
    // Отображение excel таблицы
    GetTableExcel();
    // Отображение ссылок
    GetListLinks();
    // Отображение адресного перечня
    GetListAddress();
    // Отображение списка дочерних проектов
    GetListChildren();
    // Отображение списка связи с другими системами
    GetListOtherSystems();
    // Отображение истории оповещений
    GetListMessageHistory();


    // Перевод в реестр
    $("button#btn-reestr").bind("click", ToReestr);


    // Удаление загруженного в hdfs файла
    $("#page-4 table[group=file-list] tbody").on("click", "a[delete-file]", DeleteHDFSFile);

    // Удаление загруженного в hdfs файла
    $("#page-4 table[group=file-list] tbody").on("click", "input[type=checkbox]", DocProjChecked);


    // Удаление элемента исполнители и задачи
    $("#page-5 table[group=exec-list] tbody").on("click", "a[delete-task]", DeleteTask);

    // Удаление ссылки
    $("#page-1 table[group=links] tbody").on("click", "a[delete-link]", DeleteLink);

    // Удаление элемента адресного перечня
    $("#page-1 table[group=addresses] tbody").on("click", "a[delete-address]", DeleteAddress);

    // Удаление элемента связи с другими системами
    $("#page-1 table[group=systems] tbody").on("click", "a[delete-system]", DeleteOtherSystem);


    // Вызов формы редактирования элемента исполнители и даты
    $("#page-5 table[group=exec-list] tbody").on("click", "a[task]", EditTask);

    // Добавление коментария
    $("div#page-6 button#addcomment").bind("click", AddComment);

    // Установка стадии реестра проекта
    $("div#page-3 button#addstage").bind("click", AddStage);

    // Создание задачи (исполнители и даты)
    $("#page-5 a[exec]").bind("click", CreateTask);

    // Добавление ссылки
    $("#page-1 #add-link").bind("click", AddLink);

    // Добавление адресного перечня
    $("#page-1 #add-address").bind("click", AddAddress);

    // Создание дочернего проекта
    $("#page-7 a#create-child-proj").bind("click", AddChildProj);

    // Добавление кода других систем
    $("#page-1 button#append-system-code").bind("click", AddOtherSystem);

    // Отправка оповещения
    $("#page-8 button#message-send").bind("click", MessageSend);




    // Поиск адреса
    $("input#address").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#page-1',
        position: 'top',
        select: function (event,ui) {
            $("input#address").val(ui.item.label);
            window.address_id = ui.item.value;
            window.address_label = ui.item.label;

            return false;
        },
        focus: function (event,ui) {
            $("input#address").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    })


    // Сохранение основных данных карточки проекта
    $("button#btn-saving").bind("click", ReestrProjDataSave);

    // окраска кода проекта
    ReColorCode();



    // Изменение кода связи с другими системами
    $("#proj-common input#id_proj_other").change(function() {

        if ($("#proj-common input#id_proj_other").val() == "") {

            $("projcode").children("span").eq(2).text("NONE");

        }
        else {

            $("projcode").children("span").eq(2).text("eisup"+$("#proj-common input#id_proj_other").val());

        }

    });


    // Изменение кода инициатора
    $("#proj-common select#id_proj_init").change(function() {
        var init = $("#proj-common select#id_proj_init").val();
        if (init == "") {
            $("projcode").children("span").eq(0).text(init);
        }
        else {
            // Определение префикса
            var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-init-pref&init_id="+init,
            function(data) {

                $("projcode").children("span").eq(0).text(data["pref"]);

            })

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






// Перевод проекта в реестр
function ToReestr() {

    if (confirm("Перемещение в реестр?")) {

        var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

        var jqxhr = $.getJSON("/regions/jsondata/?action=processproj-to-reestr&reestrproj_id="+reestrproj_id,
        function(data) {

            if (data["result"] == "ok") { alert("Проект перемещен в реестр!"); }

        })



    }

}





// раскраска кода проекта
function ReColorCode() {
    var code = $("projcode").text().split("/");

    $("projcode").html("<span>"+code[0]+"</span>/<span>"+code[1]+"</span>/<span>"+code[2]+"</span>/<span>"+code[3]+"</span>");
    $("projcode").children("span").eq(0).css("color","blue");
    $("projcode").children("span").eq(2).css("color","green");
    $("projcode").children("span").eq(3).css("color","red");

}






// Обработка отметки (или снятия) проверки загруженного документа
function DocProjChecked(e) {

    if($(this).is(":checked")) { var checked = 'yes'; }
    else { var checked = 'no'; }
    var file_id = $(this).parents("tr").attr("file_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-doc-check-file&file_id="+file_id+"&checked="+checked,
    function(data) {
        GetListLogs();
    })

}





// Сохранение основных данных карточки проекта
function ReestrProjDataSave(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    $("#saving h3").text("Сохранение выполнено");
    $("#saving").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});


    var data = {};
    data.reestrproj_id = reestrproj_id;
    data.proj_kod = $("#proj-common projcode").text();
    data.proj_init = $("#proj-common select#id_proj_init").val();
    data.other = $("#proj-common input#id_proj_other").val();
    data.name = $("#proj-common input#id_proj_name").val();
    data.comment = $("#proj-common textarea#id_comment").val();
    data.executor = $("#proj-common select#id_executor").val();
    data.business = $("#proj-common select#id_business").val();
    data.service = $("#proj-common input#id_date_service").val();
    data.contragent = $("#page-1 input#id_contragent").val();
    data.rates = $("#page-1 select#id_rates").val();
    data.passing = $("#page-1 select#id_passing").val();
    data.object_price = $("#proj-common input#id_object_price").val();
    data.smr_price = $("#proj-common input#id_smr_price").val();
    data.other_price = $("#proj-common input#id_other_price").val();
    data.region = $("#proj-common select#id_region").val();


    data.action = "reestrproj-common-save";



    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/regions/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                $("#saving").dialog("close");
                GetListLogs();

            }
        }

    });



}





// Добавление ссылки
function AddLink(e) {


    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    // ссылка
    var link_code = $("#page-1 #link-code").val();
    // Коментарий к ссылке
    var link_comment = $("#page-1 #link-comment").val();

    if (link_code != "" && link_comment != "") {


        var data = {};
        data.link = link_code
        data.comment = link_comment;
        data.reestrproj_id = reestrproj_id;

        data.action = "reestrproj-link-add";


        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });




        $.ajax({
          url: "/regions/jsondata/",
          type: "POST",
          dataType: 'json',
          data:$.toJSON(data),
            success: function(result) {
                if (result["result"] == "ok") {

                    $("#page-1 #link-code").val("");
                    $("#page-1 #link-comment").val("");
                    GetListLinks();
                    GetListLogs();
                }
            }

        });




    }



}





// Установка стадии реестра проекта
function AddStage(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var stage = $("div#page-3 select#stage").val();
    if (stage == "") { alert("Укажите коректное значение стадии!"); }
    else {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-stage-add&reestrproj_id="+reestrproj_id+"&stage="+stage,
        function(data) {

            if (data["result"] == "ok") { $("div#page-3 select#stage").val(""); GetListStages();}
            if (data["result"] == "error") { alert("Выбранная стадия уже установлена!"); }

        })

    }

}





// Добавление коментария
function AddComment(e) {

    // Коментарий
    var comment = $("div#page-6 textarea#comment").val();
    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");


    var data = {};
    data.comment = comment;
    data.reestrproj_id = reestrproj_id;

    data.action = "reestrproj-comment-add";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/regions/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                // Очистка поля ввода
                $("div#page-6 textarea#comment").val("");
                GetListComments();

            }
        }

    });

}



// Создание задачи (исполнители и даты)
function CreateTask(e) {

    // Очистка полей ввода
    $("#exec-window input#id_date1").val("");
    $("#exec-window input#id_date2").val("");
    $("#exec-window select#id_stage").val(null);
    $("#exec-window select#id_worker").val(null);

    TaskData(action="reestrproj-task-create");

}




// Редактирование задачи (исполнители и даты)
function EditTask(e) {

    var task_id = $(this).parents("tr").attr("row_id");
    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-task-edit&task-id="+task_id,
    function(data) {

        if (data["result"] == "ok") {

            $("#exec-window").empty();
            $("#exec-window").append(data["form"]);
            $("div#exec-window input#id_date1").datepicker($.datepicker.regional['ru']);
            $("div#exec-window input#id_date2").datepicker($.datepicker.regional['ru']);

        }
        $("#exec-window").attr("task-id",data["task-id"]);

    })


    TaskData(action="reestrproj-task-edit");

}






// Создание и редактирование задачи (исполнители и даты)
function TaskData(action) {



    $("#exec-window").dialog({
        title:"Элемент исполнитель и даты",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


                var data = {};
                data.date1 = $("#exec-window input#id_date1").val();
                data.date2 = $("#exec-window input#id_date2").val();
                data.stage = $("#exec-window select#id_stage").val();
                data.worker = $("#exec-window select#id_worker").val();
                data.block = $("#exec-window select#id_block").val();
                data.reestrproj_id = $("div#proj-common").attr("reestrproj_id");
                data.action = action;
                if (action == "reestrproj-task-edit") { data.task_id = $("#exec-window").attr("task-id"); }

                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { $("#exec-window").dialog('close'); GetListTasks(); GetListComments(); }
                    }

                });

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        open: function() {
        },
        modal:true,
        minWidth:100,
        width:300

    });


}








// Очистка поля ввода загружаемого файла
function ClearUploadP2() {

    $("form#uploadfile input#upload_file").val("");

}




// Очистка поля ввода загружаемого файла
function ClearUploadP4() {

    $("form#uploadfilehdfs input#fileuploadhdfs").val("");

}




// Удаление загруженного в hdfs файла
function DeleteHDFSFile(e) {

    var file_id = $(this).parents("tr").attr("file_id");
    var filename = $(this).parents("tr").attr("filename");
    var deletefile = confirm("Удаляем "+filename+" ?");

    if (deletefile) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-hdfs-delete-file&file_id="+file_id,
        function(data) {

            if (data["result"] == "ok") { GetListHdfsFiles(); GetListLogs(); }

        })

    }


}







// Удаление элемента исполнители и задачи
function DeleteTask(e) {

    var task_id = $(this).parents("tr").attr("row_id");
    var stage = $(this).parents("tr").children("td").eq(2).text();
    var deletetask = confirm("Удаляем "+stage+" ?");

    if (deletetask) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-task-delete&task_id="+task_id,
        function(data) {

            if (data["result"] == "ok") { GetListTasks(); GetListLogs(); }

        })

    }


}







// Удаление ссылки
function DeleteLink(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var comment = $(this).parents("tr").children("td").eq(1).text();
    var row_id = $(this).parents("tr").attr("row_id");

    var deletelink = confirm("Удаляем "+comment+" ?");

    if (deletelink) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-link-delete&row-id="+row_id+"&reestrproj_id="+reestrproj_id,
        function(data) {

            if (data["result"] == "ok") { GetListLinks(); GetListLogs(); }

        })

    }


}






// Удаление элемента адресного перечня
function DeleteAddress(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var row_id = $(this).parents("tr").attr("row_id");
    var city = $(this).parents("tr").children("td").eq(0).text();
    var street = $(this).parents("tr").children("td").eq(1).text();
    var house = $(this).parents("tr").children("td").eq(2).text();

    var deleteaddress = confirm("Удаляем "+city+" "+street+" "+house+" ?");

    if (deleteaddress) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-address-delete&row-id="+row_id+"&reestrproj_id="+reestrproj_id,
        function(data) {

            if (data["result"] == "ok") { GetListAddress(); GetListLogs();}

        })

    }


}






// Удаление элемента связи с другими системами
function DeleteOtherSystem(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var row_id = $(this).parents("tr").attr("row_id");
    var system = $(this).parents("tr").children("td").eq(0).text();
    var code = $(this).parents("tr").children("td").eq(1).text();

    var deletesystem = confirm("Удаляем "+system+" "+code+" ?");

    if (deletesystem) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-other-system-delete&row-id="+row_id+"&reestrproj_id="+reestrproj_id,
        function(data) {

            if (data["result"] == "ok") { GetListOtherSystems(); GetListLogs();}

        })

    }


}






// Добавление адреса (адресный перечень)
function AddAddress(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var address_id = window.address_id;

    if (address_id) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-address-add&address_id="+address_id+"&reestrproj_id="+reestrproj_id,
        function(data) {

            if (data["result"] == "ok") { $("#page-1 input#address").val(""); GetListAddress(); GetListLogs(); }

        })

    }

}




// Добавление связи с другой системой
function AddOtherSystem(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var other_system_name = $("#page-1 select#other-system").val();
    var other_system_code = $("#page-1 input#system-code").val();

        if (other_system_name != "" && other_system_code != "") {

            var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-other-system-add&system_id="+other_system_name+"&system_code="+other_system_code+"&reestrproj_id="+reestrproj_id,
            function(data) {

                if (data["result"] == "ok") {
                    $("#page-1 select#other-system").val("");
                    $("#page-1 input#system-code").val("");
                    GetListOtherSystems();
                    GetListLogs();
                }

            })


        }


}







// Отправка оповещения
function MessageSend(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");
    var message_type = $("#page-8 select#message-type").val();

        if (message_type != "") {

            var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-message-send&message_type="+message_type+"&reestrproj_id="+reestrproj_id,
            function(data) {

                if (data["result"] == "ok") {
                    $("#page-8 select#message-type").val("");
                    GetListMessageHistory();
                }

            })


        }


}







// Список загруженных в hdfs файлов
function GetListHdfsFiles() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-hdfs-files&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=file-list] tbody").empty();
            $.each(data["data"], function(key,value) {

                if (value["checked"] == 1) { var checked_tag = "<input type=\"checkbox\" checked />"; }
                else { var checked_tag = "<input type=\"checkbox\" />"; }

                var t = "<tr file_id=" + value["file_id"] +" "+ "filename="+value["filename"]+">"
                +"<td>"+value['date']+"</td>"
                +"<td><a href=\"/regions/reestrproj/readfile?file_id="+value["file_id"]+"&file_name="+value["filename"]+"\" >"+value['filename']+"</a></td>"
                +"<td>"+value["filetype"]+"</td>"
                +"<td>"+checked_tag+"</td>"
                +"<td>"+value['user']+"</td>"
                +"<td><a delete-file><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=file-list] tbody").append(t);

            });



        }

    })


}





// Список коментраиев
function GetListComments() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-comments&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=comment-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr>"
                +"<td>"+value['date']+"</td>"
                +"<td>"+value['comment']+"</td>"
                +"<td>"+value['user']+"</td>"
                +"</tr>";

                $("table[group=comment-list] tbody").append(t);

            });



        }

    })


}






// Список логов
function GetListLogs() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-logs&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=log-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr>"
                +"<td>"+value['date']+"</td>"
                +"<td>"+value['comment']+"</td>"
                +"<td>"+value['user']+"</td>"
                +"</tr>";

                $("table[group=log-list] tbody").append(t);

            });



        }

    })


}






// Список истории стадий
function GetListStages() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-stages&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=stages-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr>"
                +"<td>"+value['date']+"</td>"
                +"<td>"+value['stage']+"</td>"
                +"<td>"+value['user']+"</td>"
                +"</tr>";

                $("table[group=stages-list] tbody").append(t);

            });



        }

    })


}







// Список исполнителей и дат
function GetListTasks() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-tasks&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=exec-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr row_id="+value['id']+">"
                +"<td><a task>"+value['date1']+"</a></td>"
                +"<td><a task>"+value['date2']+"</a></td>"
                +"<td><a task>"+value['stage']+"</a></td>"
                +"<td><a task>"+value['worker']+"</a></td>"
                +"<td><a task>"+value["block"]+"</a></td>"
                +"<td><a task>"+value['user']+"</a></td>"
                +"<td><a task>"+value['date3']+"</a></td>"
                +"<td><a delete-task><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=exec-list] tbody").append(t);

            });



        }

    })


}





// Список ссылок
function GetListLinks() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-links&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=links] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr row_id="+value['id']+" >"
                +"<td><a href="+value['link']+" target=\"_blank\" >Ссылка</a></td>"
                +"<td>"+value['comment']+"</td>"
                +"<td><a delete-link><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=links] tbody").append(t);

            });


        }

    })


}





// Адресный перечень
function GetListAddress() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-address&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=addresses] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr row_id="+value['address_id']+" >"
                +"<td>"+value['city']+"</td>"
                +"<td>"+value['street']+"</td>"
                +"<td>"+value['house']+"</td>"
                +"<td><a delete-address><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=addresses] tbody").append(t);

            });


        }

    })


}






// Список связи с другими системами
function GetListOtherSystems() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-other-system-list&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {
            // Отображение списка связи с другими системами
            $("table[group=systems] tbody").empty();
            $.each(data["system"], function(key,value) {


                var t = "<tr row_id="+value['id']+" >"
                +"<td>"+value['other_name']+"</td>"
                +"<td>"+value['other_code']+"</td>"
                +"<td><a delete-system><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=systems] tbody").append(t);

            });


        }

    })


}







// Список отправленных оповещений
function GetListMessageHistory() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-message-list&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {
            // Отображение списка связи с другими системами
            $("table[group=messages-list] tbody").empty();
            $.each(data["messages"], function(key,value) {


                var t = "<tr>"
                +"<td>"+value['date']+"</td>"
                +"<td>"+value['message_type']+"</td>"
                +"<td>"+value['emails']+"</td>"
                +"<td>"+value['user']+"</td>"
                +"</tr>";

                $("table[group=messages-list] tbody").append(t);

            });


        }

    })


}







// Отображение загруженной таблицы excel
function GetTableExcel() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-table-excel&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение excel таблицы
            $("#exceltable").empty();
            $("#exceltable").append(data["table"]);
            $("table.dataframe tbody tr td").css("padding","1px").css("background-color","sandybrown");
        }

    })


}







// Список дочерних проектов
function GetListChildren() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-list-children&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка дочерних проектов
            $("table[group=child-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr row_id="+value['id']+">"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value['kod']+"</a></td>"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value['level']+"</a></td>"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value['stage']+"</a></td>"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value['name']+"</a></td>"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value["create"]+"</a></td>"
                +"<td><a child target=\"_blank\" href=\"/regions/reestrproj/edit/"+value["id"]+"/\">"+value['author']+"</a></td>"
                +"</tr>";

                $("table[group=child-list] tbody").append(t);

            });



        }

    })


}








// Создание дочернего проекта
function AddChildProj(e) {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-child-level&reestrproj_id="+reestrproj_id,
    function(data2) {

        $("form#reestr-proj-add2 #id_proj_name").val($("#proj-common input#id_proj_name").val()+" ("+data2["level"]+")");


        $("#reestr-proj-new2").dialog({
            title:"Новый дочерний элемент",
            buttons:[{ text:"Сохранить",click: function() {

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });



                    // Проверка значений
                    if ( $("form#reestr-proj-add2 #id_proj_name").val() != "" ) {

                        var data = {};
                        data.name = $("form#reestr-proj-add2 #id_proj_name").val();
                        data.level = data2["level"];
                        data.reestrproj_id = reestrproj_id;
                        data.action = "reestrproj-create-child";


                        $.ajax({
                          url: "/regions/jsondata/",
                          type: "POST",
                          dataType: 'json',
                          data:$.toJSON(data),
                            success: function(result) {
                                if (result["result"] == "ok") { $("#reestr-proj-new2").dialog('close'); GetListChildren(); GetListComments();}
                            }

                        });


                    }
                    else { alert("Заполните поля!"); }


            }},


                {text:"Закрыть",click: function() {
                $(this).dialog("close")}}
            ],
            open: function() {
            },
            modal:true,
            minWidth:400,
            width:600

        });




    })



}
















// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);
    $("#nav-5").toggleClass("active",false);
    $("#nav-6").toggleClass("active",false);
    $("#nav-7").toggleClass("active",false);
    $("#nav-8").toggleClass("active",false);
    $("#nav-9").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();
    $("#page-5").hide();
    $("#page-6").hide();
    $("#page-7").hide();
    $("#page-8").hide();
    $("#page-9").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

