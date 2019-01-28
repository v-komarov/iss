$(document).ready(function() {


    $("a#new-device").bind("click", NewDevice);

    $( "select#id_filter_d").change(function() {
        Search_d();
    });

    $( "select#id_filter_p").change(function() {
        Search_p();
    });


    $("select#id_filter_d").val($("dl#search_d").attr("value"));
    $("select#id_filter_p").val($("dl#search_p").attr("value"));

});





// Поиск / фильтр
function Search_d(e) {


    var search = $("select#id_filter_d").val();

    var jqxhr = $.getJSON("/electro/jsondata/?action=filter-deviceslist-d&search="+search,
    function(data) {

        if (data["result"] == "ok") { location.href="/electro/deviceslist/1/"; }

    })

}



// Поиск / фильтр
function Search_p(e) {


    var search = $("select#id_filter_p").val();

    var jqxhr = $.getJSON("/electro/jsondata/?action=filter-deviceslist-p&search="+search,
    function(data) {

        if (data["result"] == "ok") { location.href="/electro/deviceslist/1/"; }

    })

}






// Создание нового устройства
function NewDevice() {

    var jqxhr = $.getJSON("/electro/jsondata/?action=create-device",
    function(data) {
        console.log(data);
        if (data["result"] == "ok") { window.open("/electro/editdevice/"+data['id']+"/", '_blank'); }

    })


}