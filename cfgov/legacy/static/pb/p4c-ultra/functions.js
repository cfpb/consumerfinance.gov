$(document).ready(function() {
    setTimeout(function(){
    $('#wizroot a, #wiz_templates a').each(function(i, n){
        var $n=$(n);
        $n.attr('target', '_blank');
    });
}, 500);

    $(".tooltip-info").click( function(event) {
    event.stopPropagation();
    // position tooltip-container based on the element clicked
        var thisoff = $(this).offset();
        var ttc = $("#tooltip-container");
        ttc.show();
        ttc.css(
            {"left": (thisoff.left + 10) + "px",
            "top": (thisoff.top + $(this).height() + 5) + "px"});
        var ttcoff = ttc.offset();
        var right = ttcoff.left + ttc.outerWidth(true);
        if (right > $(window).width()) {
            var left = $(window).width() - ttc.outerWidth(true) - 20;
            ttc.offset({"left": left});
        }
        // check offset again, properly set tips to point to the element clicked
        ttcoff = ttc.offset();
        var tipset = Math.max(thisoff.left - ttcoff.left, 0);
        ttc.find("#innertip").css("left", (tipset + 8));
        ttc.find("#outertip").css("left", (tipset + 5));
        $("#tooltip-container > p").html($(this).attr("tooltip"));

        $("html").on('click', "body", function() {
            $("#tooltip-container").hide();
            $("html").off('click');
		});
    });
});
