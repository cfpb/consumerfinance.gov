$(function(){
    $('.bubbles').each(function(i, n){
		var $bubbles = $(n);
		$bubbles.find('.bubble').click(function(){
			var target_id = $(this).attr('rel');
            document.location.hash = '#' + $(this).attr('_id');

			// update the selected bubble
			$bubbles.find('.bubble.bubble-active').removeClass('bubble-active');
			$(this).addClass('bubble-active');
            

			// update the bubble texts
			
            $bubbles.find('.answer-box .bubble-active').removeClass('bubble-active');
			$bubbles.find('.answer-box #' + target_id).addClass('bubble-active');
            
		});
	});
    
    var cur_hash = document.location.hash.replace("#","");
    
    if(cur_hash)
        $('#_' + cur_hash).click();
    else
        $('.bubbles .bubble').first().click();
    
    $(window).bind("hashchange",function(e){
        $('#_' + document.location.hash.replace("#","")).click();
    });
});

