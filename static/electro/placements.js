$(document).ready(function() {


    $("a#new-placement").bind("click", NewPlacement);
    $("ul.root a[item-id]").bind("click", EditPlacement);

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







// Добавление нового размещения
function NewPlacement(e) {

    $("#edit-placement input#id_name").val("");
    $("#edit-placement select#id_parent").val("");

    Placement("new-placement","","Добавление");

}




// Изменение размещения
function EditPlacement(e) {

    $("#edit-placement input#id_name").val($(this).text());
    $("#edit-placement select#id_parent").val("");
    var item_id = $(this).attr("item-id");

    Placement("edit-placement",item_id,"Изменение");

}





function Placement(action,item_id,title) {

    $("#edit-placement").dialog({
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
            data.name =$("#edit-placement input#id_name").val();
            data.parent = $("#edit-placement select#id_parent").val();
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

                            $("#edit-placement").dialog("close");
                            location.href="/electro/placements/";

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

