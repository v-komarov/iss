$(document).ready(function() {

    // К списку проектов
    $("button#back-proj-button").bind("click",BackProjList);


    // Виджет для даты
    $("form#projedit #id_start").datepicker($.datepicker.regional['ru']);


    // Редактирование этапа
    $("table[group=stages-list] tr[row_type=stage] a[edit]").bind("click", EditStage);
    // Редактирование шага
    $("table[group=stages-list] tr[row_type=step] a[edit]").bind("click", EditStep);

    // Показать список выбора пользователей
    $("table[group=stages-list] a[user]").bind("click", ShowUserSelect);


    // Выбор пользователя и добавление пользователя
    $( "table[group=stages-list] select[user]" ).change(function() {
        AddUser();
    });


    // Удаление пользователя
    $( "table[group=stages-list] a[minus]" ).bind("click", RemoveUser);


    // Отметка "выполнено"
    $("table[group=stages-list] tr td input[type=checkbox]").bind("click", MarkDone);


});




// Возврат к списку проектов
function BackProjList(e) {

    window.location.href = "/regions/proj/page/1/";

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



// Добавление пользователя в проект : выбор из списка
function ShowUserSelect(e) {

    $("table[group=stages-list] div[group=user-list]").hide();
    $(this).parents("td").children("div[group=user-list]").show();

}




// Редактирование этапа
function EditStage(e) {

    var row_id = $(this).parents("tr").attr("row_id");

    // Предварительная наполнение полей
    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-get-data&stage_id="+row_id,
    function(data) {


        if (data["result"] == "ok") {

            $("form#edit-stage #id_name").val(data["name"]);
            $("form#edit-stage #id_order").val(data["order"]);
            $("form#edit-stage #id_days").val(data["days"]);
            $("form#edit-stage #id_depend_on").val(data["depend_on"]);

        }

    })


    $("#editstage").dialog({
        title:"Этап",
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
        minWidth:300,
        width:400

    });



}




// Редактирование шага
function EditStep(e) {


    var row_id = $(this).parents("tr").attr("row_id");


    // Предварительная наполнение полей
    var jqxhr = $.getJSON("/regions/jsondata/?action=step-get-data&step_id="+row_id,
    function(data) {



        if (data["result"] == "ok") {

            $("form#edit-step #id_name").val(data["name"]);
            $("form#edit-step #id_order").val(data["order"]);
            $("form#edit-step #id_days").val(data["days"]);
            $("form#edit-step #id_depend_on").val(data["depend_on"]);

        }

    })


    $("#editstep").dialog({
        title:"Шаг",
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
        minWidth:300,
        width:400

    });




}


// Добавление пользователя в исполнители
function AddUser(e) {

    var selob = $("table[group=stages-list] select[user]:visible");
    if (selob.val() != "") {

            var row_id = selob.parents("tr").attr("row_id");
            var row_type = selob.parents("tr").attr("row_type");

            // Добавление пользователя в этап или шаг
            var jqxhr = $.getJSON("/regions/jsondata/?action=stage-step-add-user&row_type="+row_type+"&row_id="+row_id+"&user_id="+selob.val(),
            function(data) {


                if (data["result"] == "ok") {

                    location.reload();

                }

            })

    }

}



// Удаление пользователя (исполнителя) из этапа или шага
function RemoveUser(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var row_type = $(this).parents("tr").attr("row_type");
    var user_id = $(this).parents("div[user_id]").attr("user_id");

    // Удаление пользователя из этапа или шага
    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-step-remove-user&row_type="+row_type+"&row_id="+row_id+"&user_id="+user_id,
    function(data) {


        if (data["result"] == "ok") {

            location.reload();

        }

    })


}



// Отметка о выполнении
function MarkDone(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var row_type = $(this).parents("tr").attr("row_type");

    if ($(this).is(":checked")) {
        var status = "yes";
    }
    else { var status = "no"; }

    // Отметка выполнено / не выполнено
    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-step-status&row_type="+row_type+"&row_id="+row_id+"&status="+status,
    function(data) {


        if (data["result"] == "ok") {


        }

    })


}

