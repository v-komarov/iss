$(document).ready(function() {

    $("div#buttons button#search-button").bind("click", Search);
    $("div#buttons button#clear-button").bind("click", ClearSearch);
    $("button#create-button").bind("click", StoreOut);
    $("table[group=storeout-list] a").bind("click", StoreOutDel);






    // Поиск остатков на складе
    $("#out_search").autocomplete({
        source: "/regions/jsondata/?filter=user",
        minLength: 5,
        delay: 100,
        appendTo: '#store-out',
        position: { my: "left bottom", at: "left bottom", collision: "flip" },
        select: function (event,ui) {
            $("#out_search").val(ui.item.label);
            window.storerest_id = ui.item.value;
            window.storerest_label = ui.item.label;

            var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+ui.item.value,
            function(data) {
                if (data["result"] == "ok") {
                    $("input#out_serial").val(data["rec"]["serial"]);
                    $("input#out_q").val(data["rec"]["rest"]);
                    $("input#out_eisup").val(data["rec"]["eisup"]);
                    $("input#out_store").val(data["rec"]["store"]);
                }
            });


            return false;
        },
        focus: function (event,ui) {
            $("#out_search").val(ui.item.label);
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

        if (data["result"] == "ok") { location.href="/regions/storeout/page/1/"; }

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

        if (data["result"] == "ok") { location.href="/regions/storeout/page/1/"; }

    })


}







// Расход
function StoreOut(e) {


    $("input#out_search").val("");
    $("input#out_serial").val("");
    $("input#out_q").val("");
    $("input#out_eisup").val("");
    $("input#out_store").val("");
    $("input#out_proj_kod").val("");
    $("input#comment").val("");



    $("#store-out").dialog({
        title:"Расход со склада",
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
            data.q = $("input#out_q").val();
            data.comment = $("input#out_comment").val();
            data.proj = $("input#out_proj_kod").val();
            data.action = "store-out-q";



            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {

                        $("#store-out").dialog("close");
                        location.href="/regions/storeout/page/1/";
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




// Расход удаление
function StoreOutDel(e) {


    var row_id = $(this).parents("tr").attr("row_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-out-rec&row_id="+row_id,
    function(data) {


        $("input#out_name_del").val(data["rec"]["name"]);
        $("input#out_eisup_del").val(data["rec"]["eisup"]);
        $("input#out_store_del").val(data["rec"]["store"]);
        $("input#out_q_del").val(data["rec"]["q"]);
        $("input#out_proj_kod_del").val(data["rec"]["proj"]);
        $("input#out_serial_del").val(data["rec"]["serial"]);
        $("input#out_comment_del").val(data["rec"]["comment"]);


    })




    $("#store-out-del").dialog({
        title:"Расход со склада удаление",
        buttons:[{ text:"Удалить",click: function() {


            var jqxhr = $.getJSON("/regions/jsondata/?action=store-out-del&row_id="+row_id,
            function(data) {

                location.href="/regions/storeout/page/1/";

            })

        }},


            {text:"Отмена",click: function() {
                $(this).dialog("close") }}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:350
    });


}

