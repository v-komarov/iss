$(document).ready(function() {

    // Для списка устройств
    //$("table[group=devices] tbody tr").bind("click",ClickEventRow);

    // Для интерфейса списка устройств
    $("#edititem").hide();

    //$("#edititem").bind("click",DeviceData);

    // Форма создания устройства
    $("#additem").bind("click",AddDevice);

    // Поиск
    $("#runsearch_device").bind("click",RunSearch);

    // Сброс поиска
    $("#clearsearch_device").bind("click",ClearSearch);



    // Поиск адреса
    $("#deviceaddress").autocomplete({
        source: "/monitor/events/jsondata",
        minLength: 1,
        delay: 1000,
        appendTo: '#createdevice',
        position: 'top',
        select: function (event,ui) {
            $("#deviceaddress").val(ui.item.label);
            window.address_id = ui.item.value;
            window.address_label = ui.item.label;

            return false;
        },
        focus: function (event,ui) {
            $("#deviceaddress").val(ui.item.label);
            return false;
        },
        change: function (event,ui) {
            return false;
        }


    })


});






// Поиск
function RunSearch(e) {
    var search = $("#search_device").val();
    var jqxhr = $.getJSON("/inventory/jsondata?search="+search,
        function(data) {
            window.location=$("#menu4devices a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("#search_device").val("");
    $("#search_device").attr("placeholder","");

    var search = "";
    var jqxhr = $.getJSON("/inventory/jsondata?search="+search,
        function(data) {
            window.location=$("#menu4devices a").attr("href");
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






// Выделение строки устройств
function ClickEventRow(e) {

        $("table[group=devices] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=devices] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#edititem").show();

}







/*
// устройства - переход
function DeviceData(e) {
    var dev_id = $("table[group=devices] tbody tr[marked=yes]").attr("row_id");
    var jqxhr = $.getJSON("/inventory/jsondata?dev_id="+dev_id+"&action=savedevid",
    function(data) {
        if (data["result"] == "ok")
        { window.location.href = "/inventory/devicedata/"; }

    });
}
*/









function AddDevice() {

    // Очистка полей
    $("#deviceserial").val("");
    $("#deviceaddress").val("");


    $("#createdevice").dialog({
        title:"Создание устройства",
        buttons:[{ text:"Создать",click: function() {
            if ($("#namescheme option:selected").val() && $("#devicecompany option:selected").val() && (window.address_id) && $("#deviceserial").val().length != 0 ) {
                var scheme = $("#namescheme option:selected").val();
                var company = $("#devicecompany option:selected").val();
                var address = window.address_id;
                var serial = $("#deviceserial").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });


                var data = {};
                data.scheme = scheme;
                data.company = company;
                data.address = address;
                data.serial = serial;
                data.action = "create-device";


                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok")
                        { window.location.href = "/inventory/devicedata/"+result["dev_id"]+"/"; }
                    }

                });


            }
            else { alert("Необходимо заполнить поля");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        minHeight:400,

    });

}









