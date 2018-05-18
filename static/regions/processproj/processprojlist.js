$(document).ready(function() {


    // Добавить элемент в реестр проектов
    $("#addproj").bind("click",AddProj);

    // Поиск по строке
    $("button#search-button").bind("click",Search);

    // Отмена поиска
    $("button#clear-button").bind("click", ClearSearch);


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






// Поиск
function Search(e) {


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    var data = {};
    data.search_text = $("input#search-text").val();
    data.systems = $("input#systems").val();
    data.initiator = $("select#initiator").val();
    data.real = $("select#real").val();
    data.stage = $("select#stage").val();
    data.stage_date1 = $("input#stage-date1").val();
    data.stage_date2 = $("input#stage-date2").val();
    data.stage_chif = $("select#stage-chif").val();
    data.executor = $("select#executor").val();
    data.executor_date1 = $("input#executor-date1").val();
    data.executor_date2 = $("input#executor-date2").val();
    data.department = $("select#department").val();
    data.create_date1 = $("input#create-date1").val();
    data.create_date2 = $("input#create-date2").val();

    data.action = "reestrproj-filter-create";


    $.ajax({
      url: "/regions/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") { window.location.href = "/regions/processproj/page/1/"; }
        }

    });



}





// Отмена поиска
function ClearSearch(e) {

    $("input#search-text").val("");
    $("input#systems").val("");
    $("select#initiator").val("");
    $("select#real").val("");
    $("select#stage").val("");
    $("input#stage-date1").val("");
    $("input#stage-date2").val("");
    $("select#stage-chif").val("");
    $("select#executor").val("");
    $("input#executor-date1").val("");
    $("input#executor-date2").val("");
    $("select#department").val("");
    $("input#create-date1").val("");
    $("input#create-date2").val("");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-filter-delete",
    function(data) {

        if (data["result"] == "ok") { location.href="/regions/processproj/page/1/"; }

    })


}







// Сохранение данных с формы ввода
function AddProj(e) {

    // Предварительная очистка полей
    $("form#reestr-proj-add #id_proj_name").val("");

    $("#reestr-proj-new").dialog({
        title:"Новый элемент проработки проектов",
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

                    data.action = "reestrproj-create";
                    data.process = "yes";

                    $.ajax({
                      url: "/regions/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { $("#reestr-proj-new").dialog('close'); window.location.href = "/regions/processproj/edit/"+result["id"]+"/"; }
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


