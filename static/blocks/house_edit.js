$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Переход к данным устройства
    $("div#page-2 a[devices]").bind("click",DeviceData);

    // Сохранение карточки дома
    $("button#button-save").bind("click", HouseDataSave);

    // Сохранение коментария
    $("div#page-1 button#addcomment").bind("click",AddComment);


    // Отображение логов
    GetListLogs();


    // Поиск адреса
    $("input#id_address2").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '',
        position: 'top',
        select: function (event,ui) {
            $("input#id_address2").val(ui.item.label);
            $("input#id_address2").attr("address_id",ui.item.value);

            return false;
        },
        focus: function (event,ui) {
            $("input#id_address2").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    });




    // Поиск компании
    $("input#id_manager").autocomplete({
        source: "/blocks/jsondata",
        minLength: 3,
        delay: 1000,
        appendTo: '',
        position: 'top',
        select: function (event,ui) {
            $("input#id_manager").val(ui.item.label);
            $("input#id_manager").attr("manager_id",ui.item.value);

            return false;
        },
        focus: function (event,ui) {
            $("input#id_manager").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
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








// Добавление коментария
function AddComment(e) {


    // Коментарий
    var comment = $("div#page-1 textarea#comment").val();
    var house_id = $("div#common").attr("house_id");


    var data = {};
    data.comment = comment;
    data.house = house_id;

    data.action = "house-comment-add";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/blocks/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                // Очистка поля ввода
                $("div#page-1 textarea#comment").val("");
                GetListComments();

            }
        }

    });

}















// Сохранение основных данных карточки дома
function HouseDataSave(e) {

    var house_id = $("div#common").attr("house_id");

    $("#saving h3").text("Сохранение выполнено");
    $("#saving").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});


    var data = {};
    data.house = house_id;
    data.numstoreys = $("input#id_numstoreys").val();
    data.numentrances = $("input#id_numentrances").val();
    data.numfloars = $("input#id_numfloars").val();
    data.access = $("input#id_access").val();
    data.address = $("input#id_address2").attr("address_id");
    data.manager = $("input#id_manager").attr("manager_id");


    data.action = "house-common-save";

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/blocks/jsondata/",
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






// Список логов
function GetListLogs() {

    var house_id = $("div#common").attr("house_id");

    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-house-list-logs&house="+house_id,
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






// Список коментраиев
function GetListComments() {

    var house_id = $("div#common").attr("house_id");

    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-house-list-comments&house="+house_id,
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








// Переход к интерфейсу устройства
function DeviceData(e) {

    var device_id = $(this).attr("device_id");
    var jqxhr = $.getJSON("/inventory/jsondata?dev_id="+device_id+"&action=savedevid",
    function(data) {
        if (data["result"] == "ok")

        win = window.open("/inventory/devicedata/","device");

    });


}





// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

