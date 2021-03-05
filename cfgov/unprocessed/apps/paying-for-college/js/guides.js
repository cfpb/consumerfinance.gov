// TODO: Remove jquery.
import $ from 'jquery';

const pfcGuides = ( function() {

    // Make the drop down menus accessible on focus //
    $(".pfc-nav-wrapper").find( "a, .fake-link" ).on( "focus blur", function() {
        $(this).parents().toggleClass( "focus" );
    } );

    // Key questions
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

    // Compare criteria
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


    // Ask bubbles
    // Transparent bubbles pops up answers in tiny modals
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

} )( $ );
