$(document).ready(function() {

    /*

        Управление фильтрацией по колонкам оперативного журнала

    */

    $("#columns-filter-on").bind("click",FilterColumns);

    //$("#head-table-events th input[type=text]").keyup(function() {

        //FilterColumns();

    //});
    ColorSeverity();

});





function FilterColumns(e) {

    // Показывать все
    var show_all = true;

    $("#body-table-events tr").show();

    $.each($("#body-table-events tr"), function( indexrow, valuerow ) {

        $.each($("#head-table-events th input[type=text]"), function( index, value ) {
            if ($(value).val() != "") {

                if ($(valuerow).children("td").eq(index+2).text().toUpperCase().indexOf($(value).val().toUpperCase()) <= 0 ) { $(valuerow).hide(); }

                // Если все поля пустые , то показываем все
                show_all = false;
            }
        });

    });

    if (show_all == true) { $("#body-table-events tr").show(); }

}




/// Раскраска важности
function ColorSeverity() {
    //console.log($("#body-table-events tr td"));
    $.each($("#body-table-events tr td"), function( index,value) {
        //console.log($(value).text());
        if ($.trim($(value).text()) == "Critical") { $(value).css("color","red").css("font-weight","bold"); }
        if ($.trim($(value).text()) == "Warning") { $(value).css("color","#DAA520").css("font-weight","bold"); }
        if ($.trim($(value).text()) == "Error") { $(value).css("color","#B8860B").css("font-weight","bold"); }

    });

}