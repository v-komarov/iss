$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // маска ввода
    $("form#reestr-proj-edit #id_proj_kod").mask("99/9999999/99999999/99", {placeholder:" "});

    // Виджет для даты
    $("dl dd #id_date_service").datepicker($.datepicker.regional['ru']);

    // Список загруженных файлов
    GetListHdfsFiles();

    // Удаление загруженного в hdfs файла
    $("#page-4 table[group=file-list] tbody").on("click", "a[delete-file]", DeleteHDFSFile);



});




// Очистка поля ввода загружаемого файла
function ClearUploadP2() {

    $("form#uploadfile input#upload_file").val("");

}




// Очистка поля ввода загружаемого файла
function ClearUploadP4() {

    $("form#uploadfilehdfs input#fileuploadhdfs").val("");

}




// Удаление загруженного в hdfs файла
function DeleteHDFSFile(e) {

    var file_id = $(this).parents("tr").attr("file_id");
    var filename = $(this).parents("tr").attr("filename");
    var deletefile = confirm("Удаляем "+filename+" ?");

    if (deletefile) {

        var jqxhr = $.getJSON("/regions/jsondata/?action=reestrproj-hdfs-delete-file&file_id="+file_id,
        function(data) {

            if (data["result"] == "ok") { GetListHdfsFiles(); }

        })

    }


}






// Список загруженных в hdfs файлов
function GetListHdfsFiles() {

    var reestrproj_id = $("div#proj-common").attr("reestrproj_id");

    var jqxhr = $.getJSON("/regions/jsondata/?action=get-reestrproj-hdfs-files&reestrproj_id="+reestrproj_id,
    function(data) {

        if (data["result"] == "ok") {

            // Отображение списка загруженных файлов
            $("table[group=file-list] tbody").empty();
            $.each(data["data"], function(key,value) {


                var t = "<tr file_id=" + value["file_id"] +" "+ "filename="+value["filename"]+">"
                +"<td>"+value['date']+"</td>"
                +"<td><a href=\"/regions/reestrproj/readfile?file_id="+value["file_id"]+"&file_name="+value["filename"]+"\" >"+value['filename']+"</a></td>"
                +"<td>"+value['user']+"</td>"
                +"<td><a delete-file><span class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></span></a></td>"
                +"</tr>";

                $("table[group=file-list] tbody").append(t);

            });



        }

    })


}







// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);
    $("#nav-5").toggleClass("active",false);
    $("#nav-6").toggleClass("active",false);
    //$("#nav-7").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();
    $("#page-5").hide();
    $("#page-6").hide();
    //$("#page-7").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

