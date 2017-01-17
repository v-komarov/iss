$(document).ready(function() {

    $("table[group=accidents] tbody tr").bind("click",ClickEventRow);
    $("#editrow").hide(); // первоначально если строка не выделена, то кнопку редактирования прячем


    //$('table[group=accidents]').tableScroll({height:800});

});




// Выделение строки
function ClickEventRow(e) {

        $("table[group=accidents] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=accidents] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#editrow").show();

}

