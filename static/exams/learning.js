$(document).ready(function() {

    // начать обучение
    $("button#begin").bind("click", LearnBegin);

});



// Начать обучение
function LearnBegin(e) {

        var test_id = $("information").attr("test_id");

        var jqxhr = $.getJSON("/exams/jsondata/?action=learn-begin&test_id="+test_id,
        function(data) {

            if (data["result"] == "next") {

                console.log(data);

                $("button#begin").hide();
                $("a#back").hide();
                $("button#next").show();

                $("#question-name").text("Вопрос: "+data["question-name"]);
                $("div#question table[group=answers] tbody").append(data["answers"]);
                $("div#question").show();
                $("information").attr("result_id",data["test_result_id"]);

            }

        })

}

