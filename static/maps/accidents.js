$(document).ready(function() {

    // Сброс значений выбранного города
    $("#select-cities").val("0");

    //$("table[group=accidents] tbody tr td a").bind("click",ShowAccident);
    $("td").bind("click",ShowAccident);


    // Выбор города
    $( "#select-cities" ).change(function() {

        GetGeoCity();

    });



    // Сброс значений выбора для варий
    $("table[group=accidents] tbody tr").css("background-color","");
    $("table[group=accidents] tbody tr").attr("chosen","no");



$('table[group=accidents]').tableScroll({height:600});

});






// Показать аварии на карте
function ShowAccident(e) {

    // Окно сообщения о загрузке
    $("#loading").dialog({show: { effect: "blind", duration: 100 }});


    var partr = $(this).parent("tr");
    var acc_id = partr.children("td").eq(0).text();
    var status = partr.attr("chosen");

    // Что то делаем если город выбран (отображен на карте)
    if ( $("#select-cities").val() != "0" && status == "no" ) {

        var jqxhr = $.getJSON("/maps/jsondata/?action=get_accident_geo&acc_id="+acc_id,
            function(data) {

            console.log(data);

            // Обход набора координат
            $.each(data["address_list"], function(key,value) {


                // Создание метки
                 point = new ymaps.Placemark([value["lat"], value["lng"]],
                 {
                    iconContent: data["acc_id"],
                    hintContent: data["acc_reason"],
                    balloonContentBody: value["city"] + ", " + value["street"] + " " + value["house"]
                 },

                 {
                        preset: 'islands#redStretchyIcon'
                 });

                // Размещение на карте
                 window.map.geoObjects.add(point);

            });

            partr.attr("chosen","yes");
            partr.css("background-color","#F0E68C");

        })

    }


    // Окно сообщения о загрузке
    $("#loading").dialog('close');


}







// Получение координат выбранного города или населенного пункта
function GetGeoCity() {

    // Окно сообщения о загрузке
    $("#loading").dialog({show: { effect: "blind", duration: 100 }});

    var city_id = $("#select-cities").val();

    // Сброс значений выбора для варий
    $("table[group=accidents] tbody tr").css("background-color","");
    $("table[group=accidents] tbody tr").attr("chosen","no");



    var jqxhr = $.getJSON("/maps/jsondata/?action=get_city_geo&city_id="+city_id,
        function(data) {



            // Отрисовка карты
            if (window.map) { window.map.destroy(); }

                ymaps.ready(function(){
                            window.map = new ymaps.Map("accident-map", {
                            center: [data["lat"], data["lng"]],
                            zoom: 12,
                            type:'yandex#map',
                            controls:['zoomControl','rulerControl','typeSelector','fullscreenControl']
                            });

                });


        })

    // Окно сообщения о загрузке
    $("#loading").dialog('close');


}


