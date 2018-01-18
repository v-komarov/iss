$(document).ready(function() {

    // Включить / исключить из отчета
    $("table[group=makereports-list] tbody").on("click","a[report]",Include);

    // Очистить поле ввода названия отчета
    $("button#clear-button").bind("click", ClearName);

    // Создать отчет
    $("button#create-button").bind("click", CreateReport);


});






function CreateReport(e) {

    var report_name = $("input#create-text").val();

    if (report_name != "") {

        var jqxhr = $.getJSON("/working/jsondata/?action=create-report&report_name="+report_name,
        function(data) {

            if (data["result"] == "ok") {

                // Очистить флаги
                $("table[group=makereports-list] a[report]").each(function(i,elem) {

                    if ($(elem).children("span").hasClass("glyphicon-check")) {
                        $(elem).children("span").toggleClass("glyphicon-check",false);
                        $(elem).children("span").toggleClass("glyphicon-unchecked",true);
                    }

                });
                $("input#create-text").val("");

                $("#report-ok").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});
                $("#report-ok").dialog("close");

            }
            else {
                $("#report-error").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});
                $("#report-error").dialog("close");
            }

        })

    }

}






function ClearName(e) {

    $("input#create-text").val("");

}





// Отметка включить в отчет или выключить
function Include(e) {

    var arow = $(this);
    var row_id = arow.parents("tr").attr("row_id");
    // Элемент не выбран
    if (arow.children("span").hasClass("glyphicon-unchecked")) {

        var jqxhr = $.getJSON("/working/jsondata/?action=include-report-working&row_id="+row_id,
        function(data) {

            if (data["result"] == "ok") {
                arow.children("span").toggleClass("glyphicon-unchecked",false);
                arow.children("span").toggleClass("glyphicon-check",true);
            }

        })

    }
    // Элемент выбран
    else {
        var jqxhr = $.getJSON("/working/jsondata/?action=exclude-report-working&row_id="+row_id,
        function(data) {

            if (data["result"] == "ok") {
                arow.children("span").toggleClass("glyphicon-check",false);
                arow.children("span").toggleClass("glyphicon-unchecked",true);
            }

        })
    }

}

