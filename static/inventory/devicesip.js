$(document).ready(function() {

    SearchIp();


});



function SearchIp() {

    var ip = prompt('Поиск по ip адресу', '');

    if (ip) {

        // Определение ip первого в списке устройства
        var jqxhr = $.getJSON("/inventory/jsondata?action=searchdeviceip&ip="+ip,
        function(data) {

            if (data["result"] == "ok") {

                location.href = "/inventory/devicedata/"+data['dev_id'];


            }

            else { alert("Устройство не найдено."); }

        })


    }

}