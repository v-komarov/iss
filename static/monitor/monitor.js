$(document).ready(function() {

    $("#floatingCirclesG").attr("hidden","hidden");
    $("table[group=events]").removeAttr("hidden");


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("#uuid").bind("keyup",FindUuid);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);

    $("#clearfirstseen").bind("click",ClearFirstSeen);
    $("#clearlastseen").bind("click",ClearLastSeen);

    $("#runstatus").bind("click",FilterStatus);
    $("#runseverity").bind("click",FilterSeverity);
    $("#runmanager").bind("click",FilterManager);


    RowColor();


    // Фильтр статусов
    $("#filter-status").multiselect({
        header:true,
        noneSelectedText:"Выбор статусов",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#filter-status").multiselect("uncheckAll");
    var status = eval($("#filter-status").attr("selected_value"));
    status.forEach(function(item, i, arr) {
        $("#filter-status").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр статусов конец


    // Фильтр важности
    $("#filter-severity").multiselect({
        header:true,
        noneSelectedText:"Выбор важности",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#filter-severity").multiselect("uncheckAll");
    var severity = eval($("#filter-severity").attr("selected_value"));
    severity.forEach(function(item, i, arr) {
        $("#filter-severity").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр важности конец


    // Фильтр Менеджер
    $("#manager").multiselect({
        header:true,
        noneSelectedText:"Выбор источников",
        minWidth:150,
        selectedText: "# из # выбрано",
        uncheckAllText:"Сбросить все",
        checkAllText:"Отметить все"
    });
    $("#manager").multiselect("uncheckAll");
    var manager = eval($("#manager").attr("selected_value"));
    manager.forEach(function(item, i, arr) {
        $("#manager").multiselect("widget").find(":checkbox[value='"+item+"']").click();
    });
    // Фильтр Менеджер конец


     // Установка first_seen
     $( "#first_seen" ).bind("change paste keyup", function() {
        var first_seen = $("#first_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?first_seen="+first_seen,
            function(data) {
                window.location=$("#menumonitor a").attr("href");
            })
     });

     // Установка last_seen
     $( "#last_seen" ).bind("change paste keyup", function() {
        var last_seen = $("#last_seen").val();
        var jqxhr = $.getJSON("/monitor/events/jsondata?last_seen="+last_seen,
            function(data) {
                window.location=$("#menumonitor a").attr("href");
            })
     });


    $('table[group=events] tbody tr td input[type=checkbox]').on("click",CheckBoxRow);



    $('table[group=events]').tableScroll({height:700});

});







function FilterStatus() {

    var message = $("#filter-status").multiselect("getChecked").map(function(){
       return this.value;
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?status=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}



function FilterSeverity() {

    var message = $("#filter-severity").multiselect("getChecked").map(function(){
       return this.value;
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?severity=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}



function FilterManager() {

    var message = $("#manager").multiselect("getChecked").map(function(){
       return "'"+this.value+"'";
    }).get();

    var jqxhr = $.getJSON("/monitor/events/jsondata?manager=["+message+"]",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
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






// Поиск
function RunSearch(e) {
    console.log("working");
    var search = $("#search").val();
    var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/monitor/events/jsondata?search="+search,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}



// Отмена FirstSeen
function ClearFirstSeen(e) {
    $("#first_seen").val("");
    $("#first_seen").attr("placeholder","");

    var value = "";
    var jqxhr = $.getJSON("/monitor/events/jsondata?first_seen="+value,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}




// Отмена FirstSeen
function ClearLastSeen(e) {
    $("#last_seen").val("");
    $("#last_seen").attr("placeholder","");

    var value = "";
    var jqxhr = $.getJSON("/monitor/events/jsondata?last_seen="+value,
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })
}




// Строчные checkbox-ы
function CheckBoxRow(e) {
    console.log($(this));
    if ($(this).prop('checked') == true) {
        $(this).closest("tr").attr("group",true);
        console.log($(this).closest("tr").attr("group"));
    }
    else {
        $(this).closest("tr").attr("group",false);
        console.log($(this).closest("tr").attr("group"));
    }
}

