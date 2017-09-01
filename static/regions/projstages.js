$(document).ready(function() {

    // К списку проектов
    $("button#back-proj-button").bind("click",BackProjList);

    // рассчет дат проекта
    $("button#calculate-date-button").bind("click",CalculateDate);


    // Виджет для даты
    $("form#projedit #id_start").datepicker($.datepicker.regional['ru']);

    // Добавление нового этапа
    $("button#stage-adding").bind("click", AddStage);
    // Редактирование этапа
    $("table[group=stages-list] tr a[edit]").bind("click", EditStage);
    // Список комментариев
    $("table[group=stages-list] tr td a[book]").bind("click", PreNote);

    // Показать список выбора пользователей
    $("table[group=stages-list] a[user]").bind("click", ShowUserSelect);

    // Показать выбор загружаемого файла
    $("table[group=stages-list] a[file]").bind("click", ShowUploadFile);

    // Удаление вложенного файла
    $("table[group=stages-list] a[file-delete]").bind("click", DeleteFile);


    // Выбор пользователя и добавление пользователя
    $( "table[group=stages-list] select[user]" ).change(function() {
        AddUser();
    });


    // Удаление пользователя
    $( "table[group=stages-list] a[minus]" ).bind("click", RemoveUser);


    // Редактирование основных данных проекта
    $("form#projedit button").bind("click",EditProjData);


    $('table[group=stages-list] tbody tr td input.fileinput').change(function(){
        //UploadFile();
    });

    // Добавление коментария к этапу или шагу
    $("div#noteslist table#noteadd tbody tr td button#addnote").bind("click",AddNote);


    // Удаление пункта
    $("table[group=stages-list] tr td a[delete]").bind("click", DeleteStage);



    Percents();


});









// Отрисовка слайдера
function Percents() {


      // Чтение процентов выполнеия
      var jqxhr = $.getJSON("/regions/jsondata/?action=stage-percent-status",
            function(data) {


              $('.project').each(function() {

                var $projectBar = $(this).find('.bar');
                var $projectPercent = $(this).find('.percent');
                var $projectRange = $(this).find('.ui-slider-range');
                var row_id = $(this).parents("tr").attr("row_id");

                // Предварительная прорисовка значений
                var percent = data['status']["row"+row_id];

                $projectPercent.val(percent + "%");

                    if (percent < 30) {
                      $projectPercent.css({'color': 'red'});
                      $projectRange.css({'background': '#f20000'});
                    } else if (percent > 31 && percent < 70) {
                      $projectPercent.css({
                        'color': 'gold'
                      });
                      $projectRange.css({
                        'background': 'gold'
                      });
                    } else if (percent > 70) {
                      $projectPercent.css({
                        'color': 'green'
                      });
                      $projectRange.css({
                        'background': 'green'
                      });
                    }







                $projectBar.slider({
                  range: "min",
                  animate: true,
                  value: data['status']["row"+row_id],
                  min: 0,
                  max: 100,
                  step: 1,
                  slide: function(event, ui) {
                    $projectPercent.val(ui.value + "%");
                  },
                  change: function(event, ui) {
                    var $projectRange = $(this).find('.ui-slider-range');
                    var percent = ui.value;

                    // Запись значения в базу
                    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-percent&row_id="+row_id+"&percent="+percent,
                        function(data) {

                        })


                    if (percent < 30) {
                      $projectPercent.css({
                        'color': 'red'
                      });
                      $projectRange.css({
                        'background': '#f20000'
                      });
                    } else if (percent > 31 && percent < 70) {
                      $projectPercent.css({
                        'color': 'gold'
                      });
                      $projectRange.css({
                        'background': 'gold'
                      });
                    } else if (percent > 70) {
                      $projectPercent.css({
                        'color': 'green'
                      });
                      $projectRange.css({
                        'background': 'green'
                      });
                    }
                  }
                });
              })







      })




}








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






// Удаление этапа
function DeleteStage(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var stage_name = $(this).parents("tr").children("td").eq(1).text().replace(/^\s\s*/, '').replace(/\s\s*$/, '');
    var deletestage = confirm("Удаляем "+stage_name+" ?");


    if (deletestage) {

        // Удаление этапа
        var jqxhr = $.getJSON("/regions/jsondata/?action=stage-delete&row_id="+row_id,
        function(data) {


            if (data["result"] == "ok") {

                location.reload();

            }

        })


    }

}






// Рассчитать даты проекта
function CalculateDate(e) {


    // пересчитать даты проекта
    var jqxhr = $.getJSON("/regions/jsondata/?action=project-calculate",
    function(data) {


        if (data["result"] == "ok") {

            location.reload();

        }

    })


}





// Удаление вложенного файла
function DeleteFile(e) {

    var row_id = $(this).parents("tr").attr("row_id");
    var file_id = $(this).attr("file_id");
    var file_name = $(this).attr("file_name");
    var deletefile = confirm("Удаляем файл "+file_name+" ?");


    if (deletefile) {

        // Удаление файла
        var jqxhr = $.getJSON("/regions/jsondata/?action=stage-step-delete-file&row_id="+row_id+"&file_id="+file_id,
        function(data) {


            if (data["result"] == "ok") {

                location.reload();

            }

        })


    }

}



// Загрузка файла
/*
function UploadFile(e) {

    var selfile = $("table[group=stages-list] div[group=file] input.fileinput:visible");

    var fd = new FormData();
    fd.append("filedata", selfile[0].files[0]);
    fd.append("action", "proj-load-file");



    //var data = {};
    //data.filedata = selfile[0].files[0];
    //data.action = "proj-load-file";

    //console.log(data);

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $.ajax({
        url: "/regions/proj/upload/",
        type: "POST",
        data: fd,
        enctype: 'multipart/form-data',
        processData: false,
        //contentType: false,
        //headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        success: function(result) {
            if (result["result"] == "ok") { alert("Файл загружен!"); }
        },
        error: function(ts) { alert(ts.responseText) }

    });



}
*/




// Редактирование основных данных проекта
function EditProjData(e) {


    $("form#projedit #id_name").css("background-color","yellow");
    $("form#projedit #id_start").css("background-color","yellow");

    var nameproj = $("form#projedit #id_name").val();
    var startproj = $("form#projedit #id_start").val();


    var data = {};
    data.name = nameproj;
    data.start = startproj;

    data.action = "save-proj-main-data";


    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    $.ajax({
      url: "/regions/jsondata/",
      type: "POST",
      dataType: 'json',
      data:$.toJSON(data),
        success: function(result) {
            if (result["result"] == "ok") {

                $("form#projedit #id_name").css("background-color","");
                $("form#projedit #id_start").css("background-color","");

            }
        }

    });



}






// Добавление пользователя в проект : выбор из списка
function ShowUserSelect(e) {

    $("table[group=stages-list] div[group=user-list] select[user]").val("");
    $("table[group=stages-list] div[group=user-list]").hide();
    $(this).parents("td").children("div[group=user-list]").show();

}



// Интерфейс загрузки файла
function ShowUploadFile(e) {

    $("table[group=stages-list] div[group=file]").hide();
    $(this).parents("td").children("div[group=file]").show();

}





// Редактирование этапа
function EditStage(e) {

    var row_id = $(this).parents("tr").attr("row_id");

    // Предварительная наполнение полей
    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-get-data&stage_id="+row_id,
    function(data) {


        if (data["result"] == "ok") {

            $("form#edit-stage #id_name").val(data["name"]);
            $("form#edit-stage #id_stage_order").val(data["order"]);
            $("form#edit-stage #id_days").val(data["days"]);
            $("form#edit-stage #id_deferment").val(data["deferment"]);
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
                if ( $("form#edit-stage #id_name").val() != "" && $("form#edit-stage #id_order").val() != "" ) {

                    var data = {};
                    data.row_id = row_id;
                    data.name = $("form#edit-stage #id_name").val();
                    data.order = $("form#edit-stage #id_stage_order").val();
                    data.days = $("form#edit-stage #id_days").val();
                    data.deferment = $("form#edit-stage #id_deferment").val();
                    data.depend_on = $("form#edit-stage #id_depend_on").val();

                    data.action = "save-stage-data";

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








// Создание нового этапа
function AddStage(e) {


    // Очистка полей формы
    $("form#edit-stage #id_name").val("");
    $("form#edit-stage #id_stage_order").val("");
    $("form#edit-stage #id_days").val("");
    $("form#edit-stage #id_deferment").val("");
    $("form#edit-stage #id_depend_on").val("");



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
                if ( $("form#edit-stage #id_name").val() != "" && $("form#edit-stage #id_order").val() != "" ) {

                    var data = {};
                    data.name = $("form#edit-stage #id_name").val();
                    data.order = $("form#edit-stage #id_stage_order").val();
                    data.days = $("form#edit-stage #id_days").val();
                    data.deferment = $("form#edit-stage #id_deferment").val();
                    data.depend_on = $("form#edit-stage #id_depend_on").val();

                    data.action = "create-stage-data";

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
    var user_id = $(this).parents("div[user_id]").attr("user_id");

    // Удаление пользователя из этапа или шага
    var jqxhr = $.getJSON("/regions/jsondata/?action=stage-step-remove-user&row_id="+row_id+"&user_id="+user_id,
    function(data) {


        if (data["result"] == "ok") {

            location.reload();

        }

    })


}





// Предварительное сохранение row_id
function PreNote(e) {

    // Сохранение в объектах окна типа и id записи
    $("div#noteslist").attr("row_id",$(this).parents("tr").attr("row_id"));
    Notes();
}







// Списка заметок по шагу или этапу
function Notes(e) {

    var row_id = $("div#noteslist").attr("row_id");
    var row_type = $("div#noteslist").attr("row_type");


    // Очистка поля ввода новго ДРП
    $("textarea#text-new-note").val("");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-proj-notes&row_type="+row_type+"&row_id="+row_id,
        function(data) {

            // Предварительная очистка списка
            $("#proj-notes-list").empty();

            $.each(data['notes_list'], function(index,value){

                var v = value;

                t = "<dt>"+v["author"]+"<br> ("+v["datetime"]+")<br></dt>"
                +"<dd>"
                + v["note"] +"<br>"
                + "</dd>"

                $("#proj-notes-list").prepend(t);

            });




            $("#noteslist").dialog({
                open:function() {
                },
                  title:"Коментарии: " + data["name"],
                closeOnEscape: false,
                  show: {
                    effect: "blind",
                    duration: 100
                  },
                  hide: {
                    effect: "blind",
                    duration: 100
                  },
                  buttons: [{text:"Закрыть", click: function() { $(this).dialog("close");  }}],
                  modal:true,
                  minWidth:400,
                  width:600,
                  height:400

            });
    })


}






// Добавление коментария
function AddNote(e) {


        var data = {};
        data.row_id = $("div#noteslist").attr("row_id");
        data.row_type = $("div#noteslist").attr("row_type");
        data.note = $("textarea#text-new-note").val();
        data.action = "proj-adding-note";



        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        $.ajax({
          url: "/regions/jsondata/",
          type: "POST",
          dataType: 'json',
          data:$.toJSON(data),
            success: function(result) {

                Notes();

            }

        });


}

