$(document).ready(function() {




    //setInterval('UpdateData();',5000);
   $("#clearuuid").bind("click",ClearUuid);
   $("#uuid").bind("keyup",FindUuid);
   $("table[group=events] tbody tr").bind("click",ClickEventRow);

});



// Выделение строки
function ClickEventRow(e) {

        $("table[group=events] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=events] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

}



// фильтрация по uuid
function FindUuid(e) {

        if ( ($(this).val().length) != 0 ) {

            $("table[group=events] tbody tr").hide();
            $("table[group=events] tbody tr[uuid="+($(this).val())+"]").show();

        }

        else { $("table[group=events] tbody tr").show(); }

}



// Отмена фильтрации
function ClearUuid(e) {
    $("#uuid").val("");
    $("table[group=events] tbody tr").show();
}


