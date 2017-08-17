$(document).ready(function() {

    // Сохранение данных вопроса
    $("form#test button[type=submit]").bind("click",EditTestData);

    // Добавление или удаление вопроса из теста
    $("table[group=tests-list] tr input[type=checkbox]").bind("click", TestAddDelQuestion);


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





// Добавление или удаление вопроса из теста
function TestAddDelQuestion(e) {

    // ID вопроса
    var question_id = $(this).parents("tr").attr("row_id");

    // ID теста
    var test_id = $("form#test").attr("test_id");

    // Состояние checkbox
    if ($(this).is(":checked")) { var question = "yes"; }
    else { var question = "no"; }

    // Отправка данных
    var jqxhr = $.getJSON("/exams/jsondata/?action=test-adding-remove-question&test_id="+test_id+"&question_id="+question_id+"&act="+question,
    function(data) {

        if (data["result"] == "ok") {

        }

    })


}







// Сохранение теста
function EditTestData(e) {


    $("form#test #id_name").css("background-color","yellow");
    $("form#test #id_testtime").css("background-color","yellow");
    $("form#test #id_mistakes").css("background-color","yellow");

    var test = $("form#test #id_name").val();
    var test_id = $("form#test").attr("test_id");
    var testtime = $("form#test #id_testtime").val();
    var mistakes = $("form#test #id_mistakes").val();


    if ($("form#test input#id_learning").is(":checked")) { var learn = "yes"; }
    else { var learn = "no"; }



    var data = {};
    data.test = test;
    data.test_id = test_id;
    data.testtime = testtime;
    data.mistakes = mistakes;
    data.learning = learn;
    data.action = "test-save-common-data";

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/exams/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                $("form#test #id_name").css("background-color","");
                $("form#test #id_testtime").css("background-color","");
                $("form#test #id_mistakes").css("background-color","");

            }
        }

    });


}


