var CFPBComparisonFeedback = (function() {
    $('#feedback-container button').attr('disabled', true);

    $(document).ready(function() {
        $('#feedback-container').on('keyup', 'textarea', function() {
            if ( $(this).val() != "" ) {
                $('#feedback-container button').removeAttr('disabled');            
            }
            else {
                $('#feedback-container button').attr('disabled', true);
            }
        });
    });

})(jQuery); 