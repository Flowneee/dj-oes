$(document).ready(function() {
    var i_got_it = $("#i-got-it");

    i_got_it.click(function() {
        if ($(this).is(":checked")) {
            $("#reg").removeAttr("disabled");
        } else {
            $("#reg").attr("disabled", "disabled");
        }
    });
});
