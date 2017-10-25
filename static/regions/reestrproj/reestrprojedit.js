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
    // Список истории стадий
    GetListStages();
    // Список исполнителей и дат
    GetListTasks();
    // Отображение excel таблицы
    GetTableExcel();
    // Отображение ссылок
    GetListLinks();

    // Удаление загруженного в hdfs файла
    $("#page-4 table[group=file-list] tbody").on("click", "a[delete-file]", DeleteHDFSFile);

    // Удаление элемента исполнители и задачи
    $("#page-5 table[group=exec-list] tbody").on("click", "a[delete-task]", DeleteTask);

    // Удаление ссылки
    $("#page-1 table[group=links] tbody").on("click", "a[delete-link]", DeleteLink);


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






// Добавление ссылки
function AddLink(e) {


    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    // ссылка
    var link_code = $("#page-1 #link-code").val();
    // Коментарий к ссылке
    var link_comment = $("#page-1 #link-comment").val();

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
            }
        }

    });


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
                data.reestrproj_id = $("div#proj-common").attr("reestrproj_id");
                data.action = action;
                if (action == "reestrproj-task-edit") { data.task_id = $("#exec-window").attr("task-id"); }

                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { $("#exec-window").dialog('close'); GetListTasks(); }
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

            if (data["result"] == "ok") { GetListHdfsFiles(); }

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

            if (data["result"] == "ok") { GetListTasks(); }

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

            if (data["result"] == "ok") { GetListLinks(); }

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


                var t = "<tr file_id=" + value["file_id"] +" "+ "filename="+value["filename"]+">"
                +"<td>"+value['date']+"</td>"
                +"<td><a href=\"/regions/reestrproj/readfile?file_id="+value["file_id"]+"&file_name="+value["filename"]+"\" >"+value['filename']+"</a></td>"
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







// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);
    $("#nav-5").toggleClass("active",false);
    $("#nav-6").toggleClass("active",false);
    //$("#nav-7").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();
    $("#page-5").hide();
    $("#page-6").hide();
    //$("#page-7").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

