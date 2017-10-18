$(document).ready(function() {


    // Добавить элемент в реестр проектов
    $("#addproj").bind("click",AddProj);



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





// Сохранение данных с формы ввода
function AddProj(e) {

    // Предварительная очистка полей
    $("form#reestr-proj-add #id_proj_name").val("");
    $("form#reestr-proj-add #id_proj_other").val("00000");
    $("form#reestr-proj-add #id_proj_level").val("00");

    $("#reestr-proj-new").dialog({
        title:"Новый элемент реестра проектов",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });



                // Проверка значений
                if ( $("form#reestr-proj-add #id_proj_name").val() != "" && $("form#reestr-proj-add #id_proj_other").val() != "" && $("form#reestr-proj-add #id_proj_level").val() != "" ) {

                    var data = {};
                    data.name = $("form#reestr-proj-add #id_proj_name").val();
                    data.other = $("form#reestr-proj-add #id_proj_other").val();
                    data.level = $("form#reestr-proj-add #id_proj_level").val();
                    data.proj_init = $("form#reestr-proj-add #id_proj_init").val();
                    data.proj_type = $("form#reestr-proj-add #id_proj_type").val();
                    data.region = $("form#reestr-proj-add #id_region").val();
                    data.block = $("form#reestr-proj-add #id_block").val();

                    data.action = "reestrproj-create";


                    $.ajax({
                      url: "/regions/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#reestr-proj-new").dialog('close'); window.location.href = "/regions/reestrproj/edit/"+result["id"]+"/"; }
                        }

                    });


                }
                else { alert("Заполните поля!"); }


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        open: function() {
        },
        modal:true,
        minWidth:400,
        width:600

    });

}


