$(document).ready(function() {

    // начать тестирование
    $("button#begin").bind("click", TestBegin);

    // следующий вопрос
    $("button#next").bind("click", TestNext);

    $("div#question").hide();
    $("div#result").hide();

    // Очистка полей ФИО и Должность
    $("input#id_worker").val("");
    $("input#id_job").val("");
    $("input#id_department").val("");



});






// Таймер
function MinuTimer() {

    var m = parseInt($("minut").text(),10);
    m += 1;
    $("minut").text(m);


}







// Начать тестирование
function TestBegin(e) {

        var test_id = $("information").attr("test_id");

        var fio = $("input#id_worker").val();
        var job = $("input#id_job").val();
        var department = $("input#id_department").val();


        // Проверка заполненности полей ФИО и должность
        if ( fio != "" && job != "" ) {

            var jqxhr = $.getJSON("/exams/jsondata/?action=test-begin&test_id="+test_id+"&fio="+fio+"&job="+job+"&department="+department,
            function(data) {

                if (data["result"] == "next") {

                    // Блокировка полей ФИО и Должность
                    $("input#id_worker").prop("readonly",true);
                    $("input#id_job").prop("readonly",true);
                    $("input#id_department").prop("readonly",true);

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

                    // Запуск таймера
                    window.timerId = setInterval(function() {MinuTimer();}, 60000);



                }

                if (data["result"] == "goaway") {alert("Вы сегодня уже проходили тестирование,\nпопробуйте завтра.\nДля подготовки используйте\nраздел обучения! ");}

            })


        }
        else { alert("Заполните поля ФИО и должность");}


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


            // Отображение следующего вопроса
            if (data["result"] == "next") {

                // Сохранение id вопроса
                $("information").attr("question_id",data["question_id"]);

                $("#question-name").text("Вопрос: "+data["question-name"]);
                $("div#question table[group=answers] tbody").empty();
                $("div#question table[group=answers] tbody").append(data["answers"]);
                $("div#question").show();

                // Количество оставшихся вопросов
                $("q-count").text(data["questions_count"]);
            }


            // Вопросов не осталось, подведение итогов
            if (data["result"] == "end") {
                $("div#question").hide();

                // результат
                $("#result").show();
                // Формирование ссылки на список вопросов
                $("#result-list-questions a").attr("href","/exams/questionsexam/"+result_id);

                // Информация о тестировании
                if (data["passed"] == "yes") { $("#result-name").text("Тест сдан!"); $("#result-name").css("color","green"); }
                else { $("#result-name").text("Тест не сдан!"); $("#result-name").css("color","red"); }
                $("#result-mistakes").text("Количество сделанных ошибок "+data["mistakes"]);
                $("#result-mistakes").css("color","brown");
                // По лимиту времени

                if (data["overtime"] == "yes") { $("#result-timelimit").text("Превышен лимит времени!"); }


                // Кнопки , ссылка
                $("a#back").show();
                $("button#next").hide();

                // Сброс таймера
                clearInterval(window.timerId);

                // Количество оставшихся вопросов
                $("q-count").text("0");


            }


        })

}

