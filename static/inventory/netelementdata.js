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

    // Отображение названия элемента
    ShowElemName();

    // Список устройств
    ListDevice();




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

            // история перемещений устройства
            $("table[group=devices] tbody").empty();
            $.each(data["device_list"], function(key,value) {


                var t = "<tr device_id=" + value["id"] +">"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['serial']+"</td>"
                +"<td>"+value['address_city']+" "+value['address_street']+" "+value['address_house']+"</td>"
                +"<td class=\"text-center\"><a><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=devices] tbody").append(t);

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