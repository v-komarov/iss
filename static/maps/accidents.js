$(document).ready(function() {

    // Сброс значений выбранного города
    $("#select-cities").val("0");

    // Выбор города
    $( "#select-cities" ).change(function() {

        GetGeoCity();

    });


$('table[group=accidents]').tableScroll({height:600});

});





// Получение координат выбранного города или населенного пункта
function GetGeoCity() {

    var city_id = $("#select-cities").val();

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

}


