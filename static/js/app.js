/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$(".chosen-select").chosen({
    width: '100%',
    no_results_text: "Oops, nothing found!"
});

// Reset buttons sould also reset Chosen.js elements
$('input[type="reset"]').on('click', function() {
    var $this = $(this),
        $form = $this.parents('form'),
        $chosenSelects = $form.find('.chosen-select');
        $chosenSelects.val('').trigger("chosen:updated");
});
