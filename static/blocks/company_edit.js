$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Сохранение карточки компании
    $("button#button-save").bind("click",CompanyDataSave);

    // Сохранение коментария
    $("div#page-3 button#addcomment").bind("click",AddComment);

    // Создание договора
    $("div#page-1 a#addcontract").bind("click", CreateContract);

    // Редактирование договора
    $("#page-1 table[group=contract-list] tbody").on("click", "a[contract]", EditContract);

    // Удаление договора
    $("#page-1 table[group=contract-list] tbody").on("click", "a[delete-contract]", DeleteContract);


    // Виджет для даты
    $("div#contract-window input#id_date_begin").datepicker($.datepicker.regional['ru']);
    $("div#contract-window input#id_date_end").datepicker($.datepicker.regional['ru']);



    // Отображение таблицы логов
    GetListLogs();
    // Отображение списка коментариев
    GetListComments();
    // Отображение списка договоров
    GetListContracts()


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







// Создание договора
function CreateContract(e) {

    // Очистка полей ввода
    $("#contract-window input#id_num").val("");
    $("#contract-window input#id_date_begin").val("");
    $("#contract-window input#id_date_end").val("");
    $("#contract-window input#id_goon").prop("checked", false);
    $("#contract-window input#id_money").val("0");
    $("#contract-window select#id_period").val("");
    $("#contract-window select#id_manager").val("");

    ContractData(action="contract-create");

}




// Редактирование договора
function EditContract(e) {

    var contract_id = $(this).parents("tr").attr("contract_id");
    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-company-contract-one&contract-id="+contract_id,
    function(data) {

        if (data["result"] == "ok") {

            $("#contract-window input#id_num").val(data["rec"]["num"]);
            $("#contract-window input#id_date_begin").val(data["rec"]["date_begin"]);
            $("#contract-window input#id_date_end").val(data["rec"]["date_end"]);
            if (data["rec"]["goon"] == "yes") { $("#contract-window input#id_goon").prop("checked", true); } else { $("#contract-window input#id_goon").prop("checked", false); }
            $("#contract-window input#id_money").val(data["rec"]["money"]);
            $("#contract-window select#id_period").val(data["rec"]["period"]);
            $("#contract-window select#id_manager").val(data["rec"]["manager"]);

            $("#contract-window").attr("contract-id",data["rec"]["contract_id"]);

        }

    })


    ContractData(action="contract-edit");

}






// Создание и редактирование договора
function ContractData(action) {



    $("#contract-window").dialog({
        title:"Договор",
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
                data.num = $("#contract-window input#id_num").val();
                data.date_begin = $("#contract-window input#id_date_begin").val();
                data.date_end = $("#contract-window input#id_date_end").val();
                data.date_end = $("#contract-window input#id_date_end").val();
                if ($("#contract-window input#id_goon").is(':checked')) {data.goon = "yes";} else {data.goon = "no";}
                data.money = $("#contract-window input#id_money").val();
                data.period = $("#contract-window select#id_period").val();
                data.manager = $("#contract-window select#id_manager").val();
                data.company = $("div#common").attr("company_id");
                data.action = action;

                if (action == "contract-edit") { data.contract_id = $("#contract-window").attr("contract-id"); }

                if ( (data.num != "") && (data.date_begin != "") && (data.date_end != "") && (data.money != 0) && (data.period != "") && (data.manager != "")) {

                    $.ajax({
                      url: "/blocks/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#contract-window").dialog('close');  GetListContracts(); GetListLogs();}
                        }

                    });

                }
                else { alert("Необходимо заполнить все поля!");}


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        open: function() {
        },
        modal:true,
        minWidth:100,
        width:400

    });


}







// Удаление договора
function DeleteContract(e) {

    var contract_id = $(this).parents("tr").attr("contract_id");
    var contract = $(this).parents("tr").children("td").eq(0).text();
    var deletecontract = confirm("Удаляем договор "+contract+" ?");
    var company = $("div#common").attr("company_id");

    if (deletecontract) {

        var jqxhr = $.getJSON("/blocks/jsondata/?action=contract-delete&contract_id="+contract_id+"&company="+company,
        function(data) {

            if (data["result"] == "ok") { GetListContracts(); GetListLogs(); }

        })

    }


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





// Список договоров
function GetListContracts() {

    var company_id = $("div#common").attr("company_id");

    var jqxhr = $.getJSON("/blocks/jsondata/?action=get-company-list-contracts&company="+company_id,
    function(data) {

        if (data["result"] == "ok") {

            $("table[group=contract-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr contract_id="+value["contract_id"]+" >"
                +"<td><a contract>"+value['num']+"</a></td>"
                +"<td><a contract>"+value['date_begin']+"</a></td>"
                +"<td><a contract>"+value['date_end']+"</a></td>"
                +"<td><a contract>"+value['goon']+"</a></td>"
                +"<td><a contract>"+value['money']+"</a></td>"
                +"<td><a contract>"+value['period']+"</a></td>"
                +"<td><a contract>"+value['create']+"</a></td>"
                +"<td><a contract>"+value['manager']+"</a></td>"
                +"<td><a contract>"+value['author']+"</a></td>"
                +"<td><a delete-contract><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=contract-list] tbody").append(t);

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

