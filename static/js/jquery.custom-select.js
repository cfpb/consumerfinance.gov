(function ($) {

    $.fn.customSelect = function( userSettings ){

        function getSelectedOptionText($customSelect) {
            return $customSelect.find('option[value="' + $customSelect.find('.custom-select_select').val() + '"]').text();
        }

        function updateSelectText($customSelect) {
            var $text = $customSelect.find('.custom-select_text');
            
            // Update the text
            $text.text(getSelectedOptionText($customSelect));

            // If the value is empty treat it as a placeholder
            if ($customSelect.find('select').val() === '') {
                $text.addClass('custom-select_placeholder');
            } else {
                $text.removeClass('custom-select_placeholder');
            }

            return $text;
        }

        return $(this).each(function(){
            if($(this).has('select')){
                var settings = $.extend({
                        'clickCallback': function(e){}
                    }, userSettings ),
                    changeCallback = settings.clickCallback,
                    $this = $(this),
                    $select = $(this).find('select').addClass('custom-select_select'),
                    $text = $this.append('<span class="custom-select_text"></span>');

                // Add a class to activate the styling
                $this.addClass('is-enabled');
                $select.fadeTo(0, 0);

                // Backfill support for :hover on certain elements.
                $select
                .hover(
                    function(){ $this.addClass('is-hovered'); },
                    function(){
                        $this.removeClass('is-hovered');
                        $this.removeClass('is-focused');
                    }
                )
                .focus(
                    function(){ $this.addClass('is-hovered'); },
                    function(){
                        $this.removeClass('is-hovered');
                        $this.removeClass('is-focused');
                    }
                );

                // Bind click, focus, blur and custom events.
                $select.on('updateState', function(){
                    updateSelectText($(this).parents('.custom-select'));
                })
                .trigger('updateState')
                .on('change', function(){
                    $(this).trigger('updateState');
                    changeCallback({
                        'select': $select
                    });
                })
                .on('focus', function(){
                    $this.addClass('is-focused');
                })
                .on('blur', function(){ $this.removeClass('is-focused'); });
            }
        });
    };

    // Auto init
    $('.custom-select').customSelect();

}(jQuery));
