$(document).ready(function() {

    // Добавление списка сетевых элементов
    $("#additem").bind("click",AddNetElement);
    //$("#edititem").bind("click",EditScheme);
    // Для списка сетевых элементов
    //$("table[group=netelements] tbody tr").bind("click",ClickEventRow);
    // Редактирование сетевого элемента
    //$("#edititem").bind("click",EditNetElement);

    // Для интерфейса списка сетевых элементов
    $("#edititem").hide();



    // Поиск
    $("button#runsearch").bind("click",RunSearch);

    // Сброс поиска
    $("button#clearsearch").bind("click",ClearSearch);


});






// Поиск
function RunSearch(e) {
    var search = $("input#search_netelem").val();
    var jqxhr = $.getJSON("/inventory/jsondata?search2="+search,
        function(data) {
            window.location=$("#menunetelements a").attr("href");
        })
}



// Отмена Search
function ClearSearch(e) {
    $("input#search_netelem").val("");
    $("input#search_netelem").attr("placeholder","");

    var search = "";
    var jqxhr = $.getJSON("/inventory/jsondata?search2="+search,
        function(data) {
            window.location=$("#menunetelements a").attr("href");
        })
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






// Выделение строки сетевых элементов
function ClickEventRow(e) {

        $("table[group=netelements] tbody tr").css("background-color","");
        $(this).css("background-color","#F0E68C");
        $("table[group=netelements] tbody tr").attr("marked","no");
        $(this).attr("marked","yes");

        $("#edititem").show();

}









// Редактирование элемента
function EditNetElement(e) {

    // определение id
    var row_id = $("table[group=netelements] tbody tr[marked=yes]").attr("row_id");


    // Сохранение id элемента
    var jqxhr = $.getJSON("/inventory/jsondata?savenetelem="+row_id,
    function(data) {
        window.location.href = "/inventory/netelementdata/?netelemid="+row_id;
    })

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
                        else {window.location.href = "/inventory/netelementdata/"+result["netelemid"]+"/";}
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









