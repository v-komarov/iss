$(document).ready(function() {

    // Для списка устройств
    $("table[group=devices] tbody tr").bind("click",ClickEventRow);

    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

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
