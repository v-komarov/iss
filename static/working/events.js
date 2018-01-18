$(document).ready(function() {

    // Включить / исключить из отчета
    $("table[group=events-list] tbody").on("click","a[report]",Check);


});






// Отметка включить в отчет или выключить
function Check(e) {

    var arow = $(this);
    var row_id = arow.parents("tr").attr("row_id");
    // Элемент не выбран
    if (arow.children("span").hasClass("glyphicon-unchecked")) {

        var jqxhr = $.getJSON("/working/jsondata/?action=include-report-event&row_id="+row_id,
        function(data) {

            if (data["result"] == "ok") {
                arow.children("span").toggleClass("glyphicon-unchecked",false);
                arow.children("span").toggleClass("glyphicon-check",true);
            }

        })

    }
    // Элемент выбран
    else {
        var jqxhr = $.getJSON("/working/jsondata/?action=exclude-report-event&row_id="+row_id,
        function(data) {

            if (data["result"] == "ok") {
                arow.children("span").toggleClass("glyphicon-check",false);
                arow.children("span").toggleClass("glyphicon-unchecked",true);
            }

        })
    }

}


