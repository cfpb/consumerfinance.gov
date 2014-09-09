/* ==========================================================================
   Nav-secondary
   ========================================================================== */

$(document).ready(function(){
    // This needs to be in document ready because that is when the jquery plugins
    // are instantiated.

    // Call this right away to test on document ready if we need to expand the nav.
    navSecondaryToggle();

    // Then on window resize check to see when we need to toggle the nav.
    $(window).resize(function() {
        navSecondaryToggle();
    });

    // Tests whether or not the secondary nav should be toggled.
    function navSecondaryToggleTest() {
        var isSmall = $('.nav-secondary .nav-secondary_link__button').is(':visible'),
            isExpanded = $('.nav-secondary .expandable_content').attr('aria-expanded') === 'true';
        return isSmall && isExpanded || !isSmall && !isExpanded;
    }

    function navSecondaryToggle() {
        if (navSecondaryToggleTest()) {
            $('.nav-secondary .expandable_target').trigger('click');
        }
    }
});


/* ==========================================================================
   Reveal on focus
   ========================================================================== */

$('.reveal-on-focus')
    .find('.reveal-on-focus_content').hide()
    .end()
    .find('.reveal-on-focus_target').on('focus', function() {
        $(this).parents('.reveal-on-focus').find('.reveal-on-focus_content').slideDown();
    });


/* ==========================================================================
   Init Contact us filtering
   ========================================================================== */

$('.type-and-filter').typeAndFilter({
   $input: $('.js-type-and-filter_input'),
   $items: $('.js-type-and-filter_item'),
   $button: $('.js-type-and-filter_button'),
   $clear: $('.js-type-and-filter_clear'),
   $messages: $('.js-type-and-filter_message'),
   allMessage: 'Showing all {{ count }} contacts.',
   filteredMessageSingular: 'There is 1 contact result for "{{ term }}".',
   filteredMessageMultiple: 'There are {{ count }} contact results for "{{ term }}".'
});

// Helpful filter terms
$('.js-helpful-term').on( 'click', function () {
    $('.js-type-and-filter_input').val( $( this ).text() );
    $('.type-and-filter').trigger('attemptSearch');
});

// On small screens provide a button to expand the contact list, which is hidden by default.
$('#contact-list_btn').click(function () {
   $(this).hide();
   $('#contact-list').slideDown();
});


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

    // Clear text inputs
    $form.find('input[type="text"]').val('');

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

    // Clear .custom-select elements
    $form.find('.custom-select_select')
    .trigger('updateState');

    // Clear Chosen.js elements
    $form.find('.chosen-select')
    .val('')
    .trigger('chosen:updated');
});


/* ==========================================================================
   Init jquery.cf_inputSplit
   ========================================================================== */

if ($('#filter_range_date_gte-container').length > 0) {
    $('#filter_range_date_gte-container').cf_inputSplit({
        newHTML: '#filter_range_date_gte-replacement',
        newInputsOrder: ['#filter_from_year', '#filter_from_month'],
        initialValues: $('#filter_range_date_gte').val().split('-'),
        delimiter: '-'
    });
}

if ($('#filter_range_date_lte-container').length > 0) {
    $('#filter_range_date_lte-container').cf_inputSplit({
        newHTML: '#filter_range_date_lte-replacement',
        newInputsOrder: ['#filter_to_year', '#filter_to_month'],
        initialValues: $('#filter_range_date_lte').val().split('-'),
        delimiter: '-'
    });
}

$('#filter_from_year, #filter_from_month, #filter_to_year, #filter_to_month')
.trigger('updateState');


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
   #post-filters-form validation
   ========================================================================== */

function validDateRange(date1, date2) {
   return date2.getTime() > date1.getTime();
}

$('#post-filters-form').on('submit', function(e) {
    // Check the date range values.
    // If the from (gte) date is larger than the to (lte) date then swap them.
    var validDate = validDateRange(
        new Date(Date.parse($('#filter_range_date_gte').val())),
        new Date(Date.parse($('#filter_range_date_lte').val()))
    );
    if (!validDate) {
        // Swap the values
        var gteVal = $('#filter_range_date_gte').val();
        var lteVal = $('#filter_range_date_lte').val();
        $('#filter_range_date_gte').val(lteVal);
        $('#filter_range_date_lte').val(gteVal);
    }
});


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
