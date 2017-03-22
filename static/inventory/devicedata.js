$(document).ready(function() {

    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);


    // Отображение данных
    ShowDeviceData();

    // Диалог редактирование порта
    $("#page-ports table[group=ports] tbody").on("click", "a", EditPort);



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



// Переключение закладок
function ChangeNav(e) {
    $("#nav-ports").toggleClass("active",false);
    $("#nav-slots").toggleClass("active",false);
    $("#nav-combo").toggleClass("active",false);
    $("#nav-statuses").toggleClass("active",false);
    $("#nav-removal").toggleClass("active",false);
    $("#nav-parents").toggleClass("active",false);
    $("#nav-properties").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-ports").hide();
    $("#page-slots").hide();
    $("#page-combo").hide();
    $("#page-statuses").hide();
    $("#page-removal").hide();
    $("#page-parents").hide();
    $("#page-properties").hide();

    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}






// Отображение данных по устройству
function ShowDeviceData() {
    var jqxhr = $.getJSON("/inventory/jsondata?action=getdevicedata",
    function(data) {
        console.log(data);
        if (data["result"] != "error") {

            $("#device_serial").text(data["result"]["serial"]);
            $("#device_model").text(data["result"]["model"]);
            $("#device_address").text(data["result"]["address"]);
            $("#device_company").text(data["result"]["company"]);
            $("#device_status").text(data["result"]["status"]);




            // Отображение портов
            $("table[group=ports] tbody").empty();
            $.each(data["result"]["ports"], function(key,value) {


                var t = "<tr row_id=" + value["id"] +">"
                +"<td>"+value['num']+"</td>"
                +"<td>"+value['port']+"</td>"
                +"<td>"+value['status']+"</td>"
                +"<td>"+value['datetime_str']+"</td>"
                +"<td>"+"</td>"
                +"<td>"+value['comment']+"</td>"
                +"<td>"+value['author']+"</td>"
                +"<td><a title=\"Редактировать\" href=\"#\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=ports] tbody").append(t);


            });



            // Отображение слотов
            $("table[group=slots] tbody").empty();
            $.each(data["result"]["slots"], function(key,value) {


                var t = "<tr row_id=" + value["id"] +">"
                +"<td>"+value['num']+"</td>"
                +"<td>"+value['slot']+"</td>"
                +"<td>"+value['status']+"</td>"
                +"<td>"+value['datetime_str']+"</td>"
                +"<td>"+value['comment']+"</td>"
                +"<td>"+value['author']+"</td>"
                +"<td><a title=\"Редактировать\" href=\"#\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=slots] tbody").append(t);

            });




            // Отображение комбо
            $("table[group=combo] tbody").empty();
            $.each(data["result"]["combo"], function(key,value) {


                var t = "<tr row_id=" + value["id"] +">"
                +"<td>"+value['num']+"</td>"
                +"<td>"+value['port']+"</td>"
                +"<td>"+value['slot']+"</td>"
                +"<td>"+value['status_port']+"</td>"
                +"<td>"+value['status_slot']+"</td>"
                +"<td>"+value['datetime_str']+"</td>"
                +"<td>"+value['comment']+"</td>"
                +"<td>"+value['author']+"</td>"
                +"<td><a title=\"Редактировать\" href=\"#\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=combo] tbody").append(t);

            });




            // Отображение свойств
            $("table[group=properties] tbody").empty();
            $.each(data["result"]["properties"], function(key,value) {


                var t = "<tr row_id=" + value["id"] +">"
                +"<td>"+value['name']+"</td>"
                +"<td>"+value['value']+"</td>"
                +"<td>"+value['datetime_str']+"</td>"
                +"<td>"+value['author']+"</td>"
                +"<td><a title=\"Редактировать\" href=\"#\"><span class=\"glyphicon glyphicon-edit\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=properties] tbody").append(t);

            });




        }
    });
}






// Редактирование порта
function EditPort(e) {

    //
    var port_id = $(this).parents("tr").attr("row_id");
    var status_name = $(this).parents("tr").children("td").eq(2).text();
    var num = $(this).parents("tr").children("td").eq(0).text();
    var comment = $(this).parents("tr").children("td").eq(5).text();


    $("form#editportform table tbody tr td input#num").val(num);
    $("form#editportform table tbody tr td input#comment").val(comment);
    var select_id = $("form#editportform table tbody tr td select#status").find("option:contains("+status_name+")").attr("value");
    $("form#editportform table tbody tr td select#status").val(select_id);


    $("#editport").dialog({
        title:"Изменение порта",
        buttons:[{ text:"Сохранить",click: function() {
            if ($("form#editportform table tbody tr td input#num").val().length != 0 && $("form#editportform table tbody tr td select#status").val() ) {

                var status = $("form#editportform table tbody tr td select#status").val();
                var num = $("form#editportform table tbody tr td input#num").val();
                var comment = $("form#editportform table tbody tr td input#comment").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                var data = {};
                data.port_id = port_id;
                data.num = num;
                data.status = status;
                data.comment = comment;
                data.action = "edit-port";


                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok")
                        { $("#editport").dialog("close"); ShowDeviceData(); }
                    }

                });

            }
            else { alert("Необходимо заполнить поля *");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:200,
        width:310,
        minHeight:200,

    });

}


