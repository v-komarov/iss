$(document).ready(function() {


    $("#addrow").bind("click",AddRow);
    $("#editrow").bind("click",EditRow);
    $("table[group=agregators] tbody tr").bind("click",ClickEventRow);
    $("#clearsearch").bind("click",ClearSearch);
    $("#runsearch").bind("click",RunSearch);




    //// Валидация
    $("#agregatorform").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            ipaddress: {
                required: true,
                minlength: 7,
                maxlength: 15
            },
            sysdescr: {
                required: true,
                minlength: 5,
                maxlength: 100
            },
            sysname: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            syslocation: {
                required: true,
                minlength: 5,
                maxlength: 100
            },
            serial: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
            mac: {
                required: true,
                minlength: 5,
                maxlength: 30
            },
          },

    });// Валидация


    $("#agregatorform table tbody tr td input").change(function(e) {
        $("#agregatorform").validate().element($(e.target));
    });







    $('table[group=agregators]').tableScroll({height:800});

    $("#editrow").hide();


});










// Выделение строки
function ClickEventRow(e) {

        $("table[group=agregators] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=agregators] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#editrow").show();

}




// Поиск
function RunSearch(e) {
    console.log("working");
    var search = $("#search").val();
    var jqxhr = $.getJSON("/equipment/devices/jsondata?search="+search,
        function(data) {
            window.location=$("#menuagregators a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search").val("");
    $("#search").attr("placeholder","");

    var search = "xxxxx";
    var jqxhr = $.getJSON("/equipment/devices/jsondata?search="+search,
        function(data) {
            window.location=$("#menuagregators a").attr("href");
        })
}





function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





// Добавить агрегатор
function AddRow(e) {

    $("#editagregator").attr("action","create_agregator");
    $("#editagregator").attr("agregator-id","");

    $("#agregatorform table tbody tr td input#ipaddress").val("");
    $("#agregatorform table tbody tr td input#sysname").val("");
    $("#agregatorform table tbody tr td input#sysdescr").val("");
    $("#agregatorform table tbody tr td input#syslocation").val("");
    $("#agregatorform table tbody tr td input#serial").val("");
    $("#agregatorform table tbody tr td input#mac").val("");
    $("#agregatorform table tbody tr td select#domen").val("");
    $("#agregatorform table tbody tr td select#footnode").val("");

    RowData();

}





// Редактировать агрегатор
function EditRow(e) {

    var row_id = $("table[group=agregators] tbody tr[marked=yes]").attr("row_id");
    $("#editagregator").attr("action","edit_agregator");
    $("#editagregator").attr("footnode-id",row_id);

    var jqxhr = $.getJSON("/equipment/devices/jsondata?agnode="+row_id,
        function(data) {

            $("#agregatorform table tbody tr td input#ipaddress").val(data["result"]["ipaddress"]);
            $("#agregatorform table tbody tr td input#sysname").val(data["result"]["name"]);
            $("#agregatorform table tbody tr td input#sysdescr").val(data["result"]["descr"]);
            $("#agregatorform table tbody tr td input#syslocation").val(data["result"]["location"]);
            $("#agregatorform table tbody tr td input#serial").val(data["result"]["serial"]);
            $("#agregatorform table tbody tr td input#mac").val(data["result"]["mac"]);
            $("#agregatorform table tbody tr td select#domen").val(data["result"]["domen"]);

            RowData();

        })

}







function RowData() {


    $("#editagregator").dialog({
        title:"Агрегатор",
        buttons:[{ text:"Сохранить",click: function() {
            if ($('#ipaddress').valid() && $('#sysname').valid() && $('#sysdescr').valid() && $('#syslocation').valid() && $('#serial').valid() && $('#mac').valid()) {
                var ipaddress = $("#footnodeform table tbody tr td input#ipaddress").val();
                var name = $("#footnodeform table tbody tr td input#sysname").val();
                var descr = $("#footnodeform table tbody tr td input#sysdescr").val();
                var location = $("#footnodeform table tbody tr td input#syslocation").val();
                var serial = $("#footnodeform table tbody tr td input#serial").val();
                var mac = $("#footnodeform table tbody tr td input#mac").val();
                var domen = $("#footnodeform table tbody tr td select#domen").val();
                var domen = $("#footnodeform table tbody tr td select#footnode").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });


                var row_id = ""
                var action = $("#editagregator").attr("action");
                if ($("#editagregator").attr("action") == "edit_agregator") {
                    var row_id = $("#editagregator").attr("agregator-id");
                }

                $.ajax({
                  url: "/equipment/devices/jsondata/",
                  type: "POST",
                  dataType: 'text',
                  data:"{"
                    +"'row_id':'"+row_id+"',"
                    +"'action':'"+action+"',"
                    +"'ipaddress':'"+ipaddress+"',"
                    +"'name':'"+name+"',"
                    +"'descr':'"+descr+"',"
                    +"'location':'"+location+"',"
                    +"'serial':'"+serial+"',"
                    +"'mac':'"+mac+"',"
                    +"'domen':'"+domen+"'"
                    +"}",
                    success: function(result) {
                        window.location=$("#menufootnodes a").attr("href");
                    }

                })

            }

        }},

            // Получение данных snmp
            {text:"snmp",click: function() {


                if ($('#ipaddress').valid()) {

                        var jqxhr = $.getJSON("/equipment/devices/jsondata?getdevice="+$("#ipaddress").val()+"&domen="+$("#domen").val(),
                        function(data) {
                            if (data["result"] != "error") {
                                    $("#agregatorform table tbody tr td input#sysname").val(data["result"]["sysname"]);
                                    $("#agregatorform table tbody tr td input#sysdescr").val(data["result"]["sysdescr"]);
                                    $("#agregatorform table tbody tr td input#syslocation").val(data["result"]["syslocation"]);
                                    $("#agregatorform table tbody tr td input#serial").val(data["result"]["serial"]);
                                    $("#agregatorform table tbody tr td input#mac").val(data["result"]["mac"]);
                            }

                        })

                }

            }},

            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600

    });

}

