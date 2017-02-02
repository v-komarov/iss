$(document).ready(function() {


    $("#additem").bind("click",AddScheme);
    $("#edititem").bind("click",EditScheme);



});





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








// Добавить схему
function AddScheme(e) {

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
    $("#agregatorform table tbody tr td input#uplink").val("");

    $('#footnode option').each(function(){
        $(this).hide();
    });

    RowData();

}





// Редактировать схему
function EditScheme(e) {

    var row_id = $("table[group=agregators] tbody tr[marked=yes]").attr("row_id");
    $("#editagregator").attr("action","edit_agregator");
    $("#editagregator").attr("agregator-id",row_id);

    var jqxhr = $.getJSON("/equipment/devices/jsondata?agregator="+row_id,
        function(data) {

            $("#agregatorform table tbody tr td input#ipaddress").val(data["result"]["ipaddress"]);
            $("#agregatorform table tbody tr td input#sysname").val(data["result"]["name"]);
            $("#agregatorform table tbody tr td input#sysdescr").val(data["result"]["descr"]);
            $("#agregatorform table tbody tr td input#syslocation").val(data["result"]["location"]);
            $("#agregatorform table tbody tr td input#serial").val(data["result"]["serial"]);
            $("#agregatorform table tbody tr td input#mac").val(data["result"]["mac"]);
            $("#agregatorform table tbody tr td select#domen").val(data["result"]["domen"]);
            $("#agregatorform table tbody tr td select#footnode").val(data["result"]["footnode"]);
            $("#agregatorform table tbody tr td input#uplink").val(data["result"]["uplink"]);

            RowData();

        })

}







function RowData() {


    $("#editscheme").dialog({
        title:"Схема",
        buttons:[{ text:"Сохранить",click: function() {
            if ($('#ipaddress').valid() && $('#sysname').valid() && $('#sysdescr').valid() && $('#syslocation').valid() && $('#serial').valid() && $('#mac').valid() && $('#uplink').valid() && $("#domen").valid() && $("#footnode").valid()) {
                var ipaddress = $("#agregatorform table tbody tr td input#ipaddress").val();
                var name = $("#agregatorform table tbody tr td input#sysname").val();
                var descr = $("#agregatorform table tbody tr td input#sysdescr").val();
                var location = $("#agregatorform table tbody tr td input#syslocation").val();
                var serial = $("#agregatorform table tbody tr td input#serial").val();
                var mac = $("#agregatorform table tbody tr td input#mac").val();
                var domen = $("#agregatorform table tbody tr td select#domen").val();
                var footnode = $("#agregatorform table tbody tr td select#footnode").val();
                var uplink = $("#agregatorform table tbody tr td input#uplink").val();


                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                // Определение создание или редактирование
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
                    +"'domen':'"+domen+"',"
                    +"'footnode':"+footnode+","
                    +"'uplink':'"+uplink+"'"
                    +"}",
                    success: function(result) {
                        window.location=$("#menuagregators a").attr("href");
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




