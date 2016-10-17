$(document).ready(function() {

    $("#floatingCirclesG").attr("hidden","hidden");
    $("table[group=events]").removeAttr("hidden");


    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    //$("#uuid").bind("keyup",FindUuid);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);
    $("table[group=events] tbody tr").bind("mouseenter",EnterRow);
    $("table[group=events] tbody tr").bind("mouseleave",LeaveRow);

    $("#clearfirstseen").bind("click",ClearFirstSeen);
    $("#clearlastseen").bind("click",ClearLastSeen);

    $("#runstatus").bind("click",FilterStatus);
    $("#runseverity").bind("click",FilterSeverity);
    $("#runmanager").bind("click",FilterManager);


    $("#showgroup").bind("click",ShowContainer);
    $("#hidegroup").bind("click",HideContainer);
    $("#addgroup").bind("click",AddContainer);
    //$("#showmembers").bind("click",ShowMembers);
    //$("#hidemembers").bind("click",HideMembers);
    $("#deletemembers").bind("click",DeleteMembers);
    $("#addrow").bind("click",AddRow);
    $("#editrow").bind("click",EditRow);
    $("#editmail").bind("click",EditMail);

    //RowColor();

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
    $("#showgroup").hide();
    $("#editrow").hide();
    $("#editmail").hide();

    if ($("#hidegroup").is(":visible") == true) { $("#addgroup").show(); $("#addrow").hide(); $("#deletemembers").show();}
    else { $("#addgroup").hide(); $("#addrow").show(); $("#deletemembers").hide();}


    // Сброс строковых checkbox-ов
    $("table[group=events] tbody tr td input:checkbox").each(function(){
        $(this).prop( "checked", false );
    });


    $("#containertools").hide();


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

            ShowContainer();
            ShowMembersCount();
        })

}




function ShowMembersCount() {
     $("info").text("Группировка "+$("table[group=events] tbody tr[group=members] td input").length+" элементов");
}




/*
// Свернуть группировку
function HideMembers(e) {

    $("table[group=group] tbody tr[group=members]").empty();
    //$("#showmembers").show();
    //$("#hidemembers").hide();
    $("#deletemembers").hide();
    $("#addgroup").show();

}
*/




/*
// Развернуть группировку
function ShowMembers(e) {
    var jqxhr = $.getJSON("/monitor/events/jsondata?getmembers=ok",
        function(data) {

            data['members'].forEach(function(item,i,arr){

                var icon = "";

                if (item["byhand"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-user\" aria-hidden=\"true\"></span>"; }
                if (item["agregator"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-align-justify\" aria-hidden=\"true\"></span>"; }
                if (item["bymail"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-envelope\" aria-hidden=\"true\"></span>"; }

                var t = "<tr group=members style=\"background-color:#C0C0C0;\" class=\"small\" row_id=\""+item["id"]+"\" marked=\"no\" bymail=\""+item["bymail"]+"\" >"
                +"<td style=\"padding:0;\">"+icon+"</td>"
                +"<td style=\"padding:0;\"><input type=\"checkbox\" class=\"input\"></td>"
                +"<td style=\"padding:0;\"><a id=\"tooltip\" title='"+item['uuid']+"'>"+escape(item['uuid']).substr(0,4)+"...</a></td>"
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
                +"</tr>";

                $("table[group=group] tbody").append(t);

            });

            $("#showmembers").hide();
            $("#hidemembers").show();
            $("#deletemembers").show();
            $("#addgroup").hide();

        })
}
*/






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
            ShowContainer();
            ShowMembersCount();
        })

}








function ShowContainer(e) {
    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    //$("table[group=events] tbody tr[marked=yes]").attr("container","yes");
    $("#containertools").show();
    $("table[group=events] tbody tr").unbind("click",ClickEventRow);

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




function HideContainer(e) {

    $("table[group=events] tbody tr").bind("click",ClickEventRow);
    $("#containertools").hide();
    $("table tr[group=members]").empty();
/*
    var jqxhr = $.getJSON("/monitor/events/jsondata?containergroup=_____",
        function(data) {
            window.location.reload();
        })
*/

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





/*
function RowColor() {
    $("table[group=events] tbody tr[severity_id=0]").css("color","red");
    $("table[group=events] tbody tr[severity_id=1]").css("color","brown");
    $("table[group=events] tbody tr[severity_id=2]").css("color","#B8860B");
    $("table[group=events] tbody tr[severity_id=3]").css("color","#00008B");
    $("table[group=events] tbody tr[severity_id=4]").css("color","#006400");
}
*/





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

}




function EnterRow(e) {
    if ($(this).attr("marked") == "no") {
        $(this).css("background-color"," #DCDCDC");
    }
}


function LeaveRow(e) {
    if ($(this).attr("marked") == "no") {
        $(this).css("background-color","");
    }
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

