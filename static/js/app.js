/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$(".chosen-select").chosen({
    width: '100%',
    no_results_text: "Oops, nothing found!"
});


/* ==========================================================================
   Clear form button
   - Clear checkboxes and selects
   - Clear Chosen.js elements
   - Clear jquery.custom-input elements
   ========================================================================== */

$('.js-form_clear').on('click', function() {
    var $this = $(this),
        $form = $this.parents('form');

    // Clear checkboxes
    $form.find('[type="checkbox"]')
    .removeAttr('checked');
    
    // Clear select options
    $form.find('select option')
    .removeAttr('selected');
    $form.find('select option:first')
    .attr('selected', true);
    
    // Clear .custom-input elements
    $form.find('.custom-input')
    .trigger('updateState');

    // Clear Chosen.js elements
    $form.find('.chosen-select')
    .val('')
    .trigger('chosen:updated');
});

