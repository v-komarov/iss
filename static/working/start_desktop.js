$(document).ready(function() {

    // Сообщение о регистрации IP
    SaveIP();


});



// Показать зарегистрированный IP
function SaveIP() {

    $("#ip-ok").dialog({show: { effect: "blind", duration: 500 }, hide: { effect: "explode", duration: 4000 }});
    $("#ip-ok").dialog("close");

}


