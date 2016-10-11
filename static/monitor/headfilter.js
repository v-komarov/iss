$(document).ready(function() {

    $("table[group=events] thead tr th").bind("click",FirstSeenL);
    //$("table[group=events] thead tr th #th_first_seen_i").bind("click",FirstSeenI);

});


function FirstSeenL(e) {

    console.log("dsfdfdf");
    //$("table[group=events] thead tr th #th_first_seen_l").toggle(false);
    //$("table[group=events] thead tr th #th_first_seen_i").toggle(true);

}



function FirstSeenI(e) {

    $("table[group=events] thead tr th div#th_first_seen_l").toggle(true);
    $("table[group=events] thead tr th div#th_first_seen_i").toggle(false);

}