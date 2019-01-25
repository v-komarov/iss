$(document).ready(function() {


    $("a#new-devicetype").bind("click", NewDeviceType);
    $("ul.root a[item-id]").bind("click", EditDeviceType);

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







// Добавление нового типа
function NewDeviceType(e) {

    $("#edit-devicetype input#id_name").val("");
    $("#edit-devicetype select#id_parent").val("");

    DeviceType("new-devicetype","","Добавление");

}




// Изменение типа
function EditDeviceType(e) {

    $("#edit-devicetype input#id_name").val($(this).text());
    $("#edit-devicetype select#id_parent").val("");
    var item_id = $(this).attr("item-id");

    DeviceType("edit-devicetype",item_id,"Изменение");

}





function DeviceType(action,item_id,title) {

    $("#edit-devicetype").dialog({
        title:title,
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            var data = {};
            data.name =$("#edit-devicetype input#id_name").val();
            data.parent = $("#edit-devicetype select#id_parent").val();
            data.item_id = item_id;
            data.action = action;

            if (data.name != "") {

                $.ajax({
                  url: "/electro/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") {

                            $("#edit-devicetype").dialog("close");
                            location.href="/electro/devicestypes/";

                        }

                    }

                });


            }



        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600,
        height:200
    });


}

