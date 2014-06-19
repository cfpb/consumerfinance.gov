(function ($) {

    $.fn.cf_inputSplit = function(replacement, inputs, delimeter) {
        return $(this).each(function() {
            var inputSplit = {
                $oldHTML: $(this),
                $replacementHTML: $(replacement),
                $oldInput: $(),
                replacementInputs: [],
                delimeter: delimeter,
                formElementSelectors: 'input, select, textarea',

                init: function() {
                    // This plugin can be called on an input or an ancestor of
                    // an input. This means we need to do a little work to
                    // figure out what the original form input is.
                    this.$oldInput = this.getFormElements(this.$oldHTML);

                    // Hide the old input and show the new ones
                    this.$oldInput.hide();
                    this.$replacementHTML.show();

                    for (var i = 0; i < inputs.length; i++) {
                        // Create a jQuery object out of each selector and save
                        // it in a new array.
                        var $input = $(inputs[i]);
                        this.replacementInputs[i] = $input;

                        // 3. Set up an event listener so we can update the value
                        // of the original input when the new inputs change.
                        $input.on('change', this.onNewInputChange);
                    }
                },

                onNewInputChange: function() {
                    inputSplit.updateOldInputVal();
                },

                updateOldInputVal: function() {
                    this.$oldInput.val(this.getVals());
                },

                getVals: function() {
                    // Create an array of the values from each new input.
                    var vals = [];
                    for (var i = 0; i < inputs.length; i++) {
                        var val = this.replacementInputs[i].val();
                        if (val !== '') {
                            vals.push(val);
                        }
                    }

                    // If there is more than one non-empty value then
                    // join them together using the custom delimeter.
                    // If there is only one non-empty value return it.
                    if (vals.length > 1) {
                        return vals.join(this.delimeter);
                    } else {
                        return vals[0];
                    }
                },

                getFormElements: function($html) {
                    // If $html is a form element then return it.
                    // If it's not then return any form elements inside of it.
                    if ($html.is(this.formElementSelectors)) {
                        return $html;
                    } else {
                        return $html.find(this.formElementSelectors);
                    }
                }
            };

            inputSplit.init();
        });
    };

}(jQuery));
