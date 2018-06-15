$(document).ready(function() {


    // фильтры / поиск по городу улице дому названию компании
    $( "button#search-button" ).bind('click', SearchAddress);
    $( "button#clear-button" ).bind('click', SearchClear);


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





// Поиск по городу улице дому компании
function SearchAddress(e) {

        var city = $("select#search-city").val();
        var street = $("input#search-street").val();
        var house = $("input#search-house").val();
        var company = $("input#search-company").val();

        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-company&city="+city+"&street="+street+"&house="+house+"&company="+company,
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/houselist/1/";

            }

        })


}





// Очистка поиска по городу улице дому
function SearchClear(e) {


        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-company-clear",
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/houselist/1/";

            }

        })


}





