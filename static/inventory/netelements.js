$(document).ready(function() {


    $("#additem").bind("click",AddNetElement);
    //$("#edititem").bind("click",EditScheme);
    $("table[group=netelements] tbody tr").bind("click",ClickEventRow);

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

        $("table[group=netelements] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=netelements] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#edititem").show();

}







// Добавить сетевой элемент
function AddNetElement(e) {

    $("input#namenetelement").val("");

    $("#create_netelement").dialog({
        title:"Новый сетевой элемент",
        buttons:[{ text:"Создать",click: function() {
            if ($('input#namenetelement').val().length != 0) {
                var name = $("input#namenetelement").val();

                var csrftoken = getCookie('csrftoken');

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });


                var data = {};
                data.name = name;
                data.action = "create_netelement";


                $.ajax({
                  url: "/inventory/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "error") { alert("Возможно элемент\nс таким именем уже существует!"); }
                        else {window.location.href = "/inventory/netelement/?elem=12";}
                    }

                });


            }
            else { alert("Необходимо задать название!");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600

    });



}









