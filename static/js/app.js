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


/* ==========================================================================
   Init pagination
   ========================================================================== */

$('body').cf_pagination(
    {
        callback: function(e) {
            var pageNum = getQueryVariable('page', $(e.currentTarget).serialize());

            // Update the URL
            History.pushState(
                { page:pageNum },
                'Posts pagination',
                '?' + $(e.currentTarget).serialize()
            );

            // Hide the hero if this page is > 1
            if (pageNum > 1) {
                $('.content_hero').hide();
            } else {
                $('.content_hero').show();
            }

            // Scroll to the top of the results
            $('html,body').animate({scrollTop: $('.content_main').offset().top}, 0);
        }
    }
);


/* ==========================================================================
   Utilities
   ========================================================================== */

// Based on http://css-tricks.com/snippets/javascript/get-url-variables/ and
// added optional second argument.

function getQueryVariable(variable, queryString) {
    var query;
    var vars;

    if (typeof queryString === 'string') {
        query = queryString;
    } else {
        query = window.location.search.substring(1);
    }

    vars = query.split('&');

    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (pair[0] == variable) {
            return pair[1];
        }
    }

    return(false);
}
