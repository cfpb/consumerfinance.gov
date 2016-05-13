/**
 * Transparent bubbles pops up answers in tiny modals
 */

$(function(){
    $('.bubble-top-text').click(function(){
        var $this = $(this),
            $bubble_transparent = $this.parent();
            
        if($bubble_transparent.hasClass('bubble-transparent-selected')){
            $this.closest('.bubble-space').find('.bubble-transparent-answer').hide();
            $bubble_transparent.removeClass('bubble-transparent-selected');            
        }else{
            $this.closest('.bubble-space').find('.bubble-transparent-answer').show();
            $bubble_transparent.addClass('bubble-transparent-selected');
        }
    });

    $('.btn-close').click(function(e){
        var $bubble_space = $(this).closest('.bubble-space');
        $bubble_space.find('.bubble-transparent-selected').removeClass('bubble-transparent-selected');
        $bubble_space.find('.bubble-transparent-answer').hide();
    	e.preventDefault();
    });
});

