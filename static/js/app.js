'use strict';

/*
 * ======================================================================
 * Aria Button
 * ======================================================================
 */

$.fn.cfpbAriaButton = function( userSettings ) {

    return this.each(function() {

        var $this = $( this );

        // Add aria attributes
        $this.attr( 'role', 'button' );
        $this.attr( 'aria-pressed', 'false' );
        $this.attr( 'tabindex', '0' );

        // Toggle the aria-pressed attribue
        $this.click(function() {
            togglePressedVal( $this );
        });
        $this.keyup(function(event) {
            // Space key
            if ( event.which === 32 ) {
                event.preventDefault();
                togglePressedVal( $this );
            }
        });
        // Prevent the spacebar from scrolling the page
        $this.keydown(function(event) {
            // Space key
            if ( event.which === 32 ) {
                event.preventDefault();
            }
        });
    });

    function togglePressedVal( jqueryObject ) {
        var toggledPressedVal = toggleBoolean( jqueryObject.attr( 'aria-pressed' ) );
        jqueryObject.attr( 'aria-pressed', toggledPressedVal );
    }

};

function toggleBoolean( userBoolean ) {
    var typedBoolean;
    if ( typeof userBoolean === 'boolean' ) {
        typedBoolean = userBoolean;
    } else if ( typeof userBoolean === 'string' ) {
        typedBoolean = ( userBoolean === 'true' ) ? true : false;
    }
    return !typedBoolean;
}


/* ==========================================================================
   Sliding/Pushing Menu
   ========================================================================== */

$(function() {

    var $body = $('body'),
        $slidingNav = $('.sliding-nav'),
        $slidingNavTrigger = $('.sliding-nav_trigger'),
        $slidingNavNav = $('.sliding-nav_nav'),
        $slidingNavPage = $('.sliding-nav_page'),
        $slidingNavPageOverlay = $('.sliding-nav_page-overlay');

    $slidingNavTrigger.click(function( e ) {
        e.preventDefault();

        // First deal with the filters button if it exists.
        if ( $('.l-sidenav').hasClass('is-open') ) {
            $('.l-sidenav-btn').trigger('click');
        }

        if ( $slidingNav.hasClass('is-open') ) {
            window.setTimeout( function() {
                $slidingNavPage.removeClass('is-scroll-disabled');
            }, 200 );
            $slidingNav.removeClass('is-open');
            $slidingNavPageOverlay.off('click');
        } else {
            $slidingNav.addClass('is-open');
            $(window).scroll( slidingNavStopScroll );
            $slidingNavPageOverlay.click( function( evt ) {
                evt.preventDefault();
                $( $slidingNavTrigger[0] ).trigger('click');
            });
        }
        $body.scrollTop( 0 );
    });

    function slidingNavStopScroll () {
        if ( parseInt($slidingNavPage.css('margin-right'), 10) < 0 ) {
            $slidingNavPage.addClass('is-scroll-disabled');
            $slidingNavNav.css( 'min-height', $(window).height() );
            $(window).off('scroll', slidingNavStopScroll);
        }
    }



    // Expanding list
    // TODO: Determine if we should actually use the cfpbAriaButton plugin.
    $('.list-expanding_trigger').cfpbAriaButton();
    $('.list-expanding_trigger').click( function( e ) {
        e.preventDefault();
        $(this).next().find('.list-expanding_child-list').slideToggle(100);
    });
    $('.list-expanding_trigger').keyup( function( e ) {
        if ( e.which === 32 ) { // Space key
            e.preventDefault();
            $(this).next().find('.list-expanding_child-list').slideToggle(100);
        }
    });
    // Hide the child lists initially
    $('.list-expanding_child-list').hide();

});

/* ==========================================================================
   Desktop Menu Transitions
   Do not apply a transition when hovering from one menu to the next
   ========================================================================== */

$(function() {

    var $desktopMenu = $('.primary-nav'),
        $desktopMenuTrigger = $('.primary-nav_top-level-list > li'),
        $desktopMenuChild = $('.desktop-menu_full-wrapper'),
        mouseIsInsideMenu = false,
        mouseIsInsideMenuItem = false,
        aMenuItemWasOpened = false,
        isSmall = $('.sliding-nav_trigger').is(':visible');

    // On window resize, set the isSmall variable again.
    $(window).resize(function() {
        isSmall = $('.sliding-nav_trigger').is(':visible');
    });

    // Add aria-expanded
    $desktopMenuChild.attr( 'aria-expanded', 'false' );

    $desktopMenu.mouseleave( function( e ) {

        // Update the mouse and menu state
        aMenuItemWasOpened = false;
        mouseIsInsideMenu = false;

        // Always use a transition when the mouse leaves the entire menu
        $desktopMenu.addClass('has-transition');

    });

    $desktopMenuTrigger.mouseenter( function( e ) {

        if (!isSmall) {
            // Update aria-expanded
            $(this).find('.desktop-menu_full-wrapper').attr( 'aria-expanded', 'true' );

            // Show the child list, previously hidden by default for the mobile menu.
            $('.list-expanding_child-list').show();

            if ( aMenuItemWasOpened === false ) {
                $desktopMenu.addClass('has-transition');
            } else {
                $desktopMenu.removeClass('has-transition');
            }

            // Update the mouse and menu state
            mouseIsInsideMenu = true;
            mouseIsInsideMenuItem = true;
            aMenuItemWasOpened = true;
        }

    });

    $desktopMenuTrigger.mouseleave( function( e ) {

        if (!isSmall) {
            // Update the menu item state
            mouseIsInsideMenuItem = false;

            // Use a delay to check if the mouse is inside of the menu but not in a
            // list item.
            window.setTimeout( function updateAMenuItemWasOpened() {
                if ( mouseIsInsideMenuItem === false && mouseIsInsideMenu ) {
                    aMenuItemWasOpened = false;
                }
            }, 100 );

            // Update aria-expanded
            $desktopMenuChild.attr( 'aria-expanded', 'false' );
        }

    });

});


/* ==========================================================================
   Nav-secondary
   ========================================================================== */

$(document).ready( function() {
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
   $input:                  $('.js-type-and-filter_input'),
   $items:                  $('.js-type-and-filter_item'),
   $button:                 $('.js-type-and-filter_button'),
   $clear:                  $('.js-type-and-filter_clear'),
   $messages:               $('.js-type-and-filter_message'),
   allMessage:              'Showing all {{ count }} contacts.',
   filteredMessageSingular: 'Showing 1 contact result.',
   filteredMessageMultiple: 'Showing {{ count }} contact results.'
});

// Hide the contact list header of there are zero results.
$('.type-and-filter').on( 'attemptSearch', function() {
    var resultsCount;
    if ( $('#contact-list').is(':hidden') ) {
        $('#contact-list').show();
        $('.type-and-filter').trigger('attemptSearch');
    } else {
        // Hide the show all contacts button if a search has been performed.
        $('#contact-list_btn').hide();
        // Show the message because on small screens it is hidden until needed.
        $('.js-type-and-filter_message').show();
        // Hide the contact list header of there are zero results.
        resultsCount = $('.js-type-and-filter_item').filter(':visible').length;
        $('#contact-list_header').toggle( (resultsCount > 0) );
    }
});

// Clicking on a helpful term should trigger a filter.
$('.js-helpful-term').on( 'click', function () {
    $('.js-type-and-filter_input').val( $( this ).text() ).trigger('valChange');
    $('.type-and-filter').trigger('attemptSearch');
});

// Provide a button to expand the contact list
// The contact list is hidden by default on small screens.
$('#contact-list_btn').on( 'click', function () {
    $( this ).hide();
    $('#contact-list').slideDown();
    $('.js-type-and-filter_message').slideDown();
});


/* ==========================================================================
   Initialize Chosen.js
   ========================================================================== */

$('.chosen-select').chosen({
    width:           '100%',
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
   History: Scroll up when collapsing History sectons
   ========================================================================== */

$('.history-section-expandable').find('.expandable_target')
    .not( $('.history-section-expandable').find('.expandable .expandable_target') )
    .on('click', function() {
    if ( $(this).attr('aria-pressed') === 'false' ) {
        $('html, body').animate({
            scrollTop: $(this).parent().offset().top - 15
        }, 500, 'easeOutExpo');
    }
});


/* ==========================================================================
   Init jquery.cf_inputSplit
   ========================================================================== */

$('.js-filter_range-date-wrapper').each(function( index ) {
    var $this = $( this );
    var $newThis = $this.next('.js-filter_range-date-replacement');
    var options = {
        newHTML:        $newThis,
        newInputsOrder: [
            '#' + $newThis.find('.js-filter_year').attr('id'),
            '#' + $newThis.find('.js-filter_month').attr('id')
        ],
        initialValues:  $this.find('.js-filter_range-date').val().split('-'),
        delimiter:      '-'
    };
    $this.cf_inputSplit( options );
    $( options.newInputsOrder ).trigger('updateState');
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
   #post-filters-form validation

   Checks the date range values.
   If the from (gte) date is larger than the to (lte) date, swap them.
   ========================================================================== */

$('.js-validate-filters').each(function() {
    var $this = $( this ),
        $gte = $this.find('.js-filter_range-date__gte'),
        $lte = $this.find('.js-filter_range-date__lte');

    // @param date1 {Date} The starting date in the range.
    // @param date2 {Date} The ending date in the range.
    // @return {Boolean} true if the ending date is after the starting date.
    function isValidDateRange(date1, date2) {
        return date2.getTime() > date1.getTime();
    }

    // Check that the date isn't empty,
    // and set it to the other set date if it is.
    // If it's still empty, return an empty string.
    // If year or month is missing, the current month or year are added.
    // @param targetDate {String} Date string to format.
    // @param compData {String} Other date in the date range we're checking.
    // @return {String} Formatted targetDate or an empty string.
    //   Throws an error if the expected YYYY-MM format is wrong.
    function formatDateString(targetDate, compDate) {
        var formattedDate = targetDate === '' ? compDate : targetDate;
        if (formattedDate === '') return formattedDate;

        if (/^\d{4}$/.test(formattedDate)) {
            var month = String(new Date().getMonth() + 1);
            if (month.length !== 2) month = '0' + month;
            formattedDate += '-' + month;
        } else if (/^\d{2}$/.test(formattedDate)) {
            var year = new Date().getFullYear();
            formattedDate = year + '-' + formattedDate;
        } else if (/^\d{4}-\d{2}$/.test(formattedDate) === false) {
            var msg = 'Unexpected date format! Should be in YYYY-MM format.';
            throw new Error(msg);
        }

        return formattedDate;
    }

    $( this ).on('submit', function( e ) {
        var gteVal = $gte.val();
        var lteVal = $lte.val();

        var gteParsedVal = formatDateString(gteVal, lteVal);
        var lteParsedVal = formatDateString(lteVal, gteVal);

        var validDateRange = isValidDateRange(
            new Date( gteParsedVal ),
            new Date( lteParsedVal )
        );
        if ( validDateRange ) {
            $gte.val( gteParsedVal );
            $lte.val( lteParsedVal );
        } else {
            // Swap the values if "from" value comes after "to" value.
            $gte.val( lteParsedVal );
            $lte.val( gteParsedVal );
        }
    });
});

/* ==========================================================================
   Form validation

   Check to make sure at least one form element has a value before submitting.
   ========================================================================== */

$('.js-validate_form-not-empty').each(function() {
    var $form = $(this);

    $form.on('submit', function() {
        var formIsEmpty = true;
        var event;

        $.each($form.serializeArray(), function(index, element) {
            if (element.value !== '') {
                formIsEmpty = false;
            }
        });

        if (formIsEmpty) {
            event = 'form:validate:empty';
        } else {
            event = 'form:validate:not_empty';
        }

        $form.trigger(event, $form);

        return !formIsEmpty;
    });

    return $form;
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
        if (pair[0] === key) {
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
    } else if (window.location.search.charAt(0) === '?') {
        query = window.location.search.substring(1);
    } else {
        query = window.location.search;
    }

    vars = query.split('&');

    var pair;
    for (var i = 0; i < vars.length; i++) {
        pair = vars[i].split('=');
        if (pair[0] === key) {
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
    }
    return window.location.search;
}

/* ==========================================================================
   Collapsing Beta banner
   ========================================================================== */

$('#beta-banner_btn').click( function() {
    if ( localStorage.getItem('betaBannerIsCollapsed') === 'true' ) {
        localStorage.setItem('betaBannerIsCollapsed', false);
    } else if (localStorage.getItem('betaBannerIsCollapsed') === 'false' ) {
        localStorage.setItem('betaBannerIsCollapsed', true);
    } else { // first load, item == null
        localStorage.setItem('betaBannerIsCollapsed', false);
    }
    return false;
});

$(document).ready(function() {
    if ( localStorage.getItem('betaBannerIsCollapsed') !== 'true' ) {
        // If this is the first load and the item has never been set, click to
        // expand the banner and set the item initially to 'false'.
        $('#beta-banner').get(0).expand();
    }
});

/* ==========================================================================
   Alert
   ========================================================================== */

(function($) {

    // Alert constructor.
    // @element {Element} Dom Element.
    // @options {Object} Object used to customize Alert.
    // Returns Alert instance.
    var Alert = function(element, options) {
        this.$element = $(element);
        this.options = $.extend(true, {}, this.defaults, options);
        this.init();
    };

    // Alert methods and shared properties
    Alert.prototype = {

        constructor: Alert,

        defaults: {
            validateSelector: '.js-validate_form-not-empty',
            easing:           'linear'
        },

        init: function() {
            var parentForm = this.$element.parents(this.defaults.validateSelector);

            if (parentForm.length === 1) {
                parentForm.on('form:validate:empty', $.proxy(this.show, this));
                parentForm.on('form:validate:not_empty', $.proxy(this.hide, this));
            }
            return this;
        },

        destroy: function() {
            this.$element.removeData();
            return this;
        },

        show: function() {
            this.$element.slideDown({
                easing: this.defaults.easing
            });
            return this;
        },

        hide: function() {
            this.$element.slideUp({
                easing: this.defaults.easing
            });
            return this;
        }
    };

    // Create the jQuery Alert plugin.
    // @options {Object} Object used to customize Alert.
    // Returns jQuery element.
    $.fn.createAlert = function(options) {
        return this.each(function() {
            var $this = $(this);
            $this.data('plugin', new Alert(this, options));
        });
    };

})(jQuery);

/* ==========================================================================
   Alert Initialization
   ========================================================================== */

$(document).ready(function() {
    $('.alert').createAlert();
});

/* ==========================================================================
   Footer Button: Scroll to Top
   ========================================================================== */

$(document).ready(function() {
    var duration = 300;

    $('.js-return-to-top').click(function(event) {
        event.preventDefault();
        $('html, body').animate({scrollTop: 0}, duration);
    });
});


