$(document).ready(function() {


    // Первоначально раздел
    if ( $("#manager").attr("section") == "0" ) {
        $( "#select-section" ).val("0");
    }
    else {
        $('#addt').show();
        $("#select-section option[value='0']").remove();
        $( "#select-section" ).val( $("#manager").attr("section") );
    }


    // Выбор раздела
    $( "#select-section" ).change(function() {

        ChoiceSections();

    });



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





// Выбор раздела
function ChoiceSections() {

        // Раздел
        var section = $("#select-section").val();

        var jqxhr = $.getJSON("/exams/jsondata/?action=choice-section&section="+section,
        function(data) {

            if (data["result"] == "ok") {

                // Отображение вопросов выбранного раздела
                window.location=$("#menuexamstesting a").attr("href");
            }

        })



}

