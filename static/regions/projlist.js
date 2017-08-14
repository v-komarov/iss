$(document).ready(function() {

    // Добавить Проект
    $("#addproj").bind("click",AddProj);

    // Виджет для даты
    $("form#add-proj #id_start").datepicker($.datepicker.regional['ru']);


    // Переход на редактирование
    $("table[group=proj-list] tbody td a[stage]").bind("click",LinkEditProj);


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
    $("form#add-proj #id_name").val("");
    $("form#add-proj #id_start").val("");
    $("form#add-proj #id_temp").val("");

    $("#projnew").dialog({
        title:"Проект",
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





// Сохранить id проекта и перейти
function LinkEditProj(e) {

    var proj_id = $(this).parents("tr").attr("row_id");
    window.location.href = "/regions/proj/edit/"+proj_id+"/";

        /*
        // id сообщешия
        var proj_id = $(this).parents("tr").attr("row_id");

        var jqxhr = $.getJSON("/regions/jsondata/?action=proj-save-id&proj_id="+proj_id,
        function(data) {

            if (data["result"] == "ok") {

                window.location.href = "/regions/proj/edit/";

            }

        })
        */


}
