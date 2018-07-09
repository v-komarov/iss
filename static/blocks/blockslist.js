$(document).ready(function() {


    // фильтры / поиск по городу улице дому названию компании
    $( "button#search-button" ).bind('click', SearchAddress);
    $( "button#clear-button" ).bind('click', SearchClear);

    // Создание компании
    $("a#addmanager").bind("click", CreateCompany);

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







// Создание компании
function CreateCompany() {

    $("input#id_id_www").val("");
    $("input#id_name").val("");
    $("input#id_inn").val("");
    $("input#id_phone").val("");
    $("input#id_email").val("");
    $("textarea#id_contact").val("");
    $("input#id_address2").attr("address_id",0);
    $("input#id_address_law2").attr("address_id",0);
    $("input#id_address2").val("");
    $("input#id_address_law2").val("");


    $("#create-company").dialog({
        title:"Создание компании",
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
            data.id_www = $("input#id_id_www").val();
            data.name = $("input#id_name").val();
            data.inn = $("input#id_inn").val();
            data.phone = $("input#id_phone").val();
            data.email = $("input#id_email").val();
            data.contact = $("textarea#id_contact").val();
            data.address = $("input#id_address2").attr("address_id");
            data.address_law = $("input#id_address_law2").attr("address_id");


                data.action == "company-common-create";

                if (false) {

                    $.ajax({
                      url: "/blocks/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#create-house").dialog('close');}
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

                location.href="/blocks/blocklist/1/";

            }

        })


}





// Очистка поиска по городу улице дому
function SearchClear(e) {


        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-company-clear",
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/blocklist/1/";

            }

        })


}





