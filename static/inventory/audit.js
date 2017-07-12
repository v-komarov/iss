$(document).ready(function() {


    // Освежить данные
    $("#getdevices").bind("click", GetDevices);

    // Редактировать устройства
    $("table[group=audit] tbody tr td a[device]").bind("click",DeviceEdit);

    // Редактировать сетевые элементы
    $("table[group=audit] tbody tr td a[netelem]").bind("click",NetelemEdit);


    // Поиск адреса
    $("#address").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#page-audit',
        position: 'top',
        select: function (event,ui) {
            $("#address").val(ui.item.label);
            window.address_id = ui.item.value;
            window.address_label = ui.item.label;

            return false;
        },
        focus: function (event,ui) {
            $("#address").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    })





});




// Запрос списка устройств по адресу
function GetDevices(e) {

    // Окно сообщения о загрузке
    $("#loading").dialog({show: { effect: "blind", duration: 100 }});


    var jqxhr = $.getJSON("/inventory/jsondata?action=get_devices_byaddress&address_id="+window.address_id+"&address_label="+window.address_label,
        function(data) {
            console.log(data);

            window.location=$("#menuauditports a").attr("href");
        })

}




// Редактирование устройства
function DeviceEdit(e) {

    var device_id = $(this).attr("device");
    var jqxhr = $.getJSON("/inventory/jsondata?dev_id="+device_id+"&action=savedevid",
    function(data) {
        if (data["result"] == "ok")

        win = window.open("/inventory/devicedata/","device");

    });


}




// Редактирование сетевого элемента
function NetelemEdit(e) {

    var netelem_id = $(this).attr("netelem");
    var jqxhr = $.getJSON("/inventory/jsondata?savenetelem="+netelem_id,
    function(data) {
        win2 = window.open("/inventory/netelementdata/","netelem");

    })

}

