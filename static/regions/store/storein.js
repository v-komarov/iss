$(document).ready(function() {

    $("div#buttons button#search-button").bind("click", Search);
    $("div#buttons button#clear-button").bind("click", ClearSearch);
    $("button#create-button").bind("click", StoreIn);
    $("table[group=storein-list] a").bind("click", StoreInDel);





    // Поиск остатков на складе
    $("#in_search").autocomplete({
        source: "/regions/jsondata/?filter=all",
        minLength: 5,
        delay: 100,
        appendTo: '#store-in',
        position: { my: "left bottom", at: "left bottom", collision: "flip" },
        select: function (event,ui) {
            $("#in_search").val(ui.item.label);
            window.storerest_id = ui.item.value;
            window.storerest_label = ui.item.label;


            var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+ui.item.value,
            function(data) {
                if (data["result"] == "ok") {
                    $("input#in_eisup").val(data["rec"]["eisup"]);
                }
            });


            return false;
        },
        focus: function (event,ui) {
            $("#in_search").val(ui.item.label);
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

        if (data["result"] == "ok") { location.href="/regions/storein/page/1/"; }

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

        if (data["result"] == "ok") { location.href="/regions/storein/page/1/"; }

    })


}







// Поступление
function StoreIn(e) {


    $("input#in_search").val("");
    $("input#in_eisup").val("");
    $("input#in_q").val("");
    $("input#in_kis_tmc").val("");
    $("input#in_serial").val("");
    $("input#in_comment").val("");
    $("select#in_store").val("");



    $("#store-in").dialog({
        title:"Поступление на склад",
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
            data.serial =$("input#in_serial").val();
            data.comment =$("input#in_comment").val();
            data.kis = $("input#in_kis_tmc").val();
            data.store = $("select#in_store").val();
            data.action = "store-in-q";



            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {

                        $("#store-in").dialog("close");
                        location.href="/regions/storein/page/1/";

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







// Поступление на склад удаление
function StoreInDel(e) {


    var row_id = $(this).parents("tr").attr("row_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-into-rec&row_id="+row_id,
    function(data) {


        $("input#in_name_del").val(data["rec"]["name"]);
        $("input#in_eisup_del").val(data["rec"]["eisup"]);
        $("input#in_store_del").val(data["rec"]["store"]);
        $("input#in_q_del").val(data["rec"]["q"]);
        $("input#in_kis_kod_del").val(data["rec"]["kis"]);
        $("input#in_serial_del").val(data["rec"]["serial"]);
        $("input#in_comment_del").val(data["rec"]["comment"]);


    })




    $("#store-in-del").dialog({
        title:"Поступление на склад удаление",
        buttons:[{ text:"Удалить",click: function() {


            var jqxhr = $.getJSON("/regions/jsondata/?action=store-in-del&row_id="+row_id,
            function(data) {

                location.href="/regions/storein/page/1/";

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

