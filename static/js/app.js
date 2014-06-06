/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$(".chosen-select").chosen({
    width: '100%',
    no_results_text: "Oops, nothing found!"
});

// Reset buttons sould also reset Chosen.js elements
$('.js-form_clear').on('click', function() {
    var $this = $(this),
        $form = $this.parents('form');

    // Reset checkboxes
    $form.find('[type="checkbox"]')
    .removeAttr('checked');
    
    // Reset select options
    $form.find('select option')
    .removeAttr('selected');
    $form.find('select option:first')
    .attr('selected', true);
    
    // Reset Chosen.js elements
    $form.find('.chosen-select')
    .val('')
    .trigger("chosen:updated");
});

// Custom checkboxes

(function ($) {

    $.fn.customInput = function( userSettings ){
        return $(this).each(function(){
            if($(this).is('[type=checkbox],[type=radio]')){
                var settings = $.extend({
                        'clickCallback': function(e){}
                    }, userSettings ),
                    clickCallback = settings.clickCallback,
                    input = $(this),
                    label = input.siblings('label[for="'+input.attr('id')+'"]').addClass('input_label'),
                    labelText = label.text(),
                    wrapper = input.parents('.input');

                // Add a class that activates the styling
                wrapper.addClass('is-enabled');

                // add a fake input we can style
                label.after('<span class="input_' + input.attr('type') + '"></span>');

                // move the label text from the label to a child span that we need to add extra styling
                label.text('');
                label.append('<span class="input_text">' + labelText + '</span>');

                // necessary for browsers that do not support the :hover pseudo class on divs
                wrapper.hover(
                    function(){ wrapper.addClass('is-hovered'); },
                    function(){ wrapper.removeClass('is-hovered'); }
                );

                //bind custom event, trigger it, bind click,focus,blur events                   
                input.on('updateState', function(){
                    input.is(':checked') ? wrapper.addClass('is-checked') : wrapper.removeClass('is-checked is-checkedHovered is-checkedFocused');
                })
                .trigger('updateState')
                .on('click', function(){
                    $('input[name="'+ $(this).attr('name') +'"]').trigger('updateState');
                    clickCallback({
                        'input': input,
                        'label': label,
                        'wrapper': wrapper
                    });
                })
                .on('focus', function(){
                    wrapper.addClass('is-focused');
                    if( input.is(':checked') ){
                        wrapper.addClass('is-checkedFocus');
                    }
                })
                .on('blur', function(){ wrapper.removeClass('is-focused is-checkedFocused'); });
            }
        });
    };

    // Auto init
    $('.input input').customInput();

}(jQuery));
