$(document).ready(function() {

    // Сброс значений выбранного города
    $("#select-cities").val("0");


    // Выбор города
    $( "#select-cities" ).change(function() {

        GetGeoCity();

    });



});











// Получение координат выбранного города или населенного пункта
function GetGeoCity() {

    // Окно сообщения о загрузке
    $("#loading").dialog({show: { effect: "blind", duration: 100 }});

    var city_id = $("#select-cities").val();


    var jqxhr = $.getJSON("/maps/jsondata/?action=get-devices-distance&city_id="+city_id,
        function(data) {

            // Отрисовка карты
            if (window.map) { window.map.destroy(); }

                window.map = ymaps.ready(function(){
                            window.map = new ymaps.Map("ports-map", {
                            center: [data["lat"], data["lng"]],
                            zoom: 12,
                            type:'yandex#map',
                            controls:['zoomControl','rulerControl','typeSelector','fullscreenControl']
                            });



                                // Обход устройст
                                $.each(data["devices"], function(key,value) {


                                    // Если данные по количеству портов есть
                                    if (value["ports_information"]["result"] == "ok") {

                                        // Последнее значение используемое количестов портов
                                        var newports = parseInt(value["ports_information"]["newports"], 10);

                                        // Прошлое значение используемое количестов портов
                                        var oldports = parseInt(value["ports_information"]["oldports"], 10);


                                        // Что в кружочке
                                        var icon_content = value["ports_information"]["newports"];


                                        var body = "Модель: " + value["device"] + "<br>"
                                        + "Адрес: " + value["address"] + "<br>"
                                        + "Порты (исп.): " + value["ports_information"]["newports"] + " (" +value["ports_information"]["newdate"] + ")<br>"
                                        + "Порты (исп.) за прошлый период: " + value["ports_information"]["oldports"] + " (" +value["ports_information"]["olddate"] + ")<br>"
                                        ;

                                        // Возросло использование портов или нет
                                        if (newports > oldports) { var preset = 'islands#greenStretchyIcon'; }
                                        else { var preset = 'islands#redStretchyIcon'; }
                                        if (newports == oldports) { var preset = 'islands#brownStretchyIcon';}

                                    }
                                    // Если данные не начитались
                                    else {

                                        // Определение стиля - нет данных по портам
                                        var preset = 'islands#blackStretchyIcon';

                                        // Что в кружочке
                                        var icon_content = "";

                                        var body = "Модель: " + value["device"] + "<br>"
                                        + "Адрес: " + value["address"]
                                        ;
                                    }





                                    // Создание метки
                                     point = new ymaps.Placemark([value["lat"], value["lng"]],
                                     {
                                        iconContent: icon_content,
                                        hintContent: value["ip"],
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






        })



}


