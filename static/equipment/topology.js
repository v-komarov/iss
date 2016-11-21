$(document).ready(function() {

    $("#select-domen").val("");

    ClearSelects();

    // Выбр домена
    $( "#select-domen" ).change(function() {
        var domen = $(this).val();
        ClearSelects();
        $('#select-footnode option').each(function(){
            if ($(this).attr("domen") == domen) {
                $(this).show();
            }
        });

    });

    // Выбор опорного узла
    $( "#select-footnode" ).change(function() {
        var footnode = $(this).val();

        $("#select-agregator option").each(function(){ $(this).hide(); })
        $('#select-agregator option').each(function(){
            if ($(this).attr("footnode") == footnode) {
                $(this).show();
            }
        });

    });



});




function ClearSelects() {

    // Выбор по опорному узлу и агрегатору первоначально очистить список
    $("#select-footnode").val("");
    $("#select-footnode option").each(function(){ $(this).hide(); });
    $("#select-agregator").val("");
    $("#select-agregator option").each(function(){ $(this).hide(); });


}