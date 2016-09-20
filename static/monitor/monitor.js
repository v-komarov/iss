$(document).ready(function() {


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearuuid").bind("click",ClearUuid);
    $("#uuid").bind("keyup",FindUuid);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);

    RowColor();
    //LoadSettings();

/*
    $("#filter-status").multiselect({
        header:true,
        noneSelectedText:"Выбор типов статусов",
        minWidth:500,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });

*/
     // Установка выбранного статуса
     $( "#filter-status" ).change(function() {
        var status_id = $("#filter-status").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?status="+status_id,
            function(data) {

            })
     });

});



// Загрузка настроек
function LoadSettings() {

    var jqxhr = $.getJSON("/monitor/events/jsondata?settings=get",
    function(data) {
        // status
        $('#filter-status option:selected').each(function(){
            this.selected=false;
        });
        $("#filter-status [value='"+data['settings']['status']+"']").attr("selected", "selected");
        // severity
        $('#filter-severity option:selected').each(function(){
            this.selected=false;
        });
        $("#filter-severity [value='"+data['settings']['status']+"']").attr("selected", "selected");


    })

}




function RowColor() {
    $("table[group=events] tbody tr[severity_id=0]").css("color","red");
    $("table[group=events] tbody tr[severity_id=1]").css("color","brown");
    $("table[group=events] tbody tr[severity_id=2]").css("color","#B8860B");
    $("table[group=events] tbody tr[severity_id=3]").css("color","#00008B");
    $("table[group=events] tbody tr[severity_id=4]").css("color","#006400");
}






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


