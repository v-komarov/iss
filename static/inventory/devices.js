$(document).ready(function() {

    // Для списка устройств
    $("table[group=devices] tbody tr").bind("click",ClickEventRow);


    // Для интерфейса списка устройств
    $("#edititem").hide();


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






// Выделение строки устройств
function ClickEventRow(e) {

        $("table[group=devices] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=devices] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#edititem").show();

}

