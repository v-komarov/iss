$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Сохранение карточки компании
    $("button#button-save").bind("click",CompanyDataSave);

    // Сохранение коментария
    $("div#page-3 button#addcomment").bind("click",AddComment);

    // Отображение таблицы логов
    GetListLogs();
    // Отображение списка коментариев
    GetListComments();



    // Поиск фактического адреса
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




    // Поиск юридического адреса
    $("input#id_address_law2").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '',
        position: 'top',
        select: function (event,ui) {
            $("input#id_address_law2").val(ui.item.label);
            $("input#id_address_law2").attr("address_id",ui.item.value);

            return false;
        },
        focus: function (event,ui) {
            $("input#id_address_law2").val(ui.item.label);
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





// Сохранение основных данных карточки компании
function CompanyDataSave(e) {

    var company_id = $("div#common").attr("company_id");

    $("#saving h3").text("Сохранение выполнено");
    $("#saving").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});


    var data = {};
    data.company_id = company_id;
    data.name = $("input#id_name").val();
    data.inn = $("input#id_inn").val();
    data.phone = $("input#id_phone").val();
    data.email = $("input#id_email").val();
    data.contact = $("textarea#id_contact").val();
    data.address = $("input#id_address2").attr("address_id");
    data.address_law = $("input#id_address_law2").attr("address_id");


    data.action = "company-common-save";



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







// Добавление коментария
function AddComment(e) {


    // Коментарий
    var comment = $("div#page-3 textarea#comment").val();
    var company_id = $("div#common").attr("company_id");


    var data = {};
    data.comment = comment;
    data.company = company_id;

    data.action = "company-comment-add";


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
                $("div#page-3 textarea#comment").val("");
                GetListComments();

            }
        }

    });

}







// Список логов
function GetListLogs() {

    var company_id = $("div#common").attr("company_id");

    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-company-list-logs&company="+company_id,
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

    var company_id = $("div#common").attr("company_id");

    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-company-list-comments&company="+company_id,
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







// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

