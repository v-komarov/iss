$(document).ready(function() {


    $("#additem").bind("click",AddScheme);
    $("#edititem").bind("click",EditScheme);
    $("table[group=devicescheme] tbody tr").bind("click",ClickEventRow);

    $("#edititem").hide();

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






// Выделение строки
function ClickEventRow(e) {

        $("table[group=devicescheme] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=devicescheme] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#edititem").show();

}







// Добавить схему
function AddScheme(e) {

    $("#editschemeform").attr("action","create_scheme");
    $("#editschemeform").attr("scheme-id","");

    $("#editschemeform table tbody tr td input#namescheme").val("");
    $("#editschemeform table tbody tr td textarea#jsonscheme").val("");

    RowData();

}





// Редактировать схему
function EditScheme(e) {

    var row_id = $("table[group=devicescheme] tbody tr[marked=yes]").attr("row_id");
    $("#editschemeform").attr("action","edit_scheme");
    $("#editschemeform").attr("scheme-id",row_id);

    var jqxhr = $.getJSON("/inventory/jsondata?scheme="+row_id,
        function(data) {

            $("#editschemeform table tbody tr td input#namescheme").val(data["name"]);
            $("#editschemeform table tbody tr td textarea#jsonscheme").val(data["scheme_device"]);

            RowData();

        })

}







function RowData() {


    $("#editscheme").dialog({
        title:"Схема",
        buttons:[{ text:"Сохранить",click: function() {
            if ($('input#namescheme').val().length != 0 && $('textarea#jsonscheme').val().length != 0) {
                var name = $("#editschemeform table tbody tr td input#namescheme").val();
                var scheme_device = $("#editschemeform table tbody tr td textarea#jsonscheme").val();


                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });


                var data = {};
                data.scheme_device = scheme_device;
                data.name = name;
                data.scheme_id = $("#editschemeform").attr("scheme-id");
                data.action = $("#editschemeform").attr("action");


                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { location.reload(); }
                        else { alert(result["result"]); }
                    }

                });


            }
            else { alert("Необходимо заполнить поля");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600

    });

}




