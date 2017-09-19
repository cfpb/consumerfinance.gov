var CFPB = CFPB || {};

/**
 * Validation logic for the CFPB Company Portal registration page
 */
CFPB.Register = (function () {
    'use strict';

    var validate;

    /**
     * The master validation function
     *
     * This function handles form-wide validation as well as
     * field-specific validation.
     */
    validate = function (container) {
        var fields, first_field, container_is_valid, form_is_blank;

        container = jQuery(container);
        container_is_valid = true;
        form_is_blank = true;

        if (container[0].tagName === 'FORM') {
            fields = container.find('.field INPUT, .field SELECT').not('.optional');
        } else {
            fields = container.closest('.field').find('INPUT, SELECT').not('.optional');
        }

        // trim all field values and determine whether the form is blank
        fields.each(function () {
            var element;
            element = jQuery(this);
            element.val(jQuery.trim(element.val()));
            if (element.val() !== '' && container[0].tagName === 'FORM') {
                form_is_blank = false;
            }
        });

        // focus the first field if we're validing the entire form and it is blank
        if (form_is_blank && container[0].tagName === 'FORM') {
            first_field = fields.first();
            first_field.closest('.field').find('DIV.error').show();
            first_field.closest('.field').find('.icon').removeClass('icon-ok').addClass('icon-error');
            first_field.addClass('error');
            first_field.focus();
            return false;
        }

        // validate fields individually
        fields.each(function () {
            var element, rules, field_is_valid, i, segments, rule_name, rule_args;

            field_is_valid = true;

            element = jQuery(this);
            element.removeClass('error');
            element.closest('.field').find('DIV.error').hide();
            element.closest('.field').find('.icon').removeClass(['icon-ok', 'icon-error']);

            // data validation rules are extracted from the
            // data-validation attribute, and should be a comma
            // delimited list. If a rule specifies an argument,
            // it is separated from the rule name by a hypen.
            rules = element.attr('data-validation') || '';
            rules = rules.split(',');

            for (i = 0; i < rules.length; i = i + 1) {

                segments = rules[i].split('-');

                rule_name = segments.shift();

                if (segments.length > 0) {
                    rule_args = segments;
                } else {
                    rule_args = [];
                }

                if (rule_name === 'min') {
                    if (element.val().length < parseInt(rule_args[0], 10)) {
                        field_is_valid = false;
                    }
                }

                if (rule_name === 'numeric') {
                    element.val(element.val().replace(/\D+/g, ''));
                    if (element.val().length < parseInt(rule_args[0], 10)) {
                        field_is_valid = false;
                    }
                }

                if (rule_name === 'email') {
                    if (element.val().length < 3) {
                        field_is_valid = false;
                    }

                    if (element.val().indexOf('@') === -1) {
                        field_is_valid = false;
                    }
                }
            }

            if (field_is_valid) {
                element.closest('.field').find('.icon').removeClass('icon-error').addClass('icon-ok');
            } else {
                element.closest('.field').find('DIV.error').show();
                element.closest('.field').find('.icon').removeClass('icon-ok').addClass('icon-error');
                element.addClass('error');
                container_is_valid = false;
            }
        });

        if (!container_is_valid) {
            container.find('INPUT.error, SELECT.error').first().focus();
        }

        return container_is_valid;
    };

    return {
        init: function () {

            // Replace the state dropdown with a fancy equivalent
            jQuery('FIELDSET SELECT').select2();

            // Trigger validation from the certification checkbox and
            // activate the submit button. The two are not dependant.
            jQuery('#reg-certify INPUT[type=checkbox]').on('click', function () {
                var form, checkbox, submit;
                form = jQuery('#reg-form');
                checkbox = jQuery(this);
                submit = jQuery('#reg-submit-button');
                if (checkbox.is(':checked')) {
                    if (validate(form) === true) {
                        submit.removeClass('inactive-button');
                    }

                    // Keep checking the form's validity. Now that the
                    // certification checkbox is checked, we won't
                    // have an explicit click event to rely on. But we
                    // still want to active the submit button once the
                    // form becomes valid.
                    timer = setInterval(function () {
                        if (validate(form, false) === true) {
                            submit.removeClass('inactive-button');
                        }
                    }, 750);
                } else {
                    submit.addClass('inactive-button');
                }
                validate(form);
            });

            // Trigger validation when submitting the form
            jQuery('#reg-form').on('submit', function (e) {
                if (jQuery('#reg-submit INPUT.button').hasClass('inactive-button')) {
                    e.preventDefault();
                    return;
                }

                if (validate(this) === false) {
                    e.preventDefault();
                } else {
                var serialized_data = $('#reg-form').serialize();
                $.post('',serialized_data, function(){
                    jQuery('#reg-success').show();
                    jQuery('#reg-form').hide();
                    jQuery('BODY').animate({scrollTop: jQuery('#reg-success').offset().top});
                })
                e.preventDefault();
                }
            });

            // Trigger validation when exiting a form field
            jQuery('#reg-form .textbox').on('blur', function () {
                validate(this);
            });

            // Display the success screen based on the querystring.
            // This logic doesn't particularly need to happen
            // client-side, it was just convenient.
        }
    };
}());

jQuery(document).ready(CFPB.Register.init);
