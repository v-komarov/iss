$(document).ready(function() {

    // Сохранение данных вопроса
    $("form#question button[type=submit]").bind("click",EditQuestionData);

    $("button#addanswer").bind("click", AddAns);

    // Отображение списка ответов
    ShowAnsList();

    // Удаление варианта ответа
    $("table[group=answers-list] tbody").on("click", "a[delete]", DeleteAnswer);

    // Редактирование варианта ответа
    $("table[group=answers-list] tbody").on("click", "a[ans]", EditAns);


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





// Удаление варианта ответа
function DeleteAnswer(e) {

    var answer_id = $(this).parents("tr").attr("row_id");
    var answer = $(this).parents("tr").children("td").eq(2).text();
    var deleteanswer = confirm("Удаляем ответ:\n"+answer+"\n?");

    if (deleteanswer) {


        var jqxhr = $.getJSON("/exams/jsondata/?action=delete-answer&answer_id="+answer_id,
        function(data) {

            if (data["result"] == "ok") {

                // Отображение ответов
                ShowAnsList();

            }

        })


    }

}







// Сохранение вопроса
function EditQuestionData(e) {


    $("form#question #id_name").css("background-color","yellow");

    var question = $("form#question #id_name").val();
    var question_id = $("form#question").attr("question_id");


    var data = {};
    data.question = question;
    data.question_id = question_id;
    data.action = "question-save-common-data";

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

                $("form#question #id_name").css("background-color","");

            }
        }

    });



}





// Добавление ответа
function AddAns(e) {
    // Формирование формы
    var jqxhr = $.getJSON("/exams/jsondata/?action=get-data-create-answer",
    function(data) {


        if (data["result"] == "ok") {

            $("form#answerdata table tbody").empty();
            $("form#answerdata table tbody").append(data["form"]);

            $("form#answerdata").attr("action","create-answer-data");
            $("form#answerdata").attr("answer_id","");

            DataAns();

        }

    })

}





// Редактирование ответа
function EditAns(e) {

    var answer_id = $(this).parents("tr").attr("row_id");

    // Формирование формы
    var jqxhr = $.getJSON("/exams/jsondata/?action=get-data-edit-answer&answer_id="+answer_id,
    function(data) {


        if (data["result"] == "ok") {

            $("form#answerdata table tbody").empty();
            $("form#answerdata table tbody").append(data["form"]);

            $("form#answerdata").attr("action","edit-answer-data");
            $("form#answerdata").attr("answer_id",answer_id);

            DataAns();

        }

    })

}








// Сохранение данных ответа
function DataAns(e) {


    $("#answer-data").dialog({
        title:"Добавление варианта ответа",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


                // Проверка значений
                if ( $("form#answerdata textarea#id_name").val() != "" ) {


                    if ($("form#answerdata input#id_truth").is(":checked")) { var truth = "yes"; }
                    else { var truth = "no"; }


                    var data = {};
                    data.question_id = $("form#question").attr("question_id");
                    data.name = $("form#answerdata textarea#id_name").val();
                    data.action = $("form#answerdata").attr("action");
                    data.truth = truth;
                    data.answer_id = $("form#answerdata").attr("answer_id");

                    $.ajax({
                      url: "/exams/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#answer-data").dialog('close'); ShowAnsList(); }
                        }

                    });

                }
                else { alert("Заполните поля!"); }


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        open: function() {
        },
        modal:true,
        minWidth:500,
        width:600

    });

}





// Отображение списка возможных ответов
function ShowAnsList() {


    var question_id = $("form#question").attr("question_id");

    var jqxhr = $.getJSON("/exams/jsondata/?action=get-question-answers-list&question_id="+question_id,
    function(data) {


        if (data["result"] == "ok") {

            console.log(data);

            $("table[group=answers-list] tbody").empty();
            $("table[group=answers-list] tbody").append(data["rows"]);


        }

    })



}