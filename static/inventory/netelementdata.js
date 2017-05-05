$(document).ready(function() {


    // Поиск устройства
    $("#searchdevice").autocomplete({
        source: "/inventory/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#devices',
        position: 'top',
        select: function (event,ui) {
            $("#searchdevice").val(ui.item.label);
            window.device_id = ui.item.value;
            window.device_label = ui.item.label;

            return false;
        },
        focus: function (event,ui) {
            $("#searchdevice").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    })




    // Добавление устройства
    $("#adddevice").bind("click",AddDevice);
    // Очистить поиск устройства
    $("#clear").bind("click",DeviceClear);
    // Сохранение названия сетевого элемента
    $("#saveelem").bind("click",SaveElemName);
    // Удаление устройства
    $("table[group=devices] tbody").on("click","a",DelDevice);
    // Добавление логического интерфейса
    $("#addinterface").bind("click",AddLogicalInterface);
    // Редактирование логического интерфейса
    $("table[group=interfaces] tbody").on("click","a[do=editinterface]",EditLogicalInterface);
    // Редактирование логического интерфейса
    $("table[group=interfaces] tbody").on("click","a[do=deleteinterface]",DeleteLogicalInterface);
    // Добавление свойства логического интерфейса
    $("table[group=interfaces] tbody").on("click","a[do=addproperties]",AddPropInterface);
    // Удаление свойства логического интерфейса
    $("table[group=interfaces] tbody").on("click","a[do=deleteprop]",DeleteProp);
    // Редактирование свойства логического интерфейса
    $("table[group=interfaces] tbody").on("click","a[do=editprop]",EditPropInterface);



    // Отображение названия элемента
    ShowElemName();

    // Список устройств
    ListDevice();

    // Данные по интерфейсам
    ListInterfacesData();


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




// Отображение названия сетевого элемента
function ShowElemName(e) {

    var jqxhr = $.getJSON("/inventory/jsondata?action=getelemname",
    function(data) {

        if (data["result"] == "ok") { $("#elem").val(data["name"]); }

    })

}





// Сохранение названия сетевого элемента
function SaveElemName(e) {

    var name = $("#elem").val();

    var jqxhr = $.getJSON("/inventory/jsondata?action=saveelemname&name="+name,
    function(data) {

        if (data["result"] == "ok") { alert("Название сохранено!");}

    })

}







// Добавление устройства
function AddDevice(e) {

    var jqxhr = $.getJSON("/inventory/jsondata?action=adddevice&deviceid="+window.device_id,
    function(data) {

        ListDevice();
        $("#searchdevice").val("");
        window.device_id = 0;
        window.device_label = "";


    })

}





// Удаление устройства
function DelDevice(e) {

    var device_id = $(this).parent("td").parent("tr").attr("device_id");
    var device_name = $(this).closest("tr").children("td").eq(0).text();
    var a = confirm("Удаляем "+device_name+" ?");

    if (a) {

        var jqxhr = $.getJSON("/inventory/jsondata?action=deldevice&deviceid="+device_id,
        function(data) {

            if (data["result"] == "ok") { ListDevice();}

        })

    }

}






// Список устройств
function ListDevice(e) {

    var jqxhr = $.getJSON("/inventory/jsondata?action=listdevice",
    function(data) {

        if (data["result"] == "ok") {

            // устройства
            $("table[group=devices] tbody").empty();
            $.each(data["device_list"], function(key,value) {


                var t = "<tr device_id=" + value["id"] +">"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['serial']+"</td>"
                +"<td>"+value['address_city']+" "+value['address_street']+" "+value['address_house']+"</td>"
                +"<td class=\"text-center\"><a title=\"Удалить устройство\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=devices] tbody").append(t);

            });



        }

    })

}




// Данные по логическим интерфейсам
function ListInterfacesData() {

    var jqxhr = $.getJSON("/inventory/jsondata?action=interfacedata",
    function(data) {

        if (data["result"] == "ok") {

            // устройства
            $("table[group=interfaces] tbody").empty();
            $.each(data["interfaces_list"], function(key,value) {

                // Формирование отображения названия устройства и портов
                var devices = "";
                var ports = "";
                for (var i in value["devices_ports"]) {
                    devices = devices + value["devices_ports"][i]["device"] + "<br>";
                    ports = ports + value["devices_ports"][i]["num"] + " " + value["devices_ports"][i]["port"] + "<br>";
                }

                // Данные по интерфейсам
                var t = "<tr interface_id=" + value["interface_id"] +">"
                +"<td>"+value['interface_name']+"</td>"
                +"<td>"+value['interface_comment']+"</td>"
                +"<td>"+devices+"</td>"
                +"<td>"+ports+"</td>"
                +"<td></td>"
                +"<td></td>"
                +"<td></td>"
                +"<td class=\"text-center\"><a do=\"addproperties\" title=\"добавить свойство\"><span class=\"glyphicon glyphicon-plus\" aria-hidden=\"true\"></span></a></td>"
                +"<td class=\"text-center\"><a do=\"editinterface\" title=\"редактировать интерфейс\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                +"<td class=\"text-center\"><a do=\"deleteinterface\" title=\"удалить интерфейс\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=interfaces] tbody").append(t);

                // Формирование отображения свойств логического интерфейса
                $.each(value["props"], function(k,v) {
                    var tt = "<tr interface_id=" + v["interface_id"] + " prop_id=" + v["prop_id"] + " prop_select_id=" +v["prop_select_id"]+">"
                    +"<td></td>"
                    +"<td></td>"
                    +"<td></td>"
                    +"<td></td>"
                    +"<td>"+v["prop_name"]+"</td>"
                    +"<td>"+v["prop_val"]+"</td>"
                    +"<td>"+v["prop_comment"]+"</td>"
                    +"<td></td>"
                    +"<td class=\"text-center\"><a do=\"editprop\" title=\"редактировать свойство\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                    +"<td class=\"text-center\"><a do=\"deleteprop\" title=\"удалить свойство\"><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                    +"</tr>";

                    $("table[group=interfaces] tbody").append(tt);

                });

            });

        }

    })


}






// Очистка строки поиска
function DeviceClear(e) {

    $("#searchdevice").val("");
    window.device_id = 0;
    window.device_label = "";

}







// Удаление логического интерфейса
function DeleteLogicalInterface(e) {


    var interface_id = $(this).closest("tr").attr("interface_id");
    var interface_name = $(this).closest("tr").children("td").eq(0).text();
    var a = confirm("Удаляем интерфейс "+interface_name+" ?");

    if (a) {

        var jqxhr = $.getJSON("/inventory/jsondata?action=deleteinterface&interface_id="+interface_id,
        function(data) {

            if (data["result"] == "ok") { ListInterfacesData();}

        })
    }
}






// Добавление логического интерфейса
function AddLogicalInterface(e) {

    $("#logicalinterface").attr("action","createinterface");
    $("#logicalinterface").attr("interface-id","");
    $("#nameinterface").val("");
    $("#commentinterface").val("");

    var jqxhr = $.getJSON("/inventory/jsondata?action=interfaceform",
    function(data) {

        if (data["result"] == "ok") {

            // список портов
            $("table[group=devices-ports] tbody").empty();
            $.each(data["ports_list"], function(key,value) {


                var t = "<tr port_id=" + value["port_id"] +">"
                +"<td>"+value['device_name']+"</td>"
                +"<td>"+value['device_status']+"</td>"
                +"<td>"+value['port_num']+"</td>"
                +"<td>"+value['port']+"</td>"
                +"<td>"+value['port_status']+"</td>"
                +"<td><input port_id="+value["port_id"]+" type=\"checkbox\"></></td>"
                +"</tr>";

                $("table[group=devices-ports] tbody").append(t);

            });



        }

    })


    LogicalInterfaceData();



}





// Редактирование логичсекого интерфейса
function EditLogicalInterface(e) {


    // id записи логического интерфейса
    var interface_id = $(this).closest("tr").attr("interface_id");


    $("#logicalinterface").attr("action","editinterface");
    $("#logicalinterface").attr("interface-id",interface_id);


    // Получение данные по названию интерфейса, коментария, массива выбранных (связанных) портов
    var jqxhr = $.getJSON("/inventory/jsondata?action=interfaceform2&interface_id="+interface_id,
    function(data) {

        if (data["result"] == "ok") {

            $("#nameinterface").val(data["name"]);
            $("#commentinterface").val(data["comment"]);

            $("table[group=devices-ports] tbody tr td input:checkbox").prop("checked",false);
            // список портов
            $("#logicalinterface").attr("ports_list",data["ports_list"]);

        }

    })



    var jqxhr = $.getJSON("/inventory/jsondata?action=interfaceform",
    function(data) {

        if (data["result"] == "ok") {

            // список портов
            $("table[group=devices-ports] tbody").empty();
            $.each(data["ports_list"], function(key,value) {

                // Поиск в отмеченных портах ... checked or not
                if (($.inArray(parseInt(value["port_id"],10),eval("["+$("#logicalinterface").attr("ports_list")+"]"))) == -1) { var checkb = "<td><input port_id="+value["port_id"]+" type=\"checkbox\"></></td>";}
                else { var checkb = "<td><input port_id="+value["port_id"]+" type=\"checkbox\" checked></></td>"; }

                var t = "<tr port_id=" + value["port_id"] +">"
                +"<td>"+value['device_name']+"</td>"
                +"<td>"+value['device_status']+"</td>"
                +"<td>"+value['port_num']+"</td>"
                +"<td>"+value['port']+"</td>"
                +"<td>"+value['port_status']+"</td>"
                +checkb
                +"</tr>";

                $("table[group=devices-ports] tbody").append(t);

            });

        }

    })



    LogicalInterfaceData();

}





// Наполнение данными диалога интерфейса
function LogicalInterfaceData() {



    $("#logicalinterface").dialog({
        title:"Логический интерфейс",
        buttons:[{ text:"Сохранить",click: function() {
        $(this).dialog("destroy");
            if ($("#nameinterface").val().length != 0) {

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                var port_id = [];
                var chbox = $("table[group=devices-ports] tbody td input");
                chbox.each(function(i,elem) {

                    if ($(elem).is(":checked")) {
                        port_id.push(parseInt($(elem).attr("port_id")));
                    }

                });

                var data = {};
                data.name = $("#nameinterface").val();
                data.comment = $("#commentinterface").val();
                data.action = $("#logicalinterface").attr("action");
                data.interfaceid = $("#logicalinterface").attr("interface-id");
                data.ports = port_id;

                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "error") {
                            alert("Возможно интерфейс\nс таким именем уже существует!");
                        }

                    $("#logicalinterface").hide();
                    // Обновление данных по интерфейсах
                    ListInterfacesData();

                    }

                });

            }
            else { alert("Необходимо задать название!");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:600,
        width:800,
        height:500

    });


}





// Добавление свойства логического интерфейса
function AddPropInterface(e) {

    var interface_id = $(this).closest("tr").attr("interface_id");
    $("#interfaceprop").attr("interface_id",interface_id);
    $("#interfaceprop").attr("action","createprop");
    $("#interfaceprop").attr("prop_id","");

    $("form#interfacepropform table tbody tr td input#value").val("");
    $("form#interfacepropform table tbody tr td input#comment").val("");

    PropInterfaceData();

}






// Изменение свойства логического интерфейса
function EditPropInterface(e) {

    var interface_id = $(this).closest("tr").attr("interface_id");
    var prop_id = $(this).closest("tr").attr("prop_id");
    var select_id = $(this).closest("tr").attr("prop_select_id");
    $("#interfaceprop").attr("interface_id",interface_id);
    $("#interfaceprop").attr("action","editprop");
    $("#interfaceprop").attr("prop_id",prop_id);


    var prop_val = $(this).closest("tr").children("td").eq(5).text();
    var prop_comment = $(this).closest("tr").children("td").eq(6).text();
    $("form#interfacepropform table tbody tr td select#prop").val(select_id);
    $("form#interfacepropform table tbody tr td input#value").val(prop_val);
    $("form#interfacepropform table tbody tr td input#comment").val(prop_comment);

    PropInterfaceData();

}







// Наполнение данными свойства логического интерфейса
function PropInterfaceData() {



    $("#interfaceprop").dialog({
        title:"Свойство интерфейса",
        buttons:[{ text:"Сохранить",click: function() {

            if ($("form#interfacepropform table tbody tr td select#prop").val() ) {


                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                var data = {};
                data.interface_id = $("#interfaceprop").attr("interface_id");
                data.prop_id = $("#interfaceprop").attr("prop_id");
                data.prop = $("form#interfacepropform table tbody tr td select#prop").val();
                data.value = $("form#interfacepropform table tbody tr td input#value").val();
                data.comment = $("form#interfacepropform table tbody tr td input#comment").val();
                data.action = $("#interfaceprop").attr("action");


                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok")
                        { $("#interfaceprop").dialog("close");  ListInterfacesData(); }
                    }

                });

            }
            else { alert("Необходимо заполнить поля *");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:200,
        width:310,
        minHeight:200,

    });


}




// Удаление свойства логического интерфейса
function DeleteProp(e) {


    var prop_id = $(this).closest("tr").attr("prop_id");
    var prop_name = $(this).closest("tr").children("td").eq(4).text();
    var a = confirm("Удаляем свойство "+prop_name+" ?");

    if (a) {

        var jqxhr = $.getJSON("/inventory/jsondata?action=deleteprop&prop_id="+prop_id,
        function(data) {

            if (data["result"] == "ok") { ListInterfacesData();}

        })
    }
}
