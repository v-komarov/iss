$(document).ready(function() {


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#uuid").bind("keyup",FindUuid);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);

    RowColor();


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

     // Установка выбранной важности
     $( "#filter-severity" ).change(function() {
        var severity_id = $("#filter-severity").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?severity="+severity_id,
            function(data) {

            })
     });

     // Установка manager
     $( "#manager" ).change(function() {
        var manager = $("#manager").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?manager="+manager,
            function(data) {

            })
     });

     // Установка first_seen
     $( "#first_seen" ).bind("change paste keyup", function() {
        var first_seen = $("#first_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?first_seen="+first_seen,
            function(data) {

            })
     });

     // Установка last_seen
     $( "#last_seen" ).bind("change paste keyup", function() {
        var last_seen = $("#last_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?last_seen="+last_seen,
            function(data) {

            })
     });

     // Установка search
     $( "#search" ).bind("change paste keyup", function() {
        var search = $("#search").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
            function(data) {

            })
     });



});






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



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
        function(data) {

        })
}


