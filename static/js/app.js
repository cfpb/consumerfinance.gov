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
    
    // Reset .custom-input elements
    $form.find('.custom-input').trigger('updateState');

    // Reset Chosen.js elements
    $form.find('.chosen-select')
    .val('')
    .trigger("chosen:updated");
});
