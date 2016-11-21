$(document).ready(function() {

    $("#user-settings").bind("click",UserSettings);
    $("#head-order tbody tr").bind("click",MarkTableOrder);
    $("#head-order-up").bind("click",HeadOrderUp);
    $("#head-order-down").bind("click",HeadOrderDown);


});





function MarkTableOrder(e) {
    $("#head-order tbody tr").css("background","");
    $("#head-order tbody tr").attr("marked","no")
    $(this).css("background","#ADD8E6");
    $(this).attr("marked","yes");
}



// Вверх
function HeadOrderUp(e) {

    var up = $("#head-order tbody tr[marked=yes]");
    var index_up = $("#head-order tbody tr").index(up);
    var prev = index_up - 1;

    if (prev >= 0) {
        var down = $("#head-order tbody tr").eq(prev);
        $("#head-order tbody tr").eq(prev).remove();
        $("#head-order tbody tr").eq(prev).after(down);
    }

    $("#head-order tbody tr").bind("click",MarkTableOrder);


}



// Вниз
function HeadOrderDown(e) {
    var count = $("#head-order tbody tr").length - 1;

    var down = $("#head-order tbody tr[marked=yes]");
    var index_down = $("#head-order tbody tr").index(down);
    var next = index_down + 1;

    if (next <= count) {
        var up = $("#head-order tbody tr").eq(next);
        $("#head-order tbody tr").eq(next).remove();
        $("#head-order tbody tr").eq(index_down).before(up);
    }

    $("#head-order tbody tr").bind("click",MarkTableOrder);


}




// Settings
function UserSettings(e) {


    $("#usersettings").dialog({
          title:"Настройки",
          show: {
            effect: "blind",
            duration: 100
          },
          hide: {
            effect: "blind",
            duration: 1500
          },
          buttons: [{text:"Закрыть", click: function() { $(this).dialog("close")}}],
          modal:true,
          minWidth:200,
          width:400,
          height:400

    });


}

