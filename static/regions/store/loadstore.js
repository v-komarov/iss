$(document).ready(function() {

   // Загрузка данных
   $("button#btn-load-rest").bind("click", GetTableData);




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










// Очистка поля ввода загружаемого файла
function ClearUploadEisup() {

    $("form#uploadfileeisup input#fileupload").val("");
    $("#uploadform").hide();
    $("#param").show();
    $("#param2").show();
    $("#param3").show();

    //setTimeout("GetTableData();",10000);


}




// Содержимое таблицы
function GetTableData() {

    var frame = $("#uploadframe").contents();
    var table = frame.contents().find("table");


    var col_str_begin = $("input#col-str-begin").val(); // начало строки с которой читаем
    var col_str_end = $("input#col-str-end").val(); // окончание строкой по которую читаем

    var col_name = $("input#col-name").val(); // Название номенклатуры
    var col_store = $("input#col-store").val(); // Название склада
    var col_rest = $("input#col-rest").val(); // Остаток
    var col_dimansion = $("input#col-dimansion").val(); // Единицы измерения
    var col_eisup = $("input#col-eisup").val(); // Код номенклатуры ЕИСУП
    var col_accounting_code = $("input#col-accounting-code").val(); // Счет учета

    var staff = $("select#staff").val(); // id МОЛ
    var region = $("select#region").val(); // id региона

    if (!isNaN(parseInt(col_str_begin)) && !isNaN(parseInt(col_str_end)) && !isNaN(parseInt(col_name)) && !isNaN(parseInt(col_store)) && !isNaN(parseInt(col_dimansion))  && !isNaN(parseInt(col_eisup)) && !isNaN(parseInt(col_accounting_code)) && staff !="" && region != "") {

    var data = {}; // контейнер для данных
    var tabledata = []; // контейнер для таблицы


        // Обход всех строк таблицы
        $(table).find("tr").each(function( index ) {

            // Номер строки
            var row = $(this).children("th").first().text();

            var name = $(this).children("td").eq(col_name).text(); // Название номенклатуры - значение
            var store = $(this).children("td").eq(col_store).text(); // Название склада - значение
            var rest = $(this).children("td").eq(col_rest).text(); // Остаток - значение
            var dimansion = $(this).children("td").eq(col_dimansion).text(); // Единицы измерения - значение
            var eisup = $(this).children("td").eq(col_eisup).text(); // Код номенклатуры - значение
            var accounting_code = $(this).children("td").eq(col_accounting_code).text(); // Код учета - значение


            if (!isNaN(parseInt(row)) && name != "" && store != "" && !isNaN(parseInt(rest)) && dimansion != "" && eisup != ""  && accounting_code != "") {



                // Чтение с начальной строки и по конечную
                if (parseInt(row) >= parseInt(col_str_begin) && parseInt(row) <= parseInt(col_str_end)) {


                    var data_row = {};
                    data_row.name = name;
                    data_row.store = store;
                    data_row.rest = rest;
                    data_row.dimension = dimansion;
                    data_row.eisup = eisup;
                    data_row.accounting_code = accounting_code;

                    tabledata.push(data_row);

                    //console.log(row, name, store, rest, dimansion, eisup, accounting_code);


                }


            }



        });


        // Наполнение контейнера данными
        data.table = tabledata;
        data.staff = staff;
        data.region = region;
        data.action = "store-load-rest";


        Upload(data);
        //console.log(data);


    }
    else { alert("Необходимо правильно заполнить поля!"); }


}






// Загрузка данных в базу
function Upload(data) {


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/regions/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok")  { DiffUpload(result["data"]); }
        }

    });




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
        +"<td "+color_style+">"+value["dimension"]+"</td>"
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


