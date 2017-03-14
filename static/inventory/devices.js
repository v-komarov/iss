$(document).ready(function() {

    // Для списка устройств
    $("table[group=devices] tbody tr").bind("click",ClickEventRow);

    // Для интерфейса списка устройств
    $("#edititem").hide();

    $("#edititem").bind("click",DeviceData);




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








// Данные устройства - переход
function DeviceData(e) {
    var dev_id = $("table[group=devices] tbody tr[marked=yes]").attr("row_id");
    var jqxhr = $.getJSON("/inventory/jsondata?dev_id="+dev_id+"&action=savedevid",
    function(data) {
        console.log(data);
        if (data["result"] == "ok") { window.location.href = "/inventory/devicedata/?dev="+dev_id; }

    });
}

