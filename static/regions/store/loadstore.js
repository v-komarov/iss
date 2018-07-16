$(document).ready(function() {






});







// Очистка поля ввода загружаемого файла
function ClearUploadEisup() {

    $("form#uploadfileeisup input#fileupload").val("");
    $("#uploadform").hide();
    $("#param").show();
    $("#param2").show();

    GetTableData();

}




// Содержимое таблицы
function GetTableData() {

    var frame = $("#uploadframe").contents();
    var table = frame.contents().find("table");
    console.log(frame);

}

