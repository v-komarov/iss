$(document).ready(function() {

    $("button#create-button").bind("click", CreateAVR);

    // Виджет для даты
    $("input#id_datetime_avr").datepicker($.datepicker.regional['ru']);
    $("input#id_datetime_work").datepicker($.datepicker.regional['ru']);


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





// Создание нового АВР
function CreateAVR(e) {

    $("select#id_region").val("");
    $("select#id_city").val("");
    $("input#id_objnet").val("");
    $("input#id_address").val("");
    $("input#id_datetime_avr").val("");
    $("input#id_datetime_work").val("");
    $("select#id_staff").val("");


    $("#avr").dialog({
        title:"Создание нового АВР",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            var region = $("select#id_region").val();
            var city = $("select#id_city").val();
            var objnet = $("input#id_objnet").val();
            var address = $("input#id_address").val();
            var datetime_avr = $("input#id_datetime_avr").val();
            var datetime_work = $("input#id_datetime_work").val();
            var staff = $("select#id_staff").val();


            if (region != "" && city != "" && objnet != "" && address != "" && datetime_avr != "" && staff != "") {

                var data = {};
                data.region = region;
                data.city = city;
                data.address = address;
                data.objnet = objnet;
                data.datetime_avr = datetime_avr;
                data.datetime_work = datetime_work;
                data.staff = staff;
                data.action = "avr-create";



                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") {
                            $("#avr").dialog('close');
                        }
                    }

                });

            }
            else { alert("Необходимо заполнить поля!");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        width:550,
        height:350
    });


}