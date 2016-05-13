$(function(){
    $('.ec').click(function(e) {
        var rel = $(this).attr('rel');
    	var accordion = $(this).closest('.accordion');
    	if (typeof rel === 'undefined') {
    		accordion.children('.accordion-item').toggle();
    	} else {
    		accordion.children(".accordion-item[id!='"+rel+"']").hide();
    		$(".ec[rel!='"+rel+"']").removeClass('collapse');
    		$('#'+rel).toggle();
    	}
    	$(this).toggleClass('collapse');
    	e.preventDefault();
    });
    
    $('.accordion-item').hide();
});