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

    var search = $("input#search-text").val();

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-list-search&search="+search,
    function(data) {

        if (data["result"] == "ok") { location.reload(); }

    })

}



// Отмена поиска
function ClearSearch(e) {

    $("input#search-text").val("");

    var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-list-search&search=",
    function(data) {

        if (data["result"] == "ok") { location.reload(); }

    })


}






// Сохранение данных с формы ввода
function AddProj(e) {

    // Предварительная очистка полей
    $("form#reestr-proj-add #id_proj_name").val("");

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


