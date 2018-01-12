$(document).ready(function() {

    // Начало работы
    $("button#working-start").bind("click", WorkStart);
    // Завершение работы
    $("button#working-end").bind("click", WorkEnd);
    // Начало перерыва
    $("button#relax-start").bind("click", RelaxStart);
    // Завершение перерыва
    $("button#relax-end").bind("click", RelaxEnd);

    // Получение статусов пользователя
    GetStatuses();

    // Добавление событий/действий
    $("table[group=marks-card] td a").bind("click", EventPlus);

    // Первоначальное отражение количества
    ShowCount();

});




// Добавление событий - действий
function EventPlus(e) {

    // Показатель
    mark_id = $(this).parents("tr").attr("mark_id");
    // Комментарий
    comment = $(this).parents("td").prev().children("input").val();

    var jqxhr = $.getJSON("/working/jsondata/?action=plus-event&mark_id="+mark_id+"&comment="+comment,
    function(data) {

        if (data["result"] == "ok") {
            var tr = $("table[group=marks-card] tr[mark_id="+data["mark_id"]+"]");
            tr.children("td").eq(1).text(data["count"]);
            tr.children("td").eq(2).children("input").val("");
        }

    })

}






// Первоначальное отображение количества действий или событий
function ShowCount() {

    var jqxhr = $.getJSON("/working/jsondata/?action=showcount",
    function(data) {
        if (data["result"] == "ok") {


            $("table[group=marks-card] tr").each(function(i,elem) {
                $(elem).children("td").eq(1).text("0");
            });

            $.each(data['items'], function(index,value){
                $("table[group=marks-card] tr[mark_id="+value["mark"]+"]").children("td").eq(1).text(value["count"]);
            });


        }

    })


}

















// Получение статусов пользователя (работа, перерыв)
function GetStatuses(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=get-statuses",
    function(data) {

        if (data["result"] == "ok") {

            // Управление видимостью кнопок

            // Не рабочее положение
            if (data["work"] == "no") {
                $("button#working-start").show();
                $("button#working-end").hide();
                $("button#relax-start").hide();
                $("button#relax-end").hide();
                $("user-status").text("Нет").css("color","");
                $("table[group=marks-card] td a").hide();
            }
            // перерыв в работе
            if (data["work"] == "yes" && data["relax"] == "yes") {
                $("button#working-start").hide();
                $("button#working-end").hide();
                $("button#relax-start").hide();
                $("button#relax-end").show();
                $("user-status").text("Перерыв").css("color","green");
                $("table[group=marks-card] td a").hide();
            }
            // Работа
            if (data["work"] == "yes" && data["relax"] == "no") {
                $("button#working-start").hide();
                $("button#working-end").show();
                $("button#relax-start").show();
                $("button#relax-end").hide();
                $("user-status").text("Работа").css("color","red");
                $("table[group=marks-card] td a").show();
                ShowCount();
            }
        }

    })

}





// начало работы (новая смена)
function WorkStart(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=work-start",
    function(data) {
        if (data["result"] == "ok") {GetStatuses();}

    })

}





// завершение работы (конец смены)
function WorkEnd(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=work-end",
    function(data) {
        if (data["result"] == "ok") {GetStatuses();}

    })

}



// начало перерыва
function RelaxStart(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=relax-start",
    function(data) {
        if (data["result"] == "ok") {GetStatuses();}

    })

}



// завершение перерыва
function RelaxEnd(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=relax-end",
    function(data) {
        if (data["result"] == "ok") {GetStatuses();}

    })

}
