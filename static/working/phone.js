$(document).ready(function() {


    $("#date1").datepicker($.datepicker.regional['ru']);
    $("#date2").datepicker($.datepicker.regional['ru']);


    // Создать отчет
    $("button#button-get").bind("click", PhoneQuery);


});




// Запрос
function PhoneQuery(e) {

    $("result").empty();

    var phones = $("input#phones").val();
    var filter = $("input#filter").val();
    var date1 = $("input#date1").val();
    var date2 = $("input#date2").val();


    if (phones !="" && date1 != "" && date2 != "") {

        $("result").append($("<h3>Подготовка данных...</h3>").css("margin-left","300px"));


        var jqxhr = $.getJSON("/working/jsondata/?action=phonequery&phones="+phones+"&filter="+filter+"&date1="+date1+"&date2="+date2,
        function(data) {

            if (data["result"] == "ok") {

                $("result").empty();

                var t = "<p><table class=\"table\"><tbody>"
                +"<tr><td>Всего вызовов</td><td>"+data["calls_total"]+"</td></tr>"
                +"<tr><td>Исходящих вызовов</td><td>"+data["calls_out"]+"</td></tr>"
                +"<tr><td>Входящих вызовов</td><td>"+data["calls_in"]+"</td></tr>"
                +"<tr><td>Исходящих принятых</td><td>"+data["calls_out_ok"]+"</td></tr>"
                +"<tr><td>Входящих принятых</td><td>"+data["calls_in_ok"]+"</td></tr>"
                +"<tr><td>Исходящие средняя продолжительность разговора</td><td>"+data["calls_out_avg"]+" сек.</td></tr>"
                +"<tr><td>Входящие средняя продолжительность разговора</td><td>"+data["calls_in_avg"]+" сек.</td></tr>"
                +"<tr><td>Отношение исходящих принятых</td><td>"+data["calls_out_p"]+" %</td></tr>"
                +"<tr><td>Отношение входящих принятых</td><td>"+data["calls_in_p"]+" %</td></tr>"
                +"</tbody></table></p>";

                $("result").append(t);
                $("table").css("margin-left","300px").css("width","600px");

            }

            if (data["result"] == "zero") {
                $("result").empty();
                $("result").append($("<h3>Пустая выборка данных...</h3>").css("margin-left","300px"));
            }

        })


    }
    else { alert("Задайте период дат и номара внутр. телефонов через запятую");}


}

