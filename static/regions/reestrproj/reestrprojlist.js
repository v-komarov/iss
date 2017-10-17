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
                if ( $("#id_name").val() != "" && $("#id_temp").val() != "" && $("#id_start").val() != "" ) {

                    /*
                    var data = {};
                    data.name = $("form#add-proj #id_name").val();
                    data.start = $("form#add-proj #id_start").val();
                    data.temp = $("form#add-proj #id_temp").val();

                    data.action = "create-proj";


                    $.ajax({
                      url: "/regions/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#projnew").dialog('close'); location.reload(); }
                        }

                    });
                    */

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


