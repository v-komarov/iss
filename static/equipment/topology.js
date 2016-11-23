$(document).ready(function() {

    $("#select-domen").val("");

    ClearSelects();

    // Выбр домена
    $( "#select-domen" ).change(function() {
        var domen = $(this).val();
        ClearSelects();
        $("#addlink").hide();
        $('#select-footnode option').each(function(){
            if ($(this).attr("domen") == domen) {
                $(this).show();
            }
        });

    });


    // Выбор опорного узла
    $( "#select-footnode" ).change(function() {
        var footnode = $(this).val();

        $("#select-agregator option").each(function(){ $(this).hide(); })
        $('#select-agregator option').each(function(){
            if ($(this).attr("footnode") == footnode) {
                $(this).show();
            }
        });

    });


    // Выбор агрегатора
    $( "#select-agregator" ).change(function() {

        $("#addlink").show();

    });



    $("#addlink").hide();

    $("#addlink").bind("click",AddLink);








    //// Валидация
    $("#add-link").validate({
        highlight: function(element, errorClass) {
            $(element).add($(element).parent()).addClass("invalidElem");
        },
        unhighlight: function(element, errorClass) {
            $(element).add($(element).parent()).removeClass("invalidElem");
        },

        errorElement: "div",
        errorClass: "errorMsg",

          rules: {
            ipaddress1: {
                required: true,
                minlength: 7,
                maxlength: 15
            },
            ipaddress2: {
                required: true,
                minlength: 7,
                maxlength: 15
            },
            port1: {
                required: true,
                number: true,
                range: [1,48]
            },
            port2: {
                required: true,
                number: true,
                range: [1,48]
            },
          },

    });// Валидация


    $("#add-link table tbody tr td input").change(function(e) {
        $("#add-link").validate().element($(e.target));
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













function ClearSelects() {

    // Выбор по опорному узлу и агрегатору первоначально очистить список
    $("#select-footnode").val("");
    $("#select-footnode option").each(function(){ $(this).hide(); });
    $("#select-agregator").val("");
    $("#select-agregator option").each(function(){ $(this).hide(); });


}




// Добавление связи
function AddLink(e) {


    $("#form-add-link #add-link table tbody tr td input#ipaddress1").val("");
    $("#form-add-link #add-link table tbody tr td input#ipaddress2").val("");
    $("#form-add-link #add-link table tbody tr td input#port1").val("");
    $("#form-add-link #add-link table tbody tr td input#port2").val("");


    $("#form-add-link").dialog({
        title:"Добавление связи",
        buttons:[{ text:"Сохранить",click: function() {
            if ($('#ipaddress1').valid() && $('#ipaddress2').valid() && $('#port1').valid() && $('#port2').valid()) {
                var ipaddress1 = $("#form-add-link #add-link table tbody tr td input#ipaddress1").val();
                var ipaddress2 = $("#form-add-link #add-link table tbody tr td input#ipaddress2").val();
                var port1 = $("#form-add-link #add-link table tbody tr td input#port1").val();
                var port2 = $("#form-add-link #add-link table tbody tr td input#port2").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });


                t = "<tr>"
                +"<td>"+ipaddress1+"</td>"
                +"<td>"+port1+"</td>"
                +"<td>"+port2+"</td>"
                +"<td>"+ipaddress2+"</td>"
                +"<td><a href=\"#\"><span class=\"glyphicon glyphicon-plus\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>"

                $("table[group=\"user-links\"] tbody").prepend(t);


                /*
                $.ajax({
                  url: "/equipment/devices/jsondata/",
                  type: "POST",
                  dataType: 'text',
                  data:"{"
                    +"'row_id':'"+row_id+"',"
                    +"'action':'"+action+"',"
                    +"'ipaddress':'"+ipaddress+"',"
                    +"'name':'"+name+"',"
                    +"'descr':'"+descr+"',"
                    +"'location':'"+location+"',"
                    +"'serial':'"+serial+"',"
                    +"'mac':'"+mac+"',"
                    +"'domen':'"+domen+"'"
                    +"}",
                    success: function(result) {
                        //window.location=$("#menufootnodes a").attr("href");
                    }

                })
                */
            }

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:250,
        width:400

    });

}

