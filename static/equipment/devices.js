$(document).ready(function() {

    $("table tbody tr td a").bind("click",SaveRowData);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);
    $("#access-error").bind("click",FilterNotAccess);
    $("#no-rewrite").bind("click",FilterNoRewrite);

    $('table[group=devices]').tableScroll({height:700});

    // Зебра
    zebra = "#FFF5EE"
    $("table[group=devices] tbody tr:odd").css("background-color",zebra)


});






function SaveRowData(e) {
    var row_id = $(this).attr("row-id");
    var tr = $(this).closest("tr");
    var serial = tr.find("input").eq(0).val();
    var mac = tr.find("input").eq(1).val();
    var readonly = tr.find("input").eq(2).prop("checked");

    var jqxhr = $.getJSON("/equipment/devices/jsondata?saverow=ok&rowid="+row_id+"&serial="+serial+"&mac="+mac+"&readonly="+readonly,
        function(data) {

            if (data["result"] == "ok") {

                $("#dialog-row-save").dialog({

                      show: {
                        effect: "blind",
                        duration: 100
                      },
                      hide: {
                        effect: "blind",
                        duration: 3000
                      }
                });

                $("#dialog-row-save").dialog("close");
                //setTimeout( $("#dialog-row-save").dialog("close"), 5000 );

            }

        })
}







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

