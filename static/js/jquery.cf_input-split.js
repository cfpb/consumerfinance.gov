(function ($) {

    /* ==========================================================================
       jquery.cf_inputSplit

       Takes multiple form field values and moves them to a single field.
       Useful for query strings that require one field-value pair that need to
       be created from multiple form fields.

       Setup:

       1. Use a single form field that can serve as your intial non-JavaScript
       solution. This form field should be able to submit the appropriate
       query on its own. For example if you need to submit the field-value pair
       of `date=2014-01` then use a simple input[type="text"] form field.

       2. Create the multiple input replacements and make sure that they do NOT
       have name attributes. This will prevent the replacement fields from
       submitting along with the form and affecting the query string. This is
       especially important for the non-JavaScript fallback.

       The multiple field replacements should be wrapped in a container and
       added to the HTML as a direct sibling to the single field. If this is not
       possible then use the `newHTML` option to specify a jQuery selector.

       Hide this container using `style="display:none;"`.

       3. That's it! Call the plugin like this `$('#myfield').cf_fieldSplit();`
       and the single field is hidden, and replacement fields are shown.

       Whenever one of the replacement fields fires a `change` event the plugin
       will replace the value of the hidden single field with the concatenated
       values of the replacement fields. When the form is submitted only the
       hidden single field will affect the query string.

       Options:

       newHTML: Targets the container holding the replacement fields. If this
       options is not set then the next sibling to the single field is assumed
       to be the container with the replacement fields.

           $('#myfield').cf_fieldSplit({
               newHTML: '#myfield-replacement'
           });

       newInputsOrder: Targets and orders the values of the replacement fields.
       For example if you need `year` to come before `month` in your field value
       but the fields are ordered differently in the markup you can specify the
       order.

           $('#myfield').cf_fieldSplit({
               newInputsOrder: ['#year', '#month']
           });
       
       delimiter: Sets the delimiter when concatenating the values of the
       replacement fields. Defaults to `-`.

           $('#myinput').cf_inputSplit({
               delimiter: '.'
           });

       initialValues: Sets the selected state for each replacement field.
       Currently only select elements are supported.

           $('#myinput').cf_inputSplit({
               initialValues: ['2014', '01']
           });

       ========================================================================== */

    $.fn.cf_inputSplit = function(userOptions) {
        return this.each(function() {

            var options = $.extend({
                newHTML: '',
                newInputsOrder: [],
                initialValues: [],
                delimiter: '',
                genericFields: 'input, select, textarea'
            }, userOptions);

            var inputSplit = {
                $oldHTML: $(this),
                $newHTML: $(options.newHTML),
                $oldInput: $(),
                newInputs: options.newInputsOrder,
                initialValues: options.initialValues,
                delimiter: options.delimiter,
                genericFields: options.genericFields,

                init: function() {
                    // Assume what the new HTML is...
                    // but only if it has not been specified.
                    if (this.$newHTML.size() === 0) {
                        this.$newHTML = this.$oldHTML.next();
                    }

                    // This plugin can be called on an input or an ancestor of
                    // an input. This means we need to do a little work to
                    // figure out what the original form input is.
                    this.$oldInput = this.getFormElements(this.$oldHTML);

                    // Assume the new inputs and their order...
                    // but only if it has not been specified.
                    // The order is important which is why we're saving the
                    // new inputs in an array instead of a jQuery collection.
                    // The values for each new input will get concatenated to
                    // create a new single value to send back to the old input.
                    if (this.newInputs.length === 0) {
                        this.newInputs = this.getFormElements(this.$newHTML).toArray();
                    } else {
                        // If the new inputs have been specified then we need
                        // to loop through them and grab the DOM element for
                        // each selector.
                        for (var i = 0; i < this.newInputs.length; i++) {
                            this.newInputs[i] = $(this.newInputs[i])[0];
                        }
                    }

                    // Now that we have an array of new inputs we can loop
                    // through them and add stuff.
                    for (var i = 0; i < this.newInputs.length; i++) {
                        var $input = $(this.newInputs[i]);

                        // Attach an event listener to the new inputs so we can
                        // update the value of the old input whenever a new input
                        // changes. Note: we need to use `inputSplit` instead of
                        // `this` because it's getting called from the scope of
                        // this.newInputs.
                        $input.on('change', inputSplit.onNewInputChange);

                        // Add an intial value if one was specified.
                        // Currently only select elements are supported.
                        if ($input.is('select')) {
                            $input.find('option').each(function(){
                                if ($(this).val() === inputSplit.initialValues[i]) {
                                    $(this).prop('selected', true);
                                    $(this).attr('selected', true);
                                }
                            });
                        }
                    }

                    // Hide the old input and show the new ones
                    this.$oldHTML.hide();
                    this.$newHTML.show();
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
                    for (var i = 0; i < this.newInputs.length; i++) {
                        var val = $(this.newInputs[i]).val();
                        if (val !== '') {
                            vals.push(val);
                        }
                    }

                    // If there is more than one non-empty value then
                    // join them together using the custom delimiter.
                    // If there is only one non-empty value return it.
                    if (vals.length > 1) {
                        return vals.join(this.delimiter);
                    } else {
                        return vals[0];
                    }
                },

                getFormElements: function($html) {
                    // If $html is a form field then return it.
                    // If it's not then return any form fields inside of it.
                    if ($html.is(this.genericFields)) {
                        return $html;
                    } else {
                        return $html.find(this.genericFields);
                    }
                }
            };

            inputSplit.init();
        });
    };

}(jQuery));
