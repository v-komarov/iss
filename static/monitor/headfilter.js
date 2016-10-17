$(document).ready(function() {

    $("#th_first_seen_i").hide();

    //$("#th_first_seen_l").bind("click",FirstSeenL);
    //$("#th_first_seen_i").bind("dbclick",FirstSeenI);

});


function FirstSeenL(e) {

    $("#th_first_seen_l").toggle(false);
    $("#th_first_seen_i").toggle(true);

}



function FirstSeenI(e) {

    $("#th_first_seen_l").toggle(true);
    $("#th_first_seen_i").toggle(false);

}