$(document).ready(function() {


    $("#addrow").bind("click",AddRow);



    //// Валидация
    $("#footnodeform").validate({
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


    $("#footnodeform table tbody tr td input").change(function(e) {
        $("#footnodeform").validate().element($(e.target));
    });



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







// Добавить опорный узел
function AddRow(e) {

    $("#footnodeform table tbody tr td input#ipaddress").val("");
    $("#footnodeform table tbody tr td input#sysname").val("");
    $("#footnodeform table tbody tr td input#sysdescr").val("");
    $("#footnodeform table tbody tr td input#syslocation").val("");
    $("#footnodeform table tbody tr td input#serial").val("");
    $("#footnodeform table tbody tr td input#mac").val("");
    $("#footnodeform table tbody tr td select#domen").val("");

    $("#editfootnode").dialog({
        title:"Опорный узел",
        buttons:[{ text:"Сохранить",click: function() {
            if ($('#ipaddress').valid() && $('#sysname').valid() && $('#sysdescr').valid() && $('#syslocation').valid() && $('#serial').valid() && $('#mac').valid()) {
                var ipaddress = $("#footnodeform table tbody tr td input#ipaddress").val();
                var name = $("#footnodeform table tbody tr td input#sysname").val();
                var descr = $("#footnodeform table tbody tr td input#sysdescr").val();
                var location = $("#footnodeform table tbody tr td input#syslocation").val();
                var serial = $("#footnodeform table tbody tr td input#serial").val();
                var mac = $("#footnodeform table tbody tr td input#mac").val();
                var domen = $("#footnodeform table tbody tr td select#domen").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });



                $.ajax({
                  url: "/equipment/devices/jsondata/",
                  type: "POST",
                  dataType: 'text',
                  data:"{"
                    +"'action':'create_footnode',"
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
                                    $("#footnodeform table tbody tr td input#sysname").val(data["result"]["sysname"]);
                                    $("#footnodeform table tbody tr td input#sysdescr").val(data["result"]["sysdescr"]);
                                    $("#footnodeform table tbody tr td input#syslocation").val(data["result"]["syslocation"]);
                                    $("#footnodeform table tbody tr td input#serial").val(data["result"]["serial"]);
                                    $("#footnodeform table tbody tr td input#mac").val(data["result"]["mac"]);
                            }

                        })

                }

            }},

            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:500

    });

}

