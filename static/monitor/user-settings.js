$(document).ready(function() {

    $("#user-settings").bind("click",UserSettings);
    $("#head-order tbody tr").bind("click",MarkTableOrder);
    $("#head-order-up").bind("click",HeadOrderUp);
    $("#head-order-down").bind("click",HeadOrderDown);


    /// Отображение настроек период обновления таблицы и количество событий на странице
    var refresh_table = $("#refresh-data").attr("refresh_table");
    var row_page_table = $("#row-page-data").attr("row_page_table");
    $("#refresh-data").val(refresh_table);
    $("#row-page-data").val(row_page_table);


    // Освежать данные согласно настроек пользователя
    if (refresh_table != 0) {
        // Освежать экран
        setInterval('UpdateScreen();',1000*refresh_table);

    }





});





// Обновление данных
function UpdateScreen() {

    if ( $("table[group]=events").attr("refresh") == "yes" ) {
        window.location=$("#menumonitor a").attr("href");
        console.log("has refreshed");
    }
}








function MarkTableOrder(e) {
    $("#head-order tbody tr").css("background","");
    $("#head-order tbody tr").attr("marked","no")
    $(this).css("background","#ADD8E6");
    $(this).attr("marked","yes");
}



// Вверх
function HeadOrderUp(e) {

    var up = $("#head-order tbody tr[marked=yes]");
    var index_up = $("#head-order tbody tr").index(up);
    var prev = index_up - 1;

    if (prev >= 0) {
        var down = $("#head-order tbody tr").eq(prev);
        $("#head-order tbody tr").eq(prev).remove();
        $("#head-order tbody tr").eq(prev).after(down);
    }

    $("#head-order tbody tr").bind("click",MarkTableOrder);


}



// Вниз
function HeadOrderDown(e) {
    var count = $("#head-order tbody tr").length - 1;

    var down = $("#head-order tbody tr[marked=yes]");
    var index_down = $("#head-order tbody tr").index(down);
    var next = index_down + 1;

    if (next <= count) {
        var up = $("#head-order tbody tr").eq(next);
        $("#head-order tbody tr").eq(next).remove();
        $("#head-order tbody tr").eq(index_down).before(up);
    }

    $("#head-order tbody tr").bind("click",MarkTableOrder);


}




// Settings
function UserSettings(e) {


    $("#usersettings").dialog({
          title:"Настройки",
          show: {
            effect: "blind",
            duration: 100
          },
          hide: {
            effect: "blind",
            duration: 1500
          },
          buttons: [
            {
                text:"Сохранить",
                click: function() {

                    var arr = [];


                    $.each($("#head-order tbody tr"), function(index,value) {
                        var row = {};
                        row.name = $(value).children("td").attr("name");
                        row.title = $(value).children("td").text();
                        arr.push(row);
                    });


                    data = {};
                    data.action = "save-settings";
                    data.head_order = arr;
                    data.row_page_data = $("#row-page-data").val();
                    data.refresh_data = $("#refresh-data").val();


                    var csrftoken = getCookie('csrftoken');

                    $.ajaxSetup({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        }
                    });




                    $.ajax({
                      url: "/monitor/events/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            window.location=$("#menumonitor a").attr("href");
                        }

                    })







                    $(this).dialog("close");

                }
            },
            {text:"Закрыть", click: function() { $(this).dialog("close")}}],
          modal:true,
          minWidth:200,
          width:400,
          height:400

    });


}

