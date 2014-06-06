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
                    input = $(this).addClass('custom-input_input'),
                    label = input.parents('label').addClass('custom-input_label'),
                    labelText = label.text();

                // Add a class to activate the styling
                label.addClass('is-enabled');

                // Wrap the label text for extra styling
                label.html('');
                label.append('<span class="custom-input_text">' + labelText + '</span>');
                label.append(input);

                // Add a simple element to act as our new visual input.
                // This will give us complete styling control.
                label.append('<span class="custom-input_' + input.attr('type') + '"></span>');

                // Backfill support for :hover on certain elements.
                label.hover(
                    function(){ label.addClass('is-hovered'); },
                    function(){
                        label.removeClass('is-hovered');
                        label.removeClass('is-focused');
                        label.removeClass('is-checkedFocused');
                    }
                );

                // Bind click, focus, blur and custom events.
                input.on('updateState', function(){
                    input.is(':checked') ? label.addClass('is-checked') : label.removeClass('is-checked is-checkedHovered is-checkedFocused');
                })
                .trigger('updateState')
                .on('click', function(){
                    $(this).trigger('updateState');
                    clickCallback({
                        'input': input,
                        'label': label
                    });
                })
                .on('focus', function(){
                    label.addClass('is-focused');
                    if( input.is(':checked') ){
                        label.addClass('is-checkedFocus');
                    }
                })
                .on('blur', function(){ label.removeClass('is-focused is-checkedFocused'); });
            }
        });
    };

    // Auto init
    $('.custom-input').customInput();

}(jQuery));
