$(document).ready(function() {

    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("#access-error").bind("click",FilterNotAccess);
    $("#no-rewrite").bind("click",FilterNoRewrite);

    $('table[group=devices]').tableScroll({height:700});

    // Зебра
    zebra = "#FFF5EE"
    $("table[group=devices] tbody tr:odd").css("background-color",zebra)


});



// Фильтр по устроистрам с проблемой доступа
function FilterNotAccess(e) {

    var jqxhr = $.getJSON("/equipment/devices/jsondata?notaccess=ok",
        function(data) {
            window.location=$("#menudevices a").attr("href");
        })

}


// Фильтр по устроистрам с no rewrite
function FilterNoRewrite(e) {

    var jqxhr = $.getJSON("/equipment/devices/jsondata?norewrite=ok",
        function(data) {
            window.location=$("#menudevices a").attr("href");
        })

}


// Поиск
function RunSearch(e) {
    console.log("working");
    var search = $("#search").val();
    var jqxhr = $.getJSON("/equipment/devices/jsondata?search="+search,
        function(data) {
            window.location=$("#menudevices a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/equipment/devices/jsondata?search="+search,
        function(data) {
            window.location=$("#menudevices a").attr("href");
        })
}

