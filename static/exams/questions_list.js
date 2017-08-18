$(document).ready(function() {


    // Первоначально раздел
    if ( $("#manager").attr("section") == "0" ) {
        $( "#select-section" ).val("0");
    }
    else {
        $('#addq').show();
        $("#select-section option[value='0']").remove();
        $( "#select-section" ).val( $("#manager").attr("section") );
    }


    // Выбор раздела
    $( "#select-section" ).change(function() {

        ChoiceSections();

    });



    // Удаление строки - вопроса
    $("table[group=questions-list] tbody tr td a[remove]").bind("click",DeleteQuestion);


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
                window.location=$("#menuexamsquestions a").attr("href");

            }

        })



}




// Удаление вопроса
function DeleteQuestion(e) {

    var question_id = $(this).parents("tr").attr("row_id");
    var question = $(this).attr("question");
    var deletequestion = confirm("Удаляем вопрос:\n"+question+"\n?");

    if (deletequestion) {


        var jqxhr = $.getJSON("/exams/jsondata/?action=delete-question&question_id="+question_id,
        function(data) {

            if (data["result"] == "ok") {

                // Отображение вопросов
                location.reload();

            }

        })


    }


}

