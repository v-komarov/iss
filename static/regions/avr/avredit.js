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

    // Установка статуса
    $("#page-2 button#setstatus").bind("click", SetStatus);

    // Удаление файла
    $("#page-3 table[group=file-list] tbody").on("click", "a[delete-file]", DeleteFile);

    // Удаление материала
    $("#page-1 table[group=stuff-list] tbody").on("click", "a[delete-stuff]", DeleteStuff);

    // Удаление ГСМ
    $("#page-5 table[group=gsm-list] tbody").on("click", "a[delete-gsm]", DeleteGSM);

    // Удаление трудозатрат
    $("#page-6 table[group=staff-list] tbody").on("click", "a[delete-staff]", DeleteStaff);



    // Добавление материалов
    $("button#addstuff").bind("click", StuffUpload);

    // Добавление материалов
    $("button#addgsm").bind("click", AddGSM);

    // Добавление трудозатрат
    $("button#addstaff").bind("click", AddWorker);


    // Установка цены материала
    $("#page-1 table").on("click", "a[save-price]", SetPrice);

    // Установка нормы ГСМ
    $("#page-5 table").on("click", "a[save-norma]", SetNorma);

    // Установка суммы ГСМ
    $("#page-5 table").on("click", "a[save-summa]", SetSumma);

    // Установка итоговой суммы по трудозатратам
    $("#page-6 table").on("click", "a[save-salary]", SetSalary);



    // Отображение списко логов
    GetListLogs();
    // Отображение списка комментариев
    GetListComments();
    // Отображение списка загруженных файлов
    GetListFiles();
    // Отображение списка материалов
    GetListStuff();
    // Отображение списка ГСМ
    GetListGSM();
    // Отображение списка трудозатрат
    GetListWorker();
    // загрузка возможных статусов
    GetAllowStatus();
    // Отображение истории статусов
    GetListStatus();

});









// Установка цены материалов
function SetPrice(e) {


    var stuff_id = $(this).parents("tr").attr("stuff_id");
    var input = $(this).parent("td").children("input").eq(0);


    // Установка цены материала
    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-stuff-price-set&stuff_id="+stuff_id+"&price="+input.val(),
    function(data) {

        if (data["result"] == "ok") {

            input.css("background-color","yellow");
            GetListLogs();

        }

    })


}





// Установка нормы расхода по ГСМ
function SetNorma(e) {


    var gsm_id = $(this).parents("tr").attr("gsm_id");
    var input = $(this).parent("td").children("input").eq(0);


    // Установка нормы расхода
    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-gsm-norma-set&gsm_id="+gsm_id+"&norma="+input.val(),
    function(data) {

        if (data["result"] == "ok") {

            input.css("background-color","yellow");
            GetListLogs();

        }

    })


}





// Установка суммы расхода по ГСМ
function SetSumma(e) {


    var gsm_id = $(this).parents("tr").attr("gsm_id");
    var input = $(this).parent("td").children("input").eq(0);


    // Установка суммы расхода
    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-gsm-summa-set&gsm_id="+gsm_id+"&summa="+input.val(),
    function(data) {

        if (data["result"] == "ok") {

            input.css("background-color","yellow");
            GetListLogs();

        }

    })


}





// Установка итоговой суммы по исполнителю
function SetSalary(e) {


    var staff_id = $(this).parents("tr").attr("staff_id");
    var input = $(this).parent("td").children("input").eq(0);


    // Установка суммы
    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-salary-summa-set&staff_id="+staff_id+"&summa="+input.val(),
    function(data) {

        if (data["result"] == "ok") {

            input.css("background-color","yellow");
            GetListLogs();

        }

    })


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










// Добавление GSM
function AddGSM() {


    // Идентификатор АВР
    var avr_id = $("input#id_avr_id").val();

    $("#gsm input#id_consumer").val("");
    $("#gsm input#id_km").val(0);
    $("#gsm input#id_h").val(0);
    $("#gsm input#id_kg").val(0);
    $("#gsm input#id_petrol").val(0);
    $("#gsm input#id_comment").val("");





    $("#gsm").dialog({
        title:"Добавление ГСМ",
        buttons:[{ text:"Добавить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            var consumer = $("#gsm input#id_consumer").val();
            var km = $("#gsm input#id_km").val();
            var h = $("#gsm input#id_h").val();
            var petrol = $("#gsm input#id_petrol").val();
            var kg = $("#gsm input#id_kg").val();
            var comment = $("#gsm input#id_comment").val();


            if ( consumer != "" && ((km > 0 && kg > 0) || h > 0) && petrol > 0 ) {

                var data = {};
                data.avr_id = avr_id;
                data.consumer = consumer;
                data.km = km;
                data.h = h;
                data.petrol = petrol;
                data.kg = kg;
                data.comment = comment;
                data.action = "avr-add-gsm";


                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") {

                            $("#gsm").dialog("close");
                            GetListLogs();
                            GetListGSM();

                        }
                    }

                });


            }

            else { alert("Необходимо заполнить поля!");}



        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:290
    });



}










// Добавление трудозатрат
function AddWorker() {


    // Идентификатор АВР
    var avr_id = $("input#id_avr_id").val();

    $("#worker select#id_staff").val("");
    $("#worker input#id_h").val(0);
    $("#worker input#id_h_day").val(0);
    $("#worker input#id_h_night").val(0);
    $("#worker input#id_comment").val("");





    $("#worker").dialog({
        title:"Добавление трудозатрат",
        buttons:[{ text:"Добавить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            var worker = $("#worker select#id_staff").val();
            var h = $("#worker input#id_h").val();
            var h_day = $("#worker input#id_h_day").val();
            var h_night = $("#worker input#id_h_night").val();
            var comment = $("#worker input#id_comment").val();


            if ( worker != "" && ( h > 0 || h_day > 0 || h_night > 0)) {

                var data = {};
                data.avr_id = avr_id;
                data.worker = worker;
                data.h = h;
                data.h_day = h_day;
                data.h_night = h_night;
                data.comment = comment;
                data.action = "avr-add-worker";


                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") {

                            $("#worker").dialog("close");
                            GetListLogs();
                            GetListWorker();

                        }
                    }

                });


            }

            else { alert("Необходимо заполнить поля!");}



        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:270
    });



}












// Список возможных статусов
function GetAllowStatus() {

    var status_id = $("input#id_status").val();


    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-get-status-list&status_id="+status_id,
    function(data) {


        if (data["result"] == "ok") {

            // Отображение списка
            $("#page-2 select#status").empty();
            $.each(data["status-list"], function(key,value) {

                $('#page-2 select#status').append($('<option>', { value : value["id"] }).text(value["name"]));

            });

            // Доступ к номенклатуре
            $("input#id_stuff_allow").val(data["stuff"]);

            // Доступ к установке цен
            $("input#id_price_allow").val(data["price"]);

            CheckEditing(data["stuff"], data["price"]);

        }

    })

}




// Проверка разрешений показывать некоторые кнопки и поля редактирования сумм
function CheckEditing(stuff,price) {

    if (stuff == "yes") {
        // Кнопка добавления материалов
        $("#page-1 form button#addstuff").show();

        // ГСМ
        // Кнопка добавления ГСМ
        $("#page-5 form button#addgsm").show();

        // Трудозатраты
        // Кнопка добавления трудозатрат
        $("#page-6 form button#addstaff").show();
    }
    else {
        // Кнопка добавления материалов
        $("#page-1 form button#addstuff").hide();

        // ГСМ
        // Кнопка добавления ГСМ
        $("#page-5 form button#addgsm").hide();

        // Трудозатраты
        // Кнопка добавления трудозатрат
        $("#page-6 form button#addstaff").hide();

    }



    // Освежить список материалов
    GetListStuff();
    // Освежить список затрат ГСМ
    GetListGSM();
    // Освежить список трудозатрат
    GetListWorker();




}







// Список материалов
function GetListStuff() {

    var avr_id = $("input#id_avr_id").val();

    var stuff_allow = $("input#id_stuff_allow").val();
    var price_allow = $("input#id_price_allow").val();


    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-stuff&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=stuff-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                // Ссылки удаления материала
                if (stuff_allow == "yes") {
                    delete_link = "<td><a delete-stuff><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>";
                }
                else { delete_link = "<td></td>"; }

                // Поля ввода цены
                if (price_allow == "yes") {
                    price_input =  "<td nowrap price-edit><input value="+value['price']+" /><a save-price><span class=\"glyphicon glyphicon-save\" aria-hidden=\"true\"></span></a></td>";

                }
                else {
                    price_input = "<td price-show>"+value['price']+"</td>";
                }


                var t = "<tr stuff_id="+value["row_id"]+">"
                +"<td>"+value['eisup']+"</td>"
                +"<td>"+value['accounting_code']+"</td>"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['q']+"</td>"
                +"<td>"+value['dimension']+"</td>"
                +price_input
                +"<td>"+value['store']+"</td>"
                +delete_link
                +"</tr>";

                $("table[group=stuff-list] tbody").append(t);

            });



        }

    })


}







// Список ГСМ
function GetListGSM() {

    var avr_id = $("input#id_avr_id").val();

    var stuff_allow = $("input#id_stuff_allow").val();
    var price_allow = $("input#id_price_allow").val();


    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-gsm&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=gsm-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                // Ссылки удаления ГСМ
                if (stuff_allow == "yes") {
                    delete_link = "<td><a delete-gsm><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>";
                }
                else { delete_link = "<td></td>"; }

                // Поля нормы и ссуммы
                if (price_allow == "yes") {
                    norma =  "<td nowrap gsm-norma><input value="+value['norma']+" /><a save-norma><span class=\"glyphicon glyphicon-save\" aria-hidden=\"true\"></span></a></td>";
                    summa =  "<td nowrap gsm-summa><input value="+value['summa']+" /><a save-summa><span class=\"glyphicon glyphicon-save\" aria-hidden=\"true\"></span></a></td>";

                }
                else {
                    norma = "<td>"+value['norma']+"</td>";
                    summa = "<td>"+value['summa']+"</td>";
                }




                var t = "<tr gsm_id="+value["row_id"]+">"
                +"<td>"+value['consumer']+"</td>"
                +"<td>"+value['km']+"</td>"
                +"<td>"+value['h']+"</td>"
                +"<td>"+value['petrol']+"</td>"
                +"<td>"+value['kg']+"</td>"
                +norma
                +summa
                +"<td>"+value['comment']+"</td>"
                +delete_link
                +"</tr>";

                $("table[group=gsm-list] tbody").append(t);

            });



        }

    })


}







// Список трудозатрат
function GetListWorker() {

    var avr_id = $("input#id_avr_id").val();

    var stuff_allow = $("input#id_stuff_allow").val();
    var price_allow = $("input#id_price_allow").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-worker&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=staff-list] tbody").empty();
            $.each(data["data"], function(key,value) {

                // Ссылки удаления Трудозатрат
                if (stuff_allow == "yes") {
                    delete_link = "<td><a delete-staff><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>";
                }
                else { delete_link = "<td></td>"; }

                // Поля ссуммы
                if (price_allow == "yes") {
                    summa =  "<td nowrap staff-summa><input value="+value['summa']+" /><a save-salary><span class=\"glyphicon glyphicon-save\" aria-hidden=\"true\"></span></a></td>";

                }
                else {
                    summa = "<td>"+value['summa']+"</td>";
                }



                var t = "<tr staff_id="+value["row_id"]+">"
                +"<td>"+value['worker']+"</td>"
                +"<td>"+value['h']+"</td>"
                +"<td>"+value['h_day']+"</td>"
                +"<td>"+value['h_night']+"</td>"
                +summa
                +"<td>"+value['comment']+"</td>"
                +delete_link
                +"</tr>";

                $("table[group=staff-list] tbody").append(t);

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




// История статусов
function GetListStatus() {

    var avr_id = $("input#id_avr_id").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-avr-list-status&avr_id="+avr_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка
            $("table[group=status-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr>"
                +"<td>"+value['date']+"</td>"
                +"<td>"+value['status']+"</td>"
                +"<td>"+value['user']+"</td>"
                +"</tr>";

                $("table[group=status-list] tbody").append(t);

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





// Установка статуса
function SetStatus(e) {


    var avr_id = $("input#id_avr_id").val();
    var status = $("#page-2 select#status").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=avr-set-status&avr_id="+avr_id+"&status_id="+status,
    function(data) {

        if (data["result"] == "ok") {

            $("input#id_status").val(status);
            GetAllowStatus();
            GetListStatus();
        }

    })


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






// Удаление ГСМ
function DeleteGSM(e) {

    var gsm_id = $(this).parents("tr").attr("gsm_id");
    var gsmname = $(this).parents("tr").children("td").eq(0).text();
    var deletegsm = confirm("Удаляем "+gsmname+" ?");
    var avr_id = $("input#id_avr_id").val();


    if (deletegsm) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=avr-delete-gsm&gsm_id="+gsm_id+"&avr_id="+avr_id,
        function(data) {

            if (data["result"] == "ok") {

                GetListLogs();
                GetListGSM();
            }

        })

    }


}






// Удаление Трудозатрат
function DeleteStaff(e) {

    var staff_id = $(this).parents("tr").attr("staff_id");
    var staffname = $(this).parents("tr").children("td").eq(0).text();
    var deletestaff = confirm("Удаляем "+staffname+" ?");
    var avr_id = $("input#id_avr_id").val();


    if (deletestaff) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=avr-delete-staff&staff_id="+staff_id+"&avr_id="+avr_id,
        function(data) {

            if (data["result"] == "ok") {

                GetListLogs();
                GetListWorker();
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
    $("#nav-6").toggleClass("active",false);
    $("#nav-7").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();
    $("#page-5").hide();
    $("#page-6").hide();
    $("#page-7").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

