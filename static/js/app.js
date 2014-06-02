/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$(".chosen-select").chosen({
    width: '100%',
    no_results_text: "Oops, nothing found!"
});

// Reset buttons sould also reset Chosen.js elements
$('input[type="reset"]').on('click', function() {
    $(this)
    .parents('form')
    .find('.chosen-select')
    .val('')
    .trigger("chosen:updated");
});
