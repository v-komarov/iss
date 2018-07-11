$(document).ready(function() {


    // фильтры / поиск по городу улице дому названию компании
    $( "button#search-button" ).bind('click', SearchAddress);
    $( "button#clear-button" ).bind('click', SearchClear);

    // Создание дома
    $("a#addbuilding").bind("click",CreateHouse);



    // Поиск адреса
    $("input#id_address2").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#create-house',
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
        appendTo: '#create-house',
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







// Создание дома
function CreateHouse() {

    $("input#id_www_id").val("");
    $("input#id_numstoreys").val("");
    $("input#id_numentrances").val("");
    $("input#id_numfloars").val("");
    $("input#id_access").val("");
    $("input#id_address2").attr("address_id",0);
    $("input#id_manager").attr("manager_id",0);
    $("input#id_address2").val("");
    $("input#id_manager").val("");



    $("#create-house").dialog({
        title:"Создание дома",
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
                data.id_www = $("input#id_www_id").val();
                data.numstoreys = $("input#id_numstoreys").val();
                data.numentrances = $("input#id_numentrances").val();
                data.numfloars = $("input#id_numfloars").val();
                data.access = $("input#id_access").val();
                data.address = $("input#id_address2").attr("address_id");
                data.manager = $("input#id_manager").attr("manager_id");
                data.action = "house-common-create";



                if (data.id_www !="" && data.numstoreys != "" && data.numentrances != "" && data.numfloars != "" && data.access != "" && data.address != "" && data.manager != "") {

                    $.ajax({
                      url: "/blocks/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#create-house").dialog('close'); window.open("/blocks/houseedit/"+result["id"]+"/"); }
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
        width:550

    });


}










// Поиск по городу улице дому компании
function SearchAddress(e) {

        var city = $("select#search-city").val();
        var street = $("input#search-street").val();
        var house = $("input#search-house").val();
        var company = $("input#search-company").val();

        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-company&city="+city+"&street="+street+"&house="+house+"&company="+company,
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/houselist/1/";

            }

        })


}





// Очистка поиска по городу улице дому
function SearchClear(e) {


        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-company-clear",
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/houselist/1/";

            }

        })


}





