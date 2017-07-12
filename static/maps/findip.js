$(document).ready(function() {

    // Поиск оборудования по списку ip (через запятую)
    $("#find-ip-maps").bind("click",FindDevicesIP);


});



// Поиск оборудования
function FindDevicesIP(e) {

    // Окно сообщения о загрузке
    $("#loading").dialog({show: { effect: "blind", duration: 100 }});


        var ip_list = $("#ip-list").val();

        var jqxhr = $.getJSON("/maps/jsondata/?action=find_devices_ip&ip_list="+ip_list,
            function(data) {

            if (data["result"] == "empty") { alert("Поиск не дал результатов"); }

            if (data["result"] == "ok") {
                // очистка поля ввода
                $("#ip-list").val("");


                console.log(data);


                // Центр карты по первому устройству
                var lat = data["devices"][0]["lat"];
                var lng = data["devices"][0]["lng"];

                // Отрисовка карты
                if (window.map) { window.map.destroy(); }

                    ymaps.ready(function(){
                                window.map = new ymaps.Map("ip-map", {
                                center: [lat, lng],
                                zoom: 12,
                                type:'yandex#map',
                                controls:['zoomControl','rulerControl','typeSelector','fullscreenControl']
                                });





                                // Обход устройст
                                $.each(data["devices"], function(key,value) {

                                    var body = "Модель: " + value["model"] + "<br>"
                                    + "Статус: " + value["status"] + "<br>"
                                    + "Адрес: " + value["address"] + "<br>"
                                    + "Сетевой элемент: " + value["netelems"][0]["name"] + "<br>"
                                    + "ЗКЛ: " + value["zkl"]
                                    ;


                                    // Определение стиля метки исходя из аварийности на ip адресе
                                    if ( data["accidents_ip"].indexOf(value["ip"]) == -1 ) { var preset = 'islands#greenStretchyIcon'; }
                                    else { var preset = 'islands#redStretchyIcon'; }

                                    // Создание метки
                                     point = new ymaps.Placemark([value["lat"], value["lng"]],
                                     {
                                        iconContent: value["ip"],
                                        hintContent: value["model"],
                                        balloonContentBody: body
                                     },

                                     {
                                            preset: preset
                                     });

                                    // Размещение на карте
                                     window.map.geoObjects.add(point);

                                });




                        // Окно сообщения о загрузке
                        $("#loading").dialog('close');





                    });



            }

        });



}