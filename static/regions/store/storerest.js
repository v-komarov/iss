$(document).ready(function() {

    $("table[group=goods-list] td a").bind("click", EditRest);
    $("button#create-button").bind("click", CreateRest);


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





















// Корректировка остатков
function EditRest(e) {


    var row_id = $(this).parents("tr").attr("row_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+row_id,
    function(data) {

            if (data["result"] == "ok") {
                $("input#edit_name").val(data["rec"]["name"]);
                $("input#edit_eisup").val(data["rec"]["eisup"]);
                $("input#edit_store").val(data["rec"]["store"]);
                $("input#edit_rest").val(data["rec"]["rest"]);
                $("input#edit_serial").val(data["rec"]["serial"]);
                $("input#edit_dimension").val(data["rec"]["dimension"]);
                $("input#edit_accounting_code").val(data["rec"]["accounting_code"]);

                if (data["rec"]["eisup"] == "") { $("input#edit_name").prop("readonly",false); }
                else { $("input#edit_name").prop("readonly",true); }

            }

    });




    $("#edit-rest").dialog({
        title:"Корректировка остатков",
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
            data.row_id = row_id;
            data.rest = $("input#edit_rest").val();
            data.serial = $("input#edit_serial").val();
            data.name = $("input#edit_name").val();
            data.dimension = $("input#edit_dimension").val();
            data.accounting_code =$("input#edit_accounting_code").val()
            data.action = "store-edit-rest";



            $.ajax({
              url: "/regions/jsondata/",
              type: "POST",
              dataType: 'json',
              data:$.toJSON(data),
                success: function(result) {
                    if (result["result"] == "ok") {
                        $("table[group=goods-list] tr[row_id="+row_id+"]").css("background-color","#F0E68C");
                        var jqxhr = $.getJSON("/regions/jsondata/?action=store-rest-record&row_id="+row_id,
                        function(data) {
                            if (data["result"] == "ok") {
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(1).text(data["rec"]["name"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(2).text(data["rec"]["serial"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(3).text(data["rec"]["rest"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(4).text(data["rec"]["dimension"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(9).text(data["rec"]["mol"]);
                                $("table[group=goods-list] tr[row_id="+row_id+"]").children("td").eq(10).text(data["rec"]["accounting_code"]);
                            }
                        });

                        $("#edit-rest").dialog("close");

                    }
                    else {
                        $("#edit-rest").dialog("close");

                        $("#notaccess").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 1000 }});
                        $("#notaccess").dialog("close");
                    }
                }

            });


        }},


            {text:"Закрыть",click: function() {
            //location.href="/regions/store/page/1/";
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:500,
        height:350
    });


}






// Создание нового остатка
function CreateRest(e) {

    $("input#create-name").val("");
    $("input#createrest").val("");
    $("input#create-dimension").val("");
    $("input#create-accounting-code").val("")
    $("input#create-serial").val("")


    $("#create-rest").dialog({
        title:"Создание нового остатка",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            if ($("input#create-name").val() != "" && $("input#createrest").val() != "") {

                var data = {};
                data.name = $("input#create-name").val();
                data.serial = $("input#create-serial").val();
                data.store = $("select#create-store").val();
                data.rest = $("input#createrest").val();
                data.dimension = $("input#create-dimension").val();
                data.accounting_code = $("input#create-accounting-code").val();
                data.action = "store-create-rest";


                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") {
                            var t = "<tr rec_id="+result["rec"]["id"]+" style=\"background-color:#F0E68C;\">"
                            + "<td></td>"
                            + "<td>"+result["rec"]["name"]+"</td>"
                            + "<td>"+result["rec"]["serial"]+"</td>"
                            + "<td>"+result["rec"]["rest"]+"</td>"
                            + "<td>"+result["rec"]["dimention"]+"</td>"
                            + "<td>"+result["rec"]["datetime"]+"</td>"
                            + "<td>"+result["rec"]["region"]+"</td>"
                            + "<td>"+result["rec"]["store"]+"</td>"
                            + "<td>"+result["rec"]["comment"]+"</td>"
                            + "<td>"+result["rec"]["mol"]+"</td>"
                            + "<td>"+result["rec"]["accounting_code"]+"</td>"
                            + "</tr>"

                            $("table[group=goods-list] tbody").prepend(t);

                            $("#create-rest").dialog("close");

                        }
                    }

                });

            }
            else { alert("Необходимо заполнить поля!");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:500,
        height:320
    });


}