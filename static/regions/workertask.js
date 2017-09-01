$(document).ready(function() {

    $("#begin-date").datepicker($.datepicker.regional['ru']);
    $("#end-date").datepicker($.datepicker.regional['ru']);

    $( "#begin-date" ).change(function() {

        // Сохранение
        var jqxhr = $.getJSON("/regions/jsondata/?action=workertask-begin&date="+$("#begin-date").val(),
            function(data) {

        })

    });


    $( "#end-date" ).change(function() {

        // Сохранение
        var jqxhr = $.getJSON("/regions/jsondata/?action=workertask-end&date="+$("#end-date").val(),
            function(data) {

        })

    });


    $( "select#worker" ).change(function() {

        // Сохранение
        var jqxhr = $.getJSON("/regions/jsondata/?action=workertask-worker&worker="+$("select#worker").val(),
            function(data) {

        })

    });



    // Найти информацию
    $("button#get-report-data").bind("click", GetData);


});



// Получение информации
function GetData(e) {
    window.location="/regions/workertask/1/";
}