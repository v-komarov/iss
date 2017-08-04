$(document).ready(function() {

    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // Сохранение общих данных по заявке
    $("button#save-common-button").bind("click", SaveCommonData);




    $('.fileinput').change(function(){
        var send_url = "http://10.6.0.135:50070/webhdfs/v1/test/events9.log?user.name=root&op=CREATE&overwrite=true&replication=4";
        var fd = new FormData();

        console.log(this);
        console.log(this.files);

        fd.append("userpic", this.files[0]);
        fd.append("username", "Groucho");

        console.log(fd);


        $.ajax({
            url: send_url,
            type: "POST",
            data: {'file':this.files[0]},
            processData: false,
            contentType: false,
            success: function(result) {
                if (result["result"] == "ok") { alert("Файл загружен!"); }
            },
            error: function(ts) { alert(ts.responseText) }

        });


    });



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






// Сохранение общих данных по сообщению
function SaveCommonData(e) {




                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });



                var data = {};
                data.head = $("form#message-data input#id_head").val();
                data.message_type = $("form#message-data select#id_message_type").val();
                data.message = $("form#message-data textarea#id_message").val();
                data.status = $("form#message-data select#id_status").val();
                data.action = "message-save-common-data";



                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { alert("Данные сохранены!"); }
                    }

                });




}






// Переключение закладок
function ChangeNav(e) {
    $("#nav-files").toggleClass("active",false);
    $("#nav-status").toggleClass("active",false);
    $("#nav-public").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-files").hide();
    $("#page-status").hide();
    $("#page-public").hide();

    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

