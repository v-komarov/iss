$(document).ready(function() {


    // Первоначально регион
    $( "#select-region" ).val("0");


    // Выбор региона
    $( "#select-region" ).change(function() {

        ChoiceRegion();

    });


    // Добавить позицию
    $("#addrow").bind("click",AddRow);

    // Удаление строк позиций заказа
    $("table[group=orders-list] tbody").on("click","a[delete]",DeleteRowOrder);


    // Изменение позиции заказа
    $("table[group=orders-list] tbody").on("click","a[edit]",EditRow);



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






// Удаление строки заказа
function DeleteRowOrder(e) {

    var row_id = $(this).parents("tr").attr("id");
    var name = $(this).parents("tr").children("td").eq(2).text();
    var a = confirm("Удаляем "+name+" ?");

    if (a) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=delete-row-order&row_id="+row_id,
        function(data) {

            if (data["result"] == "ok") {

                ShowOrders();

            }

        })


    }


}






// Выбор региона
function ChoiceRegion() {
    $('#addrow').show();
    $('#tocsv').show();
    $("#select-region option[value='0']").remove();

    // Отображение заказов
    ShowOrders();

}





// Отображение данных по заказам
function ShowOrders() {

        // регион
        var region = $("#select-region").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=get-rows-order&region="+region,
        function(data) {

            if (data["result"] == "ok") {

                // Очистка строк
                $("table[group=orders-list] tbody").empty();

                // добавление строк
                $("table[group=orders-list] tbody").append(data["rows"]);

            }

        })



}






// Добавить позицию
function AddRow(e) {

        // регион
        var region = $("#select-region").val();

        var jqxhr = $.getJSON("/regions/jsondata/?action=new_roworder",
        function(data) {

            $("table[group=tableform]").empty();
            $("table[group=tableform]").append(data["form"]);
            $("select#id_region").val( region );


        })

    RowData(action="order-adding");
}







// Редактировать позицию
function EditRow(e) {

        var row_id = $(this).parents("tr").attr("id");

        var jqxhr = $.getJSON("/regions/jsondata/?action=edit_roworder&row_id="+row_id,
        function(data) {

            $("table[group=tableform]").empty();
            $("table[group=tableform]").append(data["form"]);
            $("#orderdata").attr("row_id",data["row_id"]);
        })

    RowData(action="order-editing");
}











// Сохранение данных с формы ввода
function RowData(action) {


    $("#orderdata").dialog({
        title:"Заказ",
        buttons:[{ text:"Сохранить",click: function() {

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            // Отправка формы
            //$("#form-row-order").submit();



            //if ($('input#namescheme').val().length != 0 && $('textarea#jsonscheme').val().length != 0) {




                var data = {};
                data.region = $("#id_region").val();
                data.order = $("#id_order").val();
                data.model = $("#id_model").val();
                data.name = $("#id_name").val();
                data.ed = $("#id_ed").val();
                data.count = $("#id_count").val();
                data.price = $("#id_price").val();
                data.comment = $("#id_comment").val();

                if (action == "order-editing") { data.row_id = $("#orderdata").attr("row_id"); }

                data.action = action;


                $.ajax({
                  url: "/regions/jsondata/",
                  type: "POST",
                  dataType: 'json',
                  data:$.toJSON(data),
                    success: function(result) {
                        if (result["result"] == "ok") { $("#orderdata").dialog('close'); ShowOrders(); }
                        else { alert(result["result"]); }
                    }

                });


            //}
            //else { alert("Необходимо заполнить поля");}

        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        modal:true,
        minWidth:400,
        width:600

    });

}




