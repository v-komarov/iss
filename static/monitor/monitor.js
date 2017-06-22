$(document).ready(function() {




    $("#floatingCirclesG").attr("hidden","hidden");
    $("table[group=events]").removeAttr("hidden");

    $("#first_seen").datepicker($.datepicker.regional['ru']);
    $("#last_seen").datepicker($.datepicker.regional['ru']);


    $("#mark-all").bind("click",MarkAll);

    //setInterval('UpdateData();',5000);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("table[group=events] tbody tr").bind("click",ClickEventRow);
    //$("table[group=events] tbody tr").bind("mouseenter",EnterRow);
    //$("table[group=events] tbody tr").bind("mouseleave",LeaveRow);

    $("#clearfirstseen").bind("click",ClearFirstSeen);
    $("#clearlastseen").bind("click",ClearLastSeen);

    $("#runstatus").bind("click",FilterStatus);
    $("#runseverity").bind("click",FilterSeverity);
    $("#runmanager").bind("click",FilterManager);
    $("#filtergroup").bind("click",FilterGroup);
    $("#filteraccident").bind("click",FilterAccident);
    $("#filterhistory").bind("click",FilterHistory);

    //$("table[group=events] tbody tr td a").bind("click",ChooseActions);
    $("ul.dropdown-menu li a[action=zkl]").bind("click",GetZkl);
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

    //$('table[group=events]').tableScroll({height:700});

    // Видимость кнопок
    $("#editrow").hide();
    $("#editmail").hide();


    // Сброс строковых checkbox-ов
    $("table[group=events] tbody tr td input:checkbox").each(function(){
        $(this).prop( "checked", false );
    });


    $("#containertools").hide();
    $("table[group=events] tbody tr td input").hide();

    // Зебра
    //zebra = "#FFF5EE"
    //$("table[group=events] tbody tr:odd").css("background-color",zebra)

    // Видимость checkbox-a "выбрать все"
    $("#mark-all").hide();






});






function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}





function getCookie(name) {

    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}











function FreshScreenOn(e) {
    $(this).attr("freshscreen","yes");
    console.log("screen on");
}








// Отметка всех строк-событий для включения в группировку
function MarkAll(e) {

    var status = $("#mark-all").prop("checked");
    if (status == true) {
        $("table[group=events] tr[group=false] td input:checkbox").prop("checked",true);
        $("table[group=events] tr[group=false]").attr("group",true);
    }
    else {
        $("table[group=events] tr[group=true] td input").removeAttr("checked");
        $("table[group=events] tr[group=true]").attr("group",false);
    }
}





// Запрос ЗКЛ
function GetZkl(e) {

    var row_id = $(this).closest("tr").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?getzkl=ok&event_id="+row_id,
        function(data) {

            //console.log(data);
            $("table[group=zkllist] tbody").empty();
            $("table[group=zkllist] tfoot").empty();

            var use = 0;
            var reserv = 0;
            var tech = 0;


            $.each(data, function(key,value) {


                var t = "<tr group=zkllist>"
                +"<td style=\"padding:0;\">"+value['sysname']+"</td>"
                +"<td style=\"padding:0;\">"+value['address']+"</td>"
                +"<td style=\"padding:0;\">"+value['ip']+"</td>"
                +"<td style=\"padding:0;\">"+value['port_use']+"</td>"
                +"<td style=\"padding:0;\">"+value['port_reserv']+"</td>"
                +"<td style=\"padding:0;\">"+value['port_tech']+"</td>"
                +"</tr>";

                $("table[group=zkllist] tbody").append(t);


                use = use + value['port_use'];
                reserv = reserv + value['port_reserv'];
                tech = tech + value['port_tech'];

                //console.log(key,value);

            });

            // footer
            var tt = "<tr group=zkllist>"
            +"<td style=\"padding:0;\">Всего</td>"
            +"<td></td>"
            +"<td></td>"
            +"<td style=\"padding:0;\">"+use+"</td>"
            +"<td style=\"padding:0;\">"+reserv+"</td>"
            +"<td style=\"padding:0;\">"+tech+"</td>"
            +"</tr>";

            $("table[group=zkllist] tfoot").append(tt);



            $("#zkllist").dialog({
                open:function() {
                $(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar-close").remove();
                $("table[group=events]").attr("refresh","no");
                },
                  title:"ЗКЛ",
                closeOnEscape: false,
                  show: {
                    effect: "blind",
                    duration: 100
                  },
                  hide: {
                    effect: "blind",
                    duration: 1500
                  },
                  buttons: [{text:"Закрыть", click: function() { $(this).dialog("close"); $("table[group=events]").attr("refresh","yes"); }}],
                  modal:true,
                  minWidth:400,
                  width:900,
                  height:400

            });



        })

}





// Удаление выбранных элементов из контейнера
function DeleteMembers(e) {

    var container_row = $("table[group=events] tbody tr[container=yes]").attr("row_id");
    var id = [];
    var i = $("table[group=events] tbody tr[group=members] td input:checked").not("[container=yes]");
    $.each( i, function( key, value ) {
        id.push($(value).closest("tr").attr("row_id"));
    });


    var data = {};
    data.delgroup = id;
    data.container_row = container_row;
    data.action = "delgroup";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });



    $.ajax({
      url: "/monitor/events/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {

            GetMemebersContainer();
            ShowMembersCount();

        }

    });



}







function ShowMembersCount() {
     $("info").text("Группировка "+$("table[group=events] tbody tr[group=members] td input").length+" элементов");
}












// Добавление в группировку
function AddContainer(e) {

    var container_row = $("table[group=events] tbody tr[container=yes]").attr("row_id");
    var id = []
    var row_list = $("table[group=events] tbody tr[group=true]").not("[container=yes]");
    $.each( row_list, function( key, value ) {
        id.push($(value).attr("row_id"));
    });


    var data = {};
    data.addgroup = id;
    data.container_row = container_row;
    data.action = "addgroup";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });



    $.ajax({
      url: "/monitor/events/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {

            // Скрываем добавленные события из общего списка
            $.each( row_list, function( key, value ) {
                $(value).hide();
            });
            GetMemebersContainer();
            ShowMembersCount();

        }

    });


}








function GetMemebersContainer() {

    var row_id = $("table[group=events] tbody tr[container=yes]").attr("row_id");

    var jqxhr = $.getJSON("/monitor/events/jsondata?container_row="+row_id+"&getmembers=ok",
        function(data) {
            $("table tr[group=members]").empty();
            data['members'].forEach(function(item,i,arr){

                var icon = "";

                if (item["byhand"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-user\" aria-hidden=\"true\"></span>"; }
                if (item["agregator"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-align-justify\" aria-hidden=\"true\"></span>"; }
                if (item["bymail"] == "yes") { icon = icon + "<span class=\"glyphicon glyphicon-envelope\" aria-hidden=\"true\"></span>"; }


                var t = "<tr group=members style=\"background-color:#F5DEB3;\" class=\"small\" row_id=\""+item["id"]+"\" marked=\"no\" bymail=\""+item["bymail"]+"\" >"
                +"<td>"+icon+"</td>"
                +"<td><input type=\"checkbox\" class=\"input\"></td>"
                +"<td>"+item['last_seen']+"</td>"
                +"<td>"+item['first_seen']+"</td>"
                +"<td>"+item['field0']+"</td>"
                +"<td>"+item['field1']+"</td>"
                +"<td>"+item['field2']+"</td>"
                +"<td>"+item['field3']+"</td>"
                +"<td>"+item['field4']+"</td>"
                +"<td>"+item['field5']+"</td>"
                +"<td>"+item['field6']+"</td>"
                +"<td>"+item['field7']+"</td>"
                +"<td>"+item['field8']+"</td>"
                +"<td>"+item['field9']+"</td>"
                +"<td>"+item['field10']+"</td>"
                +"<td>"+item['field11']+"</td>"
                +"</tr>";

                $("table[group=events] tbody tr[marked=yes]").after(t);

            });

        ShowMembersCount();
        $("table[group=events]").attr("refresh","no");
        // Исправление заголовков таблицы
        //FixTableHead();


        })


}








function ShowContainer(e) {



    $("table[group=events] tbody tr").unbind("click",ClickEventRow);
    // Отметка контейнера
    $("table[group=events] tbody tr[marked=yes]").attr("container","yes");

    // Сброс отметки строки
    $("table[group=events] tbody tr").css("background-color","");
    $("table[group=events] tbody tr").attr("marked","no");

    var row_id = $(this).closest("tr").attr("row_id");

    $("#mark-all").show();

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

    // Снятие отметки контейнера
    $("table[group=events] tbody tr[container=yes]").attr("container","no");

    var row_id = $("table[group=events] tbody tr[marked=yes]").attr("row_id");
    $(this).prev("div.dropdown").show();
    $("ul.dropdown-menu li a[action=container]").bind("click",ShowContainer);

    $("table[group=events] tbody tr td input").hide();
    $("table[group=events] tbody tr td a[container_hide="+row_id+"]").hide();

    $("table[group=events] tbody tr[row_id="+row_id+"]").attr("marked","no");
    $("table[group=events] tbody tr[row_id="+row_id+"]").css("background-color","").css("color","");

    $("table[group=events] tbody tr").bind("mouseenter",EnterRow);
    $("table[group=events] tbody tr").bind("mouseleave",LeaveRow);

    $("#mark-all").hide();


    // Исправление заголовков таблицы
    //FixTableHead();
    $("table[group=events]").attr("refresh","yes");

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




// Фильтр по авариям
function FilterAccident(e) {

    var jqxhr = $.getJSON("/monitor/events/jsondata?filteraccident=ok",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}



// Фильтр по архивным событиям
function FilterHistory(e) {

    var jqxhr = $.getJSON("/monitor/events/jsondata?filterhistory=ok",
        function(data) {
            window.location=$("#menumonitor a").attr("href");
        })

}