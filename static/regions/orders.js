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

            if (data["result"] == "notaccess") { alert("Нет доступа к этому действию!");}

        })


    }


}






// Выбор региона
function ChoiceRegion() {
    $('#addrow').show();
    $('#tocsv').show();
    $("#select-region option[value='0']").remove();

    // Формирование ссылки
    $("#tocsv").attr("href","/regions/filedata/?action=getorders&region="+$("#select-region").val());

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

            if (data["access"] == "admin") {

            $("table[group=tableform]").empty();
            $("table[group=tableform]").append(data["form"]);
            $("select#id_region").val( region );

            RowData(action="order-adding",access="admin");

            }

            else { alert("Нет доступа к этому действию!"); }


        })

}







// Редактировать позицию
function EditRow(e) {

        var row_id = $(this).parents("tr").attr("id");

        var jqxhr = $.getJSON("/regions/jsondata/?action=edit_roworder&row_id="+row_id,
        function(data) {




            // Доступ уровня администратора или пользователя
            if (data["access"] == "admin" || data["access"] == "user") {

                $("table[group=tableform]").empty();
                $("table[group=tableform]").append(data["form"]);
                $("#orderdata").attr("row_id",data["row_id"]);

                RowData(action="order-editing", access=data["access"]);

            }

            // Для анонимного доступа
            if (data["access"] == "anonymous") { alert("Нет доступа к этому действию!");}

        })

}











// Сохранение данных с формы ввода
function RowData(action,access) {


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




                var data = {};
                data.region = $("#id_region").val();
                data.order = $("#id_order").val();
                data.model = $("#id_model").val();
                data.name = $("#id_name").val();
                data.ed = $("#id_ed").val();
                data.price = $("#id_price").val();
                data.b2b_b2o = $("#id_b2b_b2o").val();
                data.investment = $("#id_investment").val();
                data.to = $("#id_to").val();
                data.comment = $("#id_comment").val();
                data.tz = $("#id_tz").val();

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


        }},


            {text:"Закрыть",click: function() {
            $(this).dialog("close")}}
        ],
        open: function() {
            // Ограничение доступа редактирования к полям ввода
            if (access == "user") {
                $("form#form-row-order select#id_region").attr("disabled","disabled");
                $("form#form-row-order input#id_order").attr("readonly","readonly");
                $("form#form-row-order input#id_model").attr("readonly","readonly");
                $("form#form-row-order input#id_name").attr("readonly","readonly");
                $("form#form-row-order input#id_ed").attr("readonly","readonly");
            }
            // Снятие ограничений на доступ к полям ввода
            if (access == "admin") {
                $("form#form-row-order select#id_region").removeAttr("disabled");
                $("form#form-row-order input#id_order").removeAttr("readonly");
                $("form#form-row-order input#id_model").removeAttr("readonly");
                $("form#form-row-order input#id_name").removeAttr("readonly");
                $("form#form-row-order input#id_ed").removeAttr("readonly");
            }
        },
        modal:true,
        minWidth:400,
        width:600

    });

}




