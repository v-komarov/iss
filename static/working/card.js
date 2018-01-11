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

});



// Получение статусов пользователя (работа, перерыв)
function GetStatuses(e) {

    var jqxhr = $.getJSON("/working/jsondata/?action=get-statuses",
    function(data) {

        if (data["result"] == "ok") {

            // Управление видимостью кнопок
            if (data["work"] == "no") {
                $("button#working-start").show();
                $("button#working-end").hide();
                $("button#relax-start").hide();
                $("button#relax-end").hide();
                $("user-status").text("Нет").css("color","");
            }
            if (data["work"] == "yes" && data["relax"] == "yes") {
                $("button#working-start").hide();
                $("button#working-end").hide();
                $("button#relax-start").hide();
                $("button#relax-end").show();
                $("user-status").text("Перерыв").css("color","green");
            }
            if (data["work"] == "yes" && data["relax"] == "no") {
                $("button#working-start").hide();
                $("button#working-end").show();
                $("button#relax-start").show();
                $("button#relax-end").hide();
                $("user-status").text("Работа").css("color","red");
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
