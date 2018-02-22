$(document).ready(function() {


    $("#id_date1").datepicker($.datepicker.regional['ru']);
    $("#id_date2").datepicker($.datepicker.regional['ru']);


});




// Запрос
function PhoneQuery() {

    var phones = $("input")
    var date1 =
    var date2 =

    var jqxhr = $.getJSON("/working/jsondata/?action=phonequery",
    function(data) {

        if (data["result"] == "ok") {


        }

    })


}

