$(document).ready(function() {


    // фильтры / поиск по городу улице дому
    $( "button#search-button" ).bind('click', SearchAddress);
    $( "button#search-clear" ).bind('click', SearchClear);


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





// Поиск по городу улице дому
function SearchAddress(e) {

        var city = $("select#search-city").val();
        var street = $("input#search-street").val();
        var house = $("input#search-house").val();

        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-addresslist&city="+city+"&street="+street+"&house="+house,
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/addresslist/1/";

            }

        })


}





// Очистка поиска по городу улице дому
function SearchClear(e) {


        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-addresslist-clear",
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/addresslist/1/";

            }

        })


}





