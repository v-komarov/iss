$(document).ready(function() {

    // Удалить отчет
    $("table[group=reports-list] a").bind("click", DeleteReport);


});



function DeleteReport(e) {

        var report_id = $(this).parents("tr").attr("row_id");
        var name = $(this).parents("tr").children("td").eq(2).text();


        if (confirm("Удалить "+name+" ?")) {

            var jqxhr = $.getJSON("/working/jsondata/?action=delete-report&report_id="+report_id,
            function(data) {

                if (data["result"] == "ok") { location.href="/working/reports/1/"; }

            })


        }



}

