$(document).ready(function() {

    $("div#buttons button#search-button").bind("click", Search);
    $("div#buttons button#clear-button").bind("click", ClearSearch);
    $("button#create-button").bind("click", StoreCarry);





    // Поиск остатков на складе
    $("#carry_search").autocomplete({
        source: "/regions/jsondata/?filter=carry",
        minLength: 5,
        delay: 100,
        appendTo: '#store-carry',
        position: { my: "left bottom", at: "left bottom", collision: "flip" },
        select: function (event,ui) {
            $("#carry_search").val(ui.item.label);
            window.storerest_id = ui.item.value;
            window.storerest_label = ui.item.label;


            var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+ui.item.value,
            function(data) {
                if (data["result"] == "ok") {
                    $("input#carry_eisup").val(data["rec"]["eisup"]);
                    $("input#carry_out_store").val(data["rec"]["store"]);
                    $("input#carry_out_mol").val(data["rec"]["mol"]);
                    $("input#carry_q").val(data["rec"]["rest"]);
                }
            });


            return false;
        },
        focus: function (event,ui) {
            $("#carry_search").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        },
        open: function() {
            $("ul.ui-menu").width( $(this).innerWidth() );
            $("ul.ui-menu").css("margin-top","50px");
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






// Поиск / фильтр
function Search(e) {


    var search = $("input#search-text").val();
    var region = $("select#region").val();
    var store = $("select#store").val();
    var mol = $("select#mol").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-list-filter&search-text="+search+"&region="+region+"&store="+store+"&mol="+mol,
    function(data) {

        if (data["result"] == "ok") { location.href="/regions/storecarry/page/1/"; }

    })

}



// Отмена поиска /
function ClearSearch(e) {

    $("input#search-text").val("");
    $("select#region").val("");
    $("select#store").val("");
    $("select#mol").val("");

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-list-filter&search-text=&store=&region=&mol=",
    function(data) {

        if (data["result"] == "ok") { location.href="/regions/storecarry/page/1/"; }

    })


}







// Перемещение
function StoreCarry(e) {


    $("input#carry_eisup").val("");
    $("input#carry_search").val("");
    $("input#carry_out_store").val("");
    $("input#carry_out_mol").val("");
    $("input#carry_q").val("");
    $("select#carry_in_store").val("");
    $("input#carry_comment").val("");



    $("#store-carry").dialog({
        title:"Перемещение",
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
            data.id = window.storerest_id;
            data.q = $("input#in_q").val();
            data.comment =$("input#in_comment").val();
            data.store = $("select#carry_in_store").val();
            data.action = "store-carry";



            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {

                        $("#store-carry").dialog("close");
                        location.href="/regions/storecarry/page/1/";

                    }

                    else {
                        $("#notaccess").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});
                        $("#notaccess").dialog("close");
                    }
                }

            });


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:400
    });


}







