(function ($) {

    $.fn.customInput = function( userSettings ){

        function mirrorCheckedStateWithClasses($input, $label) {
            if($input.is(':checked')) {
                $label.addClass('is-checked');
            } else {
                $label.removeClass('is-checked is-checkedHovered is-checkedFocused');                        
            }
        }

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
                )
                .on('mousedown', function(){
                    label.addClass('is-active');
                })
                .on('mouseup', function(){
                    label.removeClass('is-active');
                });

                // Bind click, focus, blur and custom events.
                input.on('updateState', function(){
                    if (input.is('[type=radio]')) {
                        $('[name="' + input.attr('name') + '"]').each(function(){
                            mirrorCheckedStateWithClasses($(this), $(this).parents('.custom-input_label'));
                        });
                    } else {
                        mirrorCheckedStateWithClasses(input, label);
                    }
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
