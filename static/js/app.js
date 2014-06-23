/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$('.chosen-select').chosen({
    width: '100%',
    no_results_text: 'Oops, nothing found!'
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
   Init jquery.cf_inputSplit
   ========================================================================== */

$('#filter_range_date_gte').cf_inputSplit({
    newHTML: '#filter_range_date_gte-replacement',
    newInputsOrder: ['#filter_from_year', '#filter_from_month'],
    initialValues: $('#filter_range_date_gte input').val().split('-'),
    delimiter: '-'
});

$('#filter_range_date_lte').cf_inputSplit({
    newHTML: '#filter_range_date_lte-replacement',
    newInputsOrder: ['#filter_to_year', '#filter_to_month'],
    initialValues: $('#filter_range_date_lte input').val().split('-'),
    delimiter: '-'
});


/* ==========================================================================
   Init jquery.cf_pagination
   ========================================================================== */

/*
$('body').cf_pagination({
    callback: function(e) {
        var pageNum = getQueryVariable('page', $(e.currentTarget).serialize());
        var newQueryString = replaceQueryVariable('page', pageNum);

        // If replaceQueryVariable returns false it measn that 'page' was not
        // found within the query string. This means we should set 'page'
        // manually.
        if (newQueryString === false) {
            if (getQuery() === false) {
                // There is no current query string in this condition so we need
                // to build our own.
                newQueryString = '?' + $(e.currentTarget).serialize();
            } else {
                // The page query is not present in this condition so let's add
                // it to the existing query string.
                newQueryString = getQuery() + '&' + $(e.currentTarget).serialize();
            }
        }

        // Update the URL
        History.pushState({ page:pageNum }, document.title, newQueryString);

        // Hide the hero if this page is > 1
        if (pageNum > 1) {
            $('.content_hero').hide();
        } else {
            $('.content_hero').show();
        }

        // Scroll to the top of the results
        $('html,body').animate({scrollTop: $('.content_main').offset().top}, 800);
    }
});
*/


/* ==========================================================================
   Utilities
   ========================================================================== */

// Based on http://css-tricks.com/snippets/javascript/get-url-variables/ and
// added optional second argument.

function getQueryVariable(key, queryString) {
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
        if (pair[0] == key) {
            return pair[1];
        }
    }

    return false;
}

function replaceQueryVariable(key, value, queryString) {
    var query;
    var vars;

    if (typeof queryString === 'string') {
        query = queryString;
    } else {
        if (window.location.search.charAt(0) === '?') {
            query = window.location.search.substring(1);
        } else {
            query = window.location.search;
        }
    }

    vars = query.split('&');

    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (pair[0] == key) {
            return '?' + query.replace(
                pair[0] + '=' + pair[1],
                pair[0] + '=' + value
            );
        }
    }

    return false;
}

function getQuery() {
    if (window.location.search.charAt(0) === '') {
        return false;
    } else {
        return window.location.search;
    }
}
