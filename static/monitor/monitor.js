$(document).ready(function() {

    $("#floatingCirclesG").attr("hidden","hidden");
    $("table[group=events]").removeAttr("hidden");


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);
    $("table[group=events] tbody tr").bind("mouseenter",EnterRow);
    $("table[group=events] tbody tr").bind("mouseleave",LeaveRow);

    $("#clearfirstseen").bind("click",ClearFirstSeen);
    $("#clearlastseen").bind("click",ClearLastSeen);

    $("#runstatus").bind("click",FilterStatus);
    $("#runseverity").bind("click",FilterSeverity);
    $("#runmanager").bind("click",FilterManager);
    $("#filtergroup").bind("click",FilterGroup);

    //$("table[group=events] tbody tr td a").bind("click",ChooseActions);
    $("ul.dropdown-menu li a[action=container]").bind("click",ShowContainer);
    $("#addgroup").bind("click",AddContainer);
    $("#deletemembers").bind("click",DeleteMembers);
    $("#addrow").bind("click",AddRow);
    $("#editrow").bind("click",EditRow);
    $("#editmail").bind("click",EditMail);


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

    // Видимость кнопок
    $("#editrow").hide();
    $("#editmail").hide();
    //$("#sendmess").hide();
    //$("#working").hide();

/*
    if ($("#hidegroup").is(":visible") == true) { $("#addgroup").show(); $("#addrow").hide(); $("#deletemembers").show();}
    else { $("#addgroup").hide(); $("#addrow").show(); $("#deletemembers").hide();}
*/

    // Сброс строковых checkbox-ов
    $("table[group=events] tbody tr td input:checkbox").each(function(){
        $(this).prop( "checked", false );
    });


    $("#containertools").hide();
    $("table[group=events] tbody tr td input").hide();

    // Зебра
    zebra = "#FFF5EE"
    $("table[group=events] tbody tr:odd").css("background-color",zebra)


});










// Удаление выбранных элементов из контейнера
function DeleteMembers(e) {

    var container_row = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    var id = [];
    var i = $("table[group=events] tbody tr[group=members] td input:checked");
    $.each( i, function( key, value ) {
        id.push("'"+$(value).closest("tr").attr("row_id")+"'");
    });

    var jqxhr = $.getJSON("/monitor/events/jsondata?container_row="+container_row+"&delgroup=["+id+"]",
        function(data) {

            GetMemebersContainer();
            ShowMembersCount();
        })

}




function ShowMembersCount() {
     $("info").text("Группировка "+$("table[group=events] tbody tr[group=members] td input").length+" элементов");
}












// Добавление в группировку
function AddContainer(e) {

    var container_row = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    var id = []
    var row_list = $("table[group=events] tbody tr[group=true]");
    $.each( row_list, function( key, value ) {
        id.push("'"+$(value).attr("row_id")+"'");
    });

    var jqxhr = $.getJSON("/monitor/events/jsondata?container_row="+container_row+"&addgroup=["+id+"]",
        function(data) {
            //window.location.reload();
                // Скрываем добавленные события из общего списка
                $.each( row_list, function( key, value ) {
                    $(value).hide();
                });
            GetMemebersContainer();
            ShowMembersCount();
        })

}








function GetMemebersContainer() {

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?container_row="+row_id+"&getmembers=ok",
        function(data) {
            $("table tr[group=members]").empty();
            data['members'].forEach(function(item,i,arr){

                var icon = "";

                if (item["byhand"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-user\" aria-hidden=\"true\"></span>"; }
                if (item["agregator"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-align-justify\" aria-hidden=\"true\"></span>"; }
                if (item["bymail"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-envelope\" aria-hidden=\"true\"></span>"; }

                var t = "<tr group=members style=\"background-color:#F5DEB3;\" class=\"small\" row_id=\""+item["id"]+"\" marked=\"no\" bymail=\""+item["bymail"]+"\" >"
                +"<td style=\"padding:0;\">"+icon+"</td>"
                +"<td style=\"padding:0;\"><input type=\"checkbox\" class=\"input\"></td>"
                +"<td style=\"padding:0;\">"+item['first_seen']+"</td>"
                +"<td style=\"padding:0;\">"+item['last_seen']+"</td>"
                +"<td style=\"padding:0;\">"+item['status']+"</td>"
                +"<td style=\"padding:0;\">"+item['severity']+"</td>"
                +"<td style=\"padding:0;\">"+item['manager']+"</td>"
                +"<td style=\"padding:0;\">"+item['event_class']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_system']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_group']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_class']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_net_address']+"</td>"
                +"<td style=\"padding:0;\">"+item['device_location']+"</td>"
                +"<td style=\"padding:0;\">"+item['element_identifier']+"</td>"
                +"<td style=\"padding:0;\">"+item['element_sub_identifier']+"</td>"
                +"<td style=\"padding:0;\">"+item['summary']+"</td>"
                +"</tr>";

                $("table[group=events] tbody tr[marked=yes]").after(t);

            });

        ShowMembersCount();

        })


}








function ShowContainer(e) {



    $("table[group=events] tbody tr").unbind("click",ClickEventRow);
    // Сброс отметки строки
    $("table[group=events] tbody tr").css("background-color","");
    $("table[group=events] tbody tr").attr("marked","no");

    var row_id = $(this).closest("tr").attr("row_id");



    $($(this).closest("div.dropdown")).hide();
    $("table[group=events] tbody tr td a[container_hide="+row_id+"]").show();
    $("#containertools").show();
    $("table[group=events] tbody tr td input").show();
    // Обозначение контейнера
    $("table[group=events] tbody tr[row_id="+row_id+"]").attr("marked","yes");
    $("table[group=events] tbody tr[row_id="+row_id+"]").css("background-color","brown").css("color","white");

    $("table[group=events] tbody tr td a").unbind("click",ShowContainer);
    $("table[group=events] tbody tr td a[container_hide="+row_id+"]").bind("click",HideContainer);

    GetMemebersContainer();

    $("table[group=events] tbody tr").unbind("mouseenter",EnterRow);
    $("table[group=events] tbody tr").unbind("mouseleave",LeaveRow);


}




function HideContainer(e) {

    $("table[group=events] tbody tr").bind("click",ClickEventRow);
    $("#containertools").hide();
    $("table tr[group=members]").empty();

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    $(this).prev("div.dropdown").show();
    $("ul.dropdown-menu li a[action=container]").bind("click",ShowContainer);

    $("table[group=events] tbody tr td input").hide();
    $("table[group=events] tbody tr td a[container_hide="+row_id+"]").hide();

    $("table[group=events] tbody tr[row_id="+row_id+"]").attr("marked","no");
    $("table[group=events] tbody tr[row_id="+row_id+"]").css("background-color","").css("color","");

    $("table[group=events] tbody tr").bind("mouseenter",EnterRow);
    $("table[group=events] tbody tr").bind("mouseleave",LeaveRow);


}




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





// Выделение строки
function ClickEventRow(e) {

        $("table[group=events] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=events] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");
        if ($("#hidegroup").is(":visible") != true) {
            $("#showgroup").show();
        }
        if ($(this).attr("byhand") == "yes") { $("#editrow").show(); }
        else { $("#editrow").hide(); }
        if ($(this).attr("bymail") == "yes") { $("#editmail").show(); }
        else { $("#editmail").hide(); }

        //$("#sendmess").show();
        //$("#working").show();

}




function EnterRow(e) {
    if ($(this).attr("marked") == "no") {
        $(this).css("background-color"," #DCDCDC");
    }
    //$("table[group=events] tbody tr:odd").css("background-color",window.zebra)
}


function LeaveRow(e) {
    if ($(this).attr("marked") == "no") {
        $(this).css("background-color","");
    }
    $("table[group=events] tbody tr:odd").css("background-color",window.zebra)
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
    //console.log($(this));
    if ($(this).prop('checked') == true) {
        $(this).closest("tr").attr("group",true);
        //console.log($(this).closest("tr").attr("group"));
    }
    else {
        $(this).closest("tr").attr("group",false);
        //console.log($(this).closest("tr").attr("group"));
    }
}




// Фильтр по группировкам
function FilterGroup(e) {

    var jqxhr = $.getJSON("/monitor/events/jsondata?filtergroup=ok",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}