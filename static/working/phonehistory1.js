$(document).ready(function() {


    $("input#date").datepicker($.datepicker.regional['ru']);

    $("button#filter").bind("click", Filter);
    $("button#clear-filter").bind("click", ClearFilter);


});



// Фильтрация
function Filter(e) {

    var date = $("input#date").val();
    var phone = $("select#phone").val();
    var city = $("select#city").val();

    var trs = $("table[group=phonehistory1] tbody tr");
    //trs.hide();

    trs.each(function(i,elem) {

        var row_city = $(elem).children("td").eq(0).text();
        var row_date = $(elem).children("td").eq(1).text();
        var row_phone = $(elem).children("td").eq(2).text();



        if ( ( date == "" || date == row_date ) && ( phone == "" || phone == row_phone ) && ( city == "" || city == row_city ) ) {
            $(elem).show();
        }
        else { $(elem).hide();}

    });


}



// Отмена фильтрации
function ClearFilter(e) {

    $("select#city").val("");
    $("select#phone").val("");
    $("input#date").val("");

    $("table[group=phonehistory1] tbody tr").show();

}