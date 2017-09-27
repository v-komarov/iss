$(document).ready(function() {


    // Первоначально раздел
    if ( $("#manager").attr("section") == "0" ) {
        $( "#select-section" ).val("0");
    }
    else {
        $('#addt').show();
        $("#select-section option[value='0']").remove();
        $( "#select-section" ).val( $("#manager").attr("section") );
    }


    // Выбор раздела
    $( "#select-section" ).change(function() {

        ChoiceSections();

    });


    // Отметка для выгрузки в отчет
    $("table[group=results-list] tbody tr td input[type=checkbox]").bind("click", MarkReport);

    // Редактирование должности и места работы
    $("table[group=results-list] tbody").on("click", "a[edit]", EditResult);



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






// Выбор раздела
function ChoiceSections() {

        // Раздел
        var section = $("#select-section").val();

        var jqxhr = $.getJSON("/exams/jsondata/?action=choice-section&section="+section,
        function(data) {

            if (data["result"] == "ok") {

                ClearReport();
                // Отображение вопросов выбранного раздела
                window.location=$("#menuexamsresults a").attr("href");
            }

        })



}



// Отметка о для выгрузки
function MarkReport(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var row_type = $(this).parents("tr").attr("row_type");

    if ($(this).is(":checked")) {
        var status = "yes";
    }
    else { var status = "no"; }

    // Отметка добавть / убрать из списка выгрузки
    var jqxhr = $.getJSON("/exams/jsondata/?action=report&row_id="+row_id+"&status="+status,
    function(data) {


        if (data["result"] == "ok") {


        }

    })


}




// Удаление списка для вывода в отчет
function ClearReport(e) {


    // Отметка добавть / убрать из списка выгрузки
    var jqxhr = $.getJSON("/exams/jsondata/?action=report-clear",
    function(data) {


        if (data["result"] == "ok") {


        }

    })


}







// Редактирование ФИО, должности и места работы
function EditResult(e) {

    var result_id = $(this).parents("tr").attr("row_id");

    // Заполнение полей
    var jqxhr = $.getJSON("/exams/jsondata/?action=get-data-result&result_id="+result_id,
    function(data) {


        if (data["result"] == "ok") {

            $("form#resultdata input#id_worker").val(data["worker"]);
            $("form#resultdata input#id_job").val(data["job"]);
            $("form#resultdata input#id_department").val(data["department"]);

        }

    })


    SaveResult(result_id);

}






// Сохранение данных результата
function SaveResult(result_id) {


    $("#result-data").dialog({
        title:"Должность и место работы",
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
                if ( $("form#resultdata input#id_job").val() != "" && $("form#resultdata input#id_department").val()!= "" && $("form#resultdata input#id_worker").val() != "") {




                    var data = {};
                    data.result_id = result_id;
                    data.worker = $("form#resultdata input#id_worker").val();
                    data.job = $("form#resultdata input#id_job").val();
                    data.department = $("form#resultdata input#id_department").val();
                    data.action = "save-result";

                    $.ajax({
                      url: "/exams/jsondata/",
                      type: "POST",
                      dataType: 'json',
                      data:$.toJSON(data),
                        success: function(result) {
                            if (result["result"] == "ok") { window.location.reload(); }
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
        width:500

    });

}



