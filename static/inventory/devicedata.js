$(document).ready(function() {

    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Отображение данных
    ShowDeviceData();


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



// Переключение закладок
function ChangeNav(e) {
    $("#nav-ports").toggleClass("active",false);
    $("#nav-slots").toggleClass("active",false);
    $("#nav-combo").toggleClass("active",false);
    $("#nav-statuses").toggleClass("active",false);
    $("#nav-removal").toggleClass("active",false);
    $("#nav-parents").toggleClass("active",false);
    $("#nav-properties").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-ports").hide();
    $("#page-slots").hide();
    $("#page-combo").hide();
    $("#page-statuses").hide();
    $("#page-removal").hide();
    $("#page-parents").hide();
    $("#page-properties").hide();

    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}






// Отображение данных по устройству
function ShowDeviceData() {
    var jqxhr = $.getJSON("/inventory/jsondata?action=getdevicedata",
    function(data) {
        console.log(data);
        if (data["result"] != "error") {

            $("#device_model").text(data["result"]["model"]);
            $("#device_address").text(data["result"]["address"]);
            $("#device_company").text(data["result"]["company"]);
            $("#device_status").text(data["result"]["status"]);

        }
    });
}