$(document).ready(function() {


    // Освежить данные
    $("#getdevices").bind("click", GetDevices);



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
    var jqxhr = $.getJSON("/inventory/jsondata?action=get_devices_byaddress&address_id="+window.address_id+"&address_label="+window.address_label,
        function(data) {
            console.log(data);
            window.location=$("#menuauditports a").attr("href");
        })
}



