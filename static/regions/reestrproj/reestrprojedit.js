$(document).ready(function() {


    // Управление закладками
    $("ul.nav-tabs li a").bind("click",ChangeNav);

    // маска ввода
    $("form#reestr-proj-edit #id_proj_kod").mask("99/9999999/99999999/99", {placeholder:" "});


});






// Переключение закладок
function ChangeNav(e) {



    $("#nav-1").toggleClass("active",false);
    $("#nav-2").toggleClass("active",false);
    $("#nav-3").toggleClass("active",false);
    $("#nav-4").toggleClass("active",false);

    $(this).parent("li").toggleClass("active",true);

    $("#page-1").hide();
    $("#page-2").hide();
    $("#page-3").hide();
    $("#page-4").hide();


    // Название отображаемой страницы (на закладке)
    var a = $(this).parent("li").attr("id").split("-");
    b = "#page-"+a[1];
    $(b).show();

}

