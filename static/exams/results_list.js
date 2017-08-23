$(document).ready(function() {


    // Первоначально раздел
    if ( $("#manager").attr("section") == "0" ) {
        $( "#select-section" ).val("0");
    }
    else {
        $('#addt').show();
        $("#select-section option[value='0']").remove();
        $( "#select-section" ).val( $("#manager").attr("section") );
    }


    // Выбор раздела
    $( "#select-section" ).change(function() {

        ChoiceSections();

    });


    // Отметка для выгрузки в отчет
    $("table[group=results-list] tbody tr td input[type=checkbox]").bind("click", MarkReport);


});








// Выбор раздела
function ChoiceSections() {

        // Раздел
        var section = $("#select-section").val();

        var jqxhr = $.getJSON("/exams/jsondata/?action=choice-section&section="+section,
        function(data) {

            if (data["result"] == "ok") {

                ClearReport();
                // Отображение вопросов выбранного раздела
                window.location=$("#menuexamsresults a").attr("href");
            }

        })



}



// Отметка о для выгрузки
function MarkReport(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var row_type = $(this).parents("tr").attr("row_type");

    if ($(this).is(":checked")) {
        var status = "yes";
    }
    else { var status = "no"; }

    // Отметка добавть / убрать из списка выгрузки
    var jqxhr = $.getJSON("/exams/jsondata/?action=report&row_id="+row_id+"&status="+status,
    function(data) {


        if (data["result"] == "ok") {


        }

    })


}




// Удаление списка для вывода в отчет
function ClearReport(e) {


    // Отметка добавть / убрать из списка выгрузки
    var jqxhr = $.getJSON("/exams/jsondata/?action=report-clear",
    function(data) {


        if (data["result"] == "ok") {


        }

    })


}



