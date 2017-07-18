$(document).ready(function() {

    // Создание пользователя
    $("a#newuser").bind("click",AddUser);


    // Смена и отправка пароля по почте
    $("a#repair").bind("click",ChangePasswd);


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







// Изменение пароля и отправка по email
function ChangePasswd(e) {

    var login = prompt("Введите логин","");

    if ( login != null ) {

        var jqxhr = $.getJSON("/begin/jsondata/?action=new-passwd&login="+login,
        function(data) {


            if (data["result"] == "ok") { alert(data["comment"]); }

            else { alert(data["comment"]); }

        })



    }
}








// Добавить пользователя
function AddUser(e) {


        var jqxhr = $.getJSON("/begin/jsondata/?action=new-user-form",
        function(data) {


            if (data["result"] == "ok") {

                $("table[group=new-user-form]").empty();
                $("table[group=new-user-form]").append(data["form"]);

                RowData();

            }

            else { alert("Нет доступа к этому действию!"); }


        })

}




// Сохранение данных с формы ввода
function RowData(action,access) {


    $("#new-user-dialog").dialog({
        title:"Регистрация пользователя",
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
                data.login = $("#new-user-dialog input#id_login").val();
                data.passwd = $("#new-user-dialog input#id_passwd").val();
                data.email = $("#new-user-dialog input#id_email").val();
                data.firstname = $("#new-user-dialog input#id_firstname").val();
                data.lastname = $("#new-user-dialog input#id_lastname").val();
                data.action = "user-adding";


                $.ajax({
                  url: "/begin/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { $("#new-user-dialog").dialog('close'); alert("Учетная запись создана!");}
                        else { $("#new-user-dialog").dialog('close'); alert(result["comment"]); }
                    }

                });


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:200,
        width:400

    });

}

