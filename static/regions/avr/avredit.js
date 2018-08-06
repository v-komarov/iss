$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Виджет для даты
    $("input#id_datetime_avr").datepicker($.datepicker.regional['ru']);
    $("input#id_datetime_work").datepicker($.datepicker.regional['ru']);

    // Сохранение карточки АВР
    $("button#avr-save").bind("click", EditAVR);

    // Добавление комментария
    $("#page-4 button#addcomment").bind("click", AddComment);

    // Удаление файла
    $("#page-3 table[group=file-list] tbody").on("click", "a[delete-file]", DeleteFile);

    // Удаление материала
    $("#page-1 table[group=stuff-list] tbody").on("click", "a[delete-stuff]", DeleteStuff);


    // Добавление материалов
    $("button#addstuff").bind("click", StuffUpload);


    // Отображение списко логов
    GetListLogs();
    // Отображение списка комментариев
    GetListComments();
    // Отображение списка загруженных файлов
    GetListFiles();
    // Отображение списка материалов
    GetListStuff();

    // загрузка возможных статусов
    GetAllowStatus();

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







// Добавление материалов из списка по МОЛ
function StuffUpload() {


    // Идентификатор МОЛ-а
    var staff_id = $("select#id_staff").val();

    // Идентификатор АВР
    var avr_id = $("input#id_avr_id").val();


    // Отрисовка таблицы с остатками по МОЛ-у
    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-get-staff-rest&staff_id="+staff_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=upload-list] tbody").empty();
            $.each(data["rest-list"], function(key,value) {


                var t = "<tr stuff_id="+ value["id"]+" >"
                +"<td>"+value['eisup']+"</td>"
                +"<td>"+value['accounting_code']+"</td>"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['rest']+"</td>"
                +"<td>"+value['dim']+"</td>"
                +"<td><input class=\"input-xs class10\" value=0 type=\"text\"></td>"
                +"<td>"+value['store']+"</td>"
                +"</tr>";

                $("table[group=upload-list] tbody").append(t);

            });



        }

    })





    $("#upload-stuff").dialog({
        title:"Добавление материалов",
        buttons:[{ text:"Применить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            // Выборка данных с ненулевыми значениями по количеству
            var data_tr = [];
            $.each($("table[group=upload-list] tr").slice(1), function(key, value) {

                if ($(value).find("input").val() != 0) {

                    var data_item = {};
                    data_item.stuff_id = $(value).attr("stuff_id");
                    data_item.rest = $(value).find("input").val();
                    data_tr.push(data_item);

                }
            });



            var data = {};
            data.rest = data_tr;
            data.avr_id = avr_id;
            data.action = "avr-upload-stuff";





            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {

                        $("#upload-stuff").dialog("close");
                        GetListLogs();
                        GetListStuff();

                    }
                }

            });


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:800,
        height:400
    });



}











// Список возможных статусов
function GetAllowStatus() {

    var status_id = $("input#id_status").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-get-status-list&status_id="+status_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("select#status").empty();
            $.each(data["status-list"], function(key,value) {

                $('select#status').append($('<option>', { value : value["id"] }).text(value["name"]));

            });

            // Доступ к номенклатуре
            $("input#id_stuff_allow").val(data["stuff"]);

            // Доступ к установке цен
            $("input#id_price_allow").val(data["price"]);

        }

    })

}




// Проверка разрешений
function CheckAllow() {



}







// Список материалов
function GetListStuff() {

    var avr_id = $("input#id_avr_id").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-stuff&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=stuff-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr stuff_id="+value["row_id"]+">"
                +"<td>"+value['eisup']+"</td>"
                +"<td>"+value['accounting_code']+"</td>"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['q']+"</td>"
                +"<td>"+value['dimension']+"</td>"
                +"<td>"+value['price']+"</td>"
                +"<td>"+value['store']+"</td>"
                +"<td><a delete-stuff><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=stuff-list] tbody").append(t);

            });



        }

    })


}









// Список логов
function GetListLogs() {

    var avr_id = $("input#id_avr_id").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-logs&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
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






// Список коментраиев
function GetListComments() {

     var avr_id = $("input#id_avr_id").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-comments&avr_id="+avr_id,
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





// Список файлов, загруженных в hdfs
function GetListFiles() {

    var avr_id = $("input#id_avr_id").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-hdfs-files&avr_id="+avr_id,
    function(data) {


        if (data["result"] == "ok") {

            $("table[group=file-list] tbody").empty();
            $.each(data["files"], function(key,value) {


                var t = "<tr file_id="+value["file_id"]+" >"
                +"<td>"+value['date']+"</td>"
                +"<td><a href=\"/regions/readfileavr?file_id="+value["file_id"]+"&file_name="+value["filename"]+"\" >"+value['filename']+"</a></td>"
                +"<td>"+value['user']+"</td>"
                +"<td><a delete-file><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=file-list] tbody").append(t);

            });



        }

    })


}







// Добавление коментария
function AddComment(e) {


    // Коментарий
    var comment = $("div#page-4 textarea#comment").val();
    var avr_id = $("input#id_avr_id").val();


    var data = {};
    data.comment = comment;
    data.avr_id = avr_id;

    data.action = "avr-comment-add";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    if (data.comment != "") {

        $.ajax({
          url: "/regions/jsondata/",
          type: "POST",
          dataType: 'json',
          data:$.toJSON(data),
            success: function(result) {
                if (result["result"] == "ok") {

                    // Очистка поля ввода
                    $("div#page-4 textarea#comment").val("");
                    GetListComments();

                }
            }

        });


    }

}









// Редактирование АВР
function EditAVR(e) {


    $("#saving h3").text("Сохранение выполнено");
    $("#saving").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var avr_id = $("input#id_avr_id").val();
    var region = $("select#id_region").val();
    var city = $("select#id_city").val();
    var objnet = $("input#id_objnet").val();
    var address = $("input#id_address").val();
    var datetime_avr = $("input#id_datetime_avr").val();
    var datetime_work = $("input#id_datetime_work").val();
    var staff = $("select#id_staff").val();


    if (region != "" && city != "" && objnet != "" && address != "" && datetime_avr != "" && staff != "") {

        var data = {};
        data.avr_id = avr_id
        data.region = region;
        data.city = city;
        data.address = address;
        data.objnet = objnet;
        data.datetime_avr = datetime_avr;
        data.datetime_work = datetime_work;
        data.staff = staff;
        data.action = "avr-save";



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
    else { alert("Необходимо заполнить поля!");}


}



// Очистка поля ввода имени файла
function ClearUploadFile() {

    $("#page-3 input#fileuploadhdfs").val("");

}








// Удаление загруженного файла
function DeleteFile(e) {

    var file_id = $(this).parents("tr").attr("file_id");
    var filename = $(this).parents("tr").children("td").eq(1).text();
    var deletefile = confirm("Удаляем файл "+filename+" ?");
    var avr_id = $("input#id_avr_id").val();

    if (deletefile) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=avr-file-delete&file_id="+file_id+"&avr_id="+avr_id,
        function(data) {

            if (data["result"] == "ok") { GetListFiles(); GetListLogs(); }

        })

    }


}






// Удаление материала
function DeleteStuff(e) {

    var stuff_id = $(this).parents("tr").attr("stuff_id");
    var stuffname = $(this).parents("tr").children("td").eq(2).text();
    var deletestuff = confirm("Удаляем "+stuffname+" ?");
    var avr_id = $("input#id_avr_id").val();


    if (deletestuff) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=avr-delete-stuff&stuff_id="+stuff_id+"&avr_id="+avr_id,
        function(data) {

            if (data["result"] == "ok") {

                GetListLogs();
                GetListStuff();
            }

        })

    }


}







// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);
    $("#nav-5").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();
    $("#page-5").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

