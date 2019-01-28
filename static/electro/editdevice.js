$(document).ready(function() {


    $("button#btn-save").bind("click", DeviceDataSave);


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




// Сохранение основных данных карточки Устройства
function DeviceDataSave(e) {

    var device_id = $("div#common").attr("device-id");

    $("#saving h3").text("Сохранение выполнено");
    $("#saving").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});


    var data = {};
    data.device_id = device_id;
    data.serial = $("input#id_serial").val();
    data.name = $("input#id_name").val();
    data.devicetype = $("select#id_devicetype").val();
    data.placement = $("select#id_placement").val();
    data.address = $("input#id_address").val();
    data.comment = $("textarea#id_comment").val();


    data.action = "device-common-save";

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/electro/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                $("#saving").dialog("close");

            }
        }

    });



}

