$(document).ready(function() {


    // Добавить адрес
    $("#getaddress").bind("click", SetAddress);

    // Добавить IP
    $("#getip").bind("click", SetIP);

    // Очистить список
    $("#clear").bind("click",ClearZKL);


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




// Добавление устройств по адресу
function SetAddress(e) {
    var jqxhr = $.getJSON("/monitor/events/jsondata/?action=set_zkl_address&address_id="+window.address_id,
        function(data) {

            if (data["result"] == "OK") {

                $("#address").val("");
                GetZklDevices();
            }

        })
}


// Добавление устройств по IP
function SetIP(e) {
    var ip = $("input#ipaddress").val();
    var jqxhr = $.getJSON("/monitor/events/jsondata/?action=set_zkl_ip&ip="+ip,
        function(data) {

            if (data["result"] == "OK") {

                $("input#ipaddress").val("");
                GetZklDevices();
            }



        })

}


// Очистить список устройств ЗКЛ
function ClearZKL(e) {
    var jqxhr = $.getJSON("/monitor/events/jsondata/?action=clear_zkl_devices",
        function(data) {

            $("table[group=devices-zkl] tbody").empty();

        })
}



function GetZklDevices() {
    var jqxhr = $.getJSON("/monitor/events/jsondata/?action=get_zkl_devices",
        function(data) {

        //console.log(data);

            var ports = 0;
            var use_ports = 0;
            var reserv_ports = 0;
            var tech_ports = 0;
            var combo = 0;
            var use_combo = 0;
            var reserv_combo = 0;
            var tech_combo = 0;


            // Отображение данных таблицы
            $("table[group=devices-zkl] tbody").empty();
            $.each(data, function(key,value) {


                var t = "<tr>"
                +"<td>"+value['device_address']+"</td>"
                +"<td>"+value['device_model']+"</td>"
                +"<td>"+value['device_serial']+"</td>"
                +"<td>"+value['device_netelems']+"</td>"
                +"<td>"+value['device_ip']+"</td>"
                +"<td>"+value['device_ports']+"</td>"
                +"<td>"+value['device_use_ports']+"</td>"
                +"<td>"+value['device_reserv_ports']+"</td>"
                +"<td>"+value['device_tech_ports']+"</td>"
                +"<td>"+value['device_combo']+"</td>"
                +"<td>"+value['device_use_combo']+"</td>"
                +"<td>"+value['device_reserv_combo']+"</td>"
                +"<td>"+value['device_tech_combo']+"</td>"
                +"</tr>";

                $("table[group=devices-zkl] tbody").append(t);


                ports = ports + value['device_ports'];
                use_ports = use_ports + value['device_use_ports'];
                reserv_ports = reserv_ports + value['device_reserv_ports'];
                tech_ports = tech_ports + value['device_tech_ports'];
                combo = combo + value['device_combo'];
                use_combo = use_combo + value['device_use_combo'];
                reserv_combo = reserv_combo + value['device_reserv_combo'];
                tech_combo = tech_combo + value['device_tech_combo'];


            });


                // Итоговые суммы
                var t2 = "<tr>"
                +"<td></td>"
                +"<td></td>"
                +"<td></td>"
                +"<td></td>"
                +"<td></td>"
                +"<td>"+ports+"</td>"
                +"<td>"+use_ports+"</td>"
                +"<td>"+reserv_ports+"</td>"
                +"<td>"+tech_ports+"</td>"
                +"<td>"+combo+"</td>"
                +"<td>"+use_combo+"</td>"
                +"<td>"+reserv_combo+"</td>"
                +"<td>"+tech_combo+"</td>"
                +"</tr>";

                $("table[group=devices-zkl] tbody").append(t2);




        })

}