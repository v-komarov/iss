$(document).ready(function() {


    // Отображение значений фильтров
    $( "select#select-inout" ).val( $( "select#select-inout" ).attr("inout_value") );
    $( "select#select-message" ).val( $( "select#select-message" ).attr("message_type_value") );
    $( "select#select-status" ).val( $( "select#select-status" ).attr("message_status_value") );



    // Выбор Входящие или исходящие
    $( "select#select-inout" ).change(function() { ChoiceInOut(); });

    // Выбор вида сообщения
    $( "select#select-message" ).change(function() { ChoiceMessageType(); });

    // Выбор статуса сообщения
    $( "select#select-status" ).change(function() { ChoiceMessageStatus(); });


    // Переход на редактирование
    $("table[group=docs-list] tbody td a").bind("click",LinkEditMessage);


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



// Выбор Входящие или Исходящие
function ChoiceInOut(e) {

        // inout
        var inout = $("select#select-inout").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=filter-docs-inout&inout_id="+inout,
        function(data) {

            if (data["result"] == "ok") {

                location.reload();

            }

        })



}






// Выбор вида сообщения
function ChoiceMessageType(e) {

        // Вид сообщения
        var mess_type = $("select#select-message").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=filter-docs-messagetype&mess_type="+mess_type,
        function(data) {

            if (data["result"] == "ok") {

                location.reload();

            }

        })


}






// Выбор статуса сообщения
function ChoiceMessageStatus(e) {

        // Статус сообщения
        var mess_status = $("select#select-status").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=filter-docs-messagestatus&mess_status="+mess_status,
        function(data) {

            if (data["result"] == "ok") {

                location.reload();

            }

        })


}






// Сохранить id сообщения и перейти
function LinkEditMessage(e) {

        // id сообщешия
        var message_id = $(this).parents("tr").attr("row_id");;

        var jqxhr = $.getJSON("/regions/jsondata/?action=docs-save-id&message_id="+message_id,
        function(data) {

            if (data["result"] == "ok") {

                window.location.href = "/regions/docs/edit/update/";

            }

        })


}
