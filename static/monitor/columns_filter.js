$(document).ready(function() {

    /*

        Управление фильтрацией по колонкам оперативного журнала

    */

    $("#columns-filter-on").bind("click",FilterColumnsSave);

    //$("#head-table-events th input[type=text]").keyup(function() {

        //FilterColumns();

    //});
    ColorSeverity();
    FilterColumnsShow();

});








// Отображение сохраненных значений фильтров
function FilterColumnsShow() {


    var jqxhr = $.getJSON("/monitor/events/jsondata?getfiltercolumns=ok",
        function(data) {


            $("#head-table-events th input[type=text]").eq(0).val(data["f1"]);
            $("#head-table-events th input[type=text]").eq(1).val(data["f2"]);
            $("#head-table-events th input[type=text]").eq(2).val(data["f3"]);
            $("#head-table-events th input[type=text]").eq(3).val(data["f4"]);
            $("#head-table-events th input[type=text]").eq(4).val(data["f5"]);
            $("#head-table-events th input[type=text]").eq(5).val(data["f6"]);
            $("#head-table-events th input[type=text]").eq(6).val(data["f7"]);
            $("#head-table-events th input[type=text]").eq(7).val(data["f8"]);
            $("#head-table-events th input[type=text]").eq(8).val(data["f9"]);
            $("#head-table-events th input[type=text]").eq(9).val(data["f10"]);
            $("#head-table-events th input[type=text]").eq(10).val(data["f11"]);
            $("#head-table-events th input[type=text]").eq(11).val(data["f12"]);
            $("#head-table-events th input[type=text]").eq(12).val(data["f13"]);
            $("#head-table-events th input[type=text]").eq(13).val(data["f14"]);



            $.each($("#body-table-events tr"), function( indexrow, valuerow ) {


                if ($(valuerow).children("td").eq(2).text().toUpperCase().indexOf(data["f1"].toUpperCase()) <= 0  && data["f1"] != "") { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(3).text().toUpperCase().indexOf(data["f2"].toUpperCase()) <= 0  && data["f2"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(4).text().toUpperCase().indexOf(data["f3"].toUpperCase()) <= 0  && data["f3"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(5).text().toUpperCase().indexOf(data["f4"].toUpperCase()) <= 0  && data["f4"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(6).text().toUpperCase().indexOf(data["f5"].toUpperCase()) <= 0  && data["f5"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(7).text().toUpperCase().indexOf(data["f6"].toUpperCase()) <= 0  && data["f6"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(8).text().toUpperCase().indexOf(data["f7"].toUpperCase()) <= 0  && data["f7"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(9).text().toUpperCase().indexOf(data["f8"].toUpperCase()) <= 0  && data["f8"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(10).text().toUpperCase().indexOf(data["f9"].toUpperCase()) <= 0  && data["f9"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(11).text().toUpperCase().indexOf(data["f10"].toUpperCase()) <= 0  && data["f10"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(12).text().toUpperCase().indexOf(data["f11"].toUpperCase()) <= 0  && data["f11"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(13).text().toUpperCase().indexOf(data["f12"].toUpperCase()) <= 0  && data["f12"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(14).text().toUpperCase().indexOf(data["f13"].toUpperCase()) <= 0  && data["f13"] != "" ) { $(valuerow).hide(); }
                if ($(valuerow).children("td").eq(15).text().toUpperCase().indexOf(data["f14"].toUpperCase()) <= 0  && data["f14"] != "" ) { $(valuerow).hide(); }

            });

            // Показывать все
            if (data["f1"] == "" && data["f2"] == "" && data["f3"] == "" && data["f4"] == "" && data["f5"] == "" && data["f6"] == "" && data["f7"] == "" && data["f8"] == "" && data["f9"] == "" && data["f10"] == "" && data["f11"] == "" && data["f12"] == "" && data["f13"] == "" && data["f14"] == "") {$("#body-table-events tr").show();}

        })


}














function FilterColumns() {

    // Показывать все
    var show_all = true;

    $("#body-table-events tr").show();

    $.each($("#body-table-events tr"), function( indexrow, valuerow ) {

        $.each($("#head-table-events th input[type=text]"), function( index, value ) {
            if ($(value).val() != "") {

                if ($(valuerow).children("td").eq(index+2).text().toUpperCase().indexOf($(value).val().toUpperCase()) <= 0 ) { $(valuerow).hide(); }

                // Если все поля пустые , то показываем все
                show_all = false;
            }
        });

    });

    if (show_all == true) { $("#body-table-events tr").show(); }




}




/// Раскраска важности
function ColorSeverity() {
    //console.log($("#body-table-events tr td"));
    $.each($("#body-table-events tr td"), function( index,value) {
        //console.log($(value).text());
        if ($.trim($(value).text()) == "Critical") { $(value).css("color","red").css("font-weight","bold"); }
        if ($.trim($(value).text()) == "Warning") { $(value).css("color","#DAA520").css("font-weight","bold"); }
        if ($.trim($(value).text()) == "Error") { $(value).css("color","#B8860B").css("font-weight","bold"); }

    });


}




// Сохранение значений фильтров
function FilterColumnsSave(e) {


        data = {};
        data.action = "save-filter-columns";
        data.f1 = $("#head-table-events th input[type=text]").eq(0).val();
        data.f2 = $("#head-table-events th input[type=text]").eq(1).val();
        data.f3 = $("#head-table-events th input[type=text]").eq(2).val();
        data.f4 = $("#head-table-events th input[type=text]").eq(3).val();
        data.f5 = $("#head-table-events th input[type=text]").eq(4).val();
        data.f6 = $("#head-table-events th input[type=text]").eq(5).val();
        data.f7 = $("#head-table-events th input[type=text]").eq(6).val();
        data.f8 = $("#head-table-events th input[type=text]").eq(7).val();
        data.f9 = $("#head-table-events th input[type=text]").eq(8).val();
        data.f10 = $("#head-table-events th input[type=text]").eq(9).val();
        data.f11 = $("#head-table-events th input[type=text]").eq(10).val();
        data.f12 = $("#head-table-events th input[type=text]").eq(11).val();
        data.f13 = $("#head-table-events th input[type=text]").eq(12).val();
        data.f14 = $("#head-table-events th input[type=text]").eq(13).val();


        var csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });





        $.ajax({
          url: "/monitor/events/jsondata/",
          type: "POST",
          dataType: 'json',
          data:$.toJSON(data),
            success: function(result) {
                FilterColumns();
            }

        })



}