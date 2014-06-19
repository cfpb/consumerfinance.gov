(function ($) {

    $.fn.cf_inputSplit = function(replacement, inputs, delimeter) {
        return $(this).each(function() {
            var inputSplit = {
                $singleInput: $(this),
                $replacementHTML: $(replacement),
                replacementInputs: [],
                delimeter: delimeter,

                init: function() {
                    // Hide the old input and show the new ones
                    this.$singleInput.hide();
                    this.$replacementHTML.show();

                    for (var i = 0; i < inputs.length; i++) {
                        // Create a jQuery object out of each selector and save
                        // it in a new array.
                        var $input = $(inputs[i]);
                        this.replacementInputs[i] = $input;

                        // Remove the name attributes from each replacement input
                        // to prevent their values from affecting the query string.
                        $input.removeAttr('name');

                        // 3. Set up an event listener so we can update the value
                        // of the original input when the new inputs change.
                        $input.on('change', this.onNewInputChange);
                    }
                },

                onNewInputChange: function() {
                    inputSplit.updateOldInputVal();
                },

                updateOldInputVal: function() {
                    this.$singleInput.val(this.getVals());
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
                }
            };

            inputSplit.init();
        });
    };

}(jQuery));
