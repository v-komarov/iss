$(document).ready(function() {

    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);





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
    $("#nav-files").toggleClass("active",false);
    $("#nav-status").toggleClass("active",false);
    $("#nav-public").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-files").hide();
    $("#page-status").hide();
    $("#page-public").hide();

    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

