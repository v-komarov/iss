$(document).ready(function() {

    // начать тестирование
    $("button#begin").bind("click", TestBegin);

    // следующий вопрос
    $("button#next").bind("click", TestNext);

    $("div#question").hide();
    $("div#result").hide();


});



// Начать тестирование
function TestBegin(e) {

        var test_id = $("information").attr("test_id");

        var jqxhr = $.getJSON("/exams/jsondata/?action=test-begin&test_id="+test_id,
        function(data) {

            if (data["result"] == "next") {


                // Сохранение id вопроса
                $("information").attr("question_id",data["question_id"]);
                $("information").attr("result_id",data["result_id"]);

                $("button#begin").hide();
                $("a#back").hide();
                $("#result").hide();
                $("button#next").show();

                // Отображение вопроса
                $("#question-name").text("Вопрос: "+data["question-name"]);
                $("div#question table[group=answers] tbody").empty();
                $("div#question table[group=answers] tbody").append(data["answers"]);
                $("div#question").show();

            }

        })

}





// Следующий вопрос
function TestNext(e) {

        var test_id = $("information").attr("test_id");
        var question_id = $("information").attr("question_id");
        var result_id = $("information").attr("result_id");
        // Список правильных ответов
        var answer_list = "";
        $("table[group=answers] tbody tr td input:checkbox:checked").each(function(){
            answer_list = answer_list + $(this).parents("tr").attr("answer_id") + ",";
        });

        var jqxhr = $.getJSON("/exams/jsondata/?action=test-next&result_id="+result_id+"&question_id="+question_id+"&answer_list="+answer_list.substring(0, answer_list.length - 1),
        function(data) {

            // Ответ без ошибок, отображение следующего вопроса
            if (data["result"] == "next") {

                // Сохранение id вопроса
                $("information").attr("question_id",data["question_id"]);

                $("#question-name").text("Вопрос: "+data["question-name"]);
                $("div#question table[group=answers] tbody").empty();
                $("div#question table[group=answers] tbody").append(data["answers"]);
                $("div#question").show();
                $("div#error").hide();
            }


            // Вопросов не осталось, подведение итогов
            if (data["result"] == "end") {
                $("div#error").hide();
                $("div#question").hide();
                $("error").text("");

                // результат
                $("#result").show();

                // Информация о тестировании
                if (data["passed"] == "yes") { $("#result-name").text("Тест сдан!"); $("#result-name").css("color","green"); }
                else { $("#result-name").text("Тест не сдан!"); $("#result-name").css("color","red"); }
                $("#result-mistakes").text("Количество сделанных ошибок "+data["mistakes"]);
                $("#result-mistakes").css("color","brown");

                // Кнопки , ссылка
                $("button#begin").show();
                $("a#back").show();
                $("button#next").hide();
            }


        })

}

