$(document).ready(function() {


    // Отображение значений фильтров
    $( "select#select-region" ).val( $( "select#select-region" ).attr("region") );
    $( "select#select-city" ).val( $( "select#select-city" ).attr("city") );



    // Выбор региона
    $( "select#select-region" ).change(function() { ChoiceRegion(); });

    // Выбор населенного пункта
    $( "select#select-city" ).change(function() { ChoiceCity(); });




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



// Выбор региона
function ChoiceRegion() {

        // регион
        var region = $("select#select-region").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=filter-region-reestr&region_id="+region,
        function(data) {

            if (data["result"] == "ok") {

                location.reload();

            }

        })



}





// Выбор населенного пункта
function ChoiceCity() {

        // Населенный пункт
        var city = $("select#select-city").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=filter-city-reestr&city_id="+city,
        function(data) {

            if (data["result"] == "ok") {

                location.reload();

            }

        })



}

