$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Переход к данным устройства
    $("div#page-3 a[devices]").bind("click",DeviceData);


});




// Переход к интерфейсу устройства
function DeviceData(e) {

    var device_id = $(this).attr("device_id");
    var jqxhr = $.getJSON("/inventory/jsondata?dev_id="+device_id+"&action=savedevid",
    function(data) {
        if (data["result"] == "ok")

        win = window.open("/inventory/devicedata/","device");

    });


}





// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

