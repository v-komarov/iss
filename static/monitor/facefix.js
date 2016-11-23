$(document).ready(function() {

    // Исправление заголовков таблицы
    FixTableHead();


});



function FixTableHead() {

    // Исправление заголовков таблицы
    var t2 = $("#body-table-events td").eq(2).offset().left;
    var t3 = $("#body-table-events td").eq(3).offset().left;
    var t4 = $("#body-table-events td").eq(4).offset().left;
    var t5 = $("#body-table-events td").eq(5).offset().left;
    var t6 = $("#body-table-events td").eq(6).offset().left;
    var t7 = $("#body-table-events td").eq(7).offset().left;
    var t8 = $("#body-table-events td").eq(8).offset().left;
    var t9 = $("#body-table-events td").eq(9).offset().left;
    var t10 = $("#body-table-events td").eq(10).offset().left;
    var t11 = $("#body-table-events td").eq(11).offset().left;
    var t12 = $("#body-table-events td").eq(12).offset().left;
    var t13 = $("#body-table-events td").eq(13).offset().left;
    var t14 = $("#body-table-events td").eq(14).offset().left;
    var t15 = $("#body-table-events td").eq(15).offset().left;

    $("#head-table-events th").eq(2).offset({'left':t2});
    $("#head-table-events th").eq(3).offset({'left':t3});
    $("#head-table-events th").eq(4).offset({'left':t4});
    $("#head-table-events th").eq(5).offset({'left':t5});
    $("#head-table-events th").eq(6).offset({'left':t6});
    $("#head-table-events th").eq(7).offset({'left':t7});
    $("#head-table-events th").eq(8).offset({'left':t8});
    $("#head-table-events th").eq(9).offset({'left':t9});
    $("#head-table-events th").eq(10).offset({'left':t10});
    $("#head-table-events th").eq(11).offset({'left':t11});
    $("#head-table-events th").eq(12).offset({'left':t12});
    $("#head-table-events th").eq(13).offset({'left':t13});
    $("#head-table-events th").eq(14).offset({'left':t14});
    $("#head-table-events th").eq(15).offset({'left':t15});

    $("#head-table-events th").eq(0).css("width","10px");
    $("#head-table-events th").eq(1).css("width","10px");
    $("#head-table-events td").eq(0).css("width","10px");
    $("#head-table-events td").eq(1).css("width","10px");


}