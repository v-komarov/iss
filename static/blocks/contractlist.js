$(document).ready(function() {


    // фильтры / поиск договора
    $( "button#search-button" ).bind('click', SearchContract);
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





// Поиск договора
function SearchContract(e) {

        var inn = $("input#search-inn").val();
        var company = $("input#search-company").val();
        var manager = $("select#search-manager").val();

        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-contract&inn="+inn+"&company="+company+"&manager="+manager,
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/contractlist/1/";

            }

        })


}





// Отмена фильтра
function SearchClear(e) {


        var jqxhr = $.getJSON("/blocks/jsondata/?action=filter-contract-clear",
        function(data) {

            if (data["result"] == "ok") {

                location.href="/blocks/contractlist/1/";

            }

        })


}





