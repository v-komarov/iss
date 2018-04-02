$(document).ready(function() {

    $("div#buttons button#search-button").bind("click", Search);
    $("div#buttons button#clear-button").bind("click", ClearSearch);
    $("button#create-button").bind("click", StoreIn);

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

    console.log("xxxxxxxxxxx");

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

            /*
            var data = {};
            data.row_id = row_id;
            data.rest = $("input#edit_rest").val();
            data.name = $("input#edit_name").val();
            data.action = "store-edit-rest";



            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {
                        $("table[group=goods-list] tr[row_id="+row_id+"]").css("background-color","#F0E68C");
                        var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+row_id,
                        function(data) {
                            if (data["result"] == "ok") {
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(1).text(data["rec"]["name"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(2).text(data["rec"]["rest"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(7).text(data["rec"]["mol"]);
                            }
                        });

                        $("#edit-rest").dialog("close");

                    }
                }

            });
            */

        }},


            {text:"Закрыть",click: function() {
            //location.href="/regions/store/page/1/";
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:350
    });


}

