$(document).ready(function() {

    $("div#buttons button#search-button").bind("click", Search);
    $("div#buttons button#clear-button").bind("click", ClearSearch);
    $("table[group=goods-list] td a").bind("click", EditRest);


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

        if (data["result"] == "ok") { location.href="/regions/store/page/1/"; }

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

        if (data["result"] == "ok") { location.href="/regions/store/page/1/"; }

    })


}







// Очистка поля ввода загружаемого файла
function ClearUploadEisup() {

    $("form#uploadfileeisup input#fileupload").val("");

}





// Результат загрузки данных, запрос замены
function DiffUpload(data) {

    // Отрисовка данных загрузки
    $("table[group=upload-list] tbody").empty();
    $.each(data, function(key,value) {

        if (value["load"] == "yes") { var checked_tag = "";  var color_style = "style=\"background-color: #98FB98;\""; var load_text="Загружен";}
        else { var checked_tag = "<input type=\"checkbox\" />"; var color_style = "style=\"background-color: #F08080;\""; var load_text="";}

        var t = "<tr row_id="+value["id"]+">"
        +"<td "+color_style+">"+ checked_tag +"</td>"
        +"<td "+color_style+">"+value["eisup"]+"</td>"
        +"<td "+color_style+">"+value["name"]+"</td>"
        +"<td "+color_style+">"+value["rest"]+"</td>"
        +"<td "+color_style+">"+value["store"]+"</td>"
        +"<td "+color_style+">"+load_text+"</td>"
        +"</tr>";

        $("table[group=upload-list] tbody").append(t);

    });






    $("#upload-eisup").dialog({
        title:"Загрузка остатков",
        buttons:[{ text:"Применить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            // Выборка данных по отмеченным ckeck-box-ах
            var data_tr = [];
            $.each($("table input[type=checkbox]:checked"), function(key, value) {
                var data_item = {};
                var tr = $(value).parents("tr");
                data_item.row_id = tr.attr("row_id");
                data_item.rest = tr.children("td").eq(3).text();
                data_tr.push(data_item)

            });





                var data = {};
                data.pair = data_tr;
                data.action = "store-resave-rest";


                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { location.href="/regions/store/page/1/"; }
                    }

                });


        }},


            {text:"Закрыть",click: function() {
            location.href="/regions/store/page/1/";
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:800,
        height:400
    });



}








// Корректировка остатков
function EditRest(e) {


    var row_id = $(this).parents("tr").attr("row_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+row_id,
    function(data) {

            if (data["result"] == "ok") {
                $("input#edit_name").val(data["rec"]["name"]);
                $("input#edit_eisup").val(data["rec"]["eisup"]);
                $("input#edit_store").val(data["rec"]["store"]);
                $("input#edit_rest").val(data["rec"]["rest"]);
            }

    });




    $("#edit-rest").dialog({
        title:"Корректировка остатков",
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
            data.row_id = row_id;
            data.rest = $("input#edit_rest").val();
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
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(2).text(data["rec"]["rest"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(7).text(data["rec"]["mol"]);
                            }
                        });

                        $("#edit-rest").dialog("close");

                    }
                }

            });


        }},


            {text:"Закрыть",click: function() {
            //location.href="/regions/store/page/1/";
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:500,
        height:270
    });


}