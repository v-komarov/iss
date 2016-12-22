$(document).ready(function() {

    //FixTableHead();

});



function FixTableHead() {

    // Исправление заголовков таблицы
    // Исправление ширины столбцов таблицы
    $("#body-table-events th").eq(0).width(6);
    $("#body-table-events th").eq(1).width(6);

    $("#body-table-events tr td").eq(2).width($("#head-table-events tr th").eq(2).width()-12);
    $("#body-table-events tr td").eq(3).width($("#head-table-events tr th").eq(3).width());
    $("#body-table-events tr td").eq(4).width($("#head-table-events tr th").eq(4).width());
    $("#body-table-events tr td").eq(5).width($("#head-table-events tr th").eq(5).width());
    $("#body-table-events tr td").eq(6).width($("#head-table-events tr th").eq(6).width());
    $("#body-table-events tr td").eq(7).width($("#head-table-events tr th").eq(7).width());
    $("#body-table-events tr td").eq(8).width($("#head-table-events tr th").eq(8).width());
    $("#body-table-events tr td").eq(9).width($("#head-table-events tr th").eq(9).width());
    $("#body-table-events tr td").eq(10).width($("#head-table-events tr th").eq(10).width());
    $("#body-table-events tr td").eq(11).width($("#head-table-events tr th").eq(11).width()-1);
    $("#body-table-events tr td").eq(12).width($("#head-table-events tr th").eq(12).width()-1);
    $("#body-table-events tr td").eq(13).width($("#head-table-events tr th").eq(13).width()-1);
    $("#body-table-events tr td").eq(14).width($("#head-table-events tr th").eq(14).width()-1);


}
