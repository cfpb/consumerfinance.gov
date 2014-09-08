/**
 * jquery.type-and-filter.js
 *
 * Filters a list as you type using fuzzy or strict search for matching.
 * Fuzzy search depends on git://github.com/joshaven/string_score#0.1.20
 *
 * A public domain work of the Consumer Financial Protection Bureau
 */

(function ($) {

    $.fn.typeAndFilter = function( userSettings ) {

        return $( this ).each(function() {
            var settings = $.extend( {
                    minLength: 3,
                    fuzzy: true,
                    fuzziness: 0.5,
                    threshold: 0.35,
                    $button: $(),
                    $clear: $(),
                    $input: $(),
                    $items: $(),
                    $messages: $(),
                    allMessage: 'Showing all {{ count }}',
                    filteredMessage: 'Showing {{ count }} filtered results for {{ term }}',
                    minTermMessage: '<em>The search term "{{ term }}" is not long enough.<br>Please use a minimum of 3 characters.</em>',
                    'clickCallback': function(e){}
                }, userSettings ),
                $this = $( this ),
                $button = settings.$button,
                $messages = settings.$messages,
                $input = settings.$input,
                $items = settings.$items,
                $clear = settings.$clear,
                searchTerm,
                resultsCount;
            // Set aria attributes
            $messages.attr( 'aria-live', 'polite' ).attr( 'role', 'region' );
            // Only proceed if we have both the search input and enough items
            // to filter.
            if ( $input.length === 0 && $items.length < 2 ) {
                return;
            }
            // Check to see if we should perform the filter on button click or as you type.
            if ( $button.length > 0 ) {
                $button.on( 'click', function () {
                    $this.trigger('attemptSearch');
                });
            } else {
                $input.on( 'keyup', function() {
                    $this.trigger('attemptSearch');
                });
            }
            // Reset everything when the clear button is pressed
            $clear.on( 'click', function () {
                $this.trigger('clear');
            });
            // Search on keyup if the user typed 3 or more characters.
            // If the input is less than 3 then show all items.
            $this.on( 'attemptSearch', function() {
                searchTerm = $.fn.typeAndFilter.scrubText( $input.val() );
                if ( searchTerm.length >= 3 ) {
                    $this.trigger('search');
                } else {
                    $this.trigger('minTermError');
                }
            });
            // 
            $this.on( 'search', function () {
                $.fn.typeAndFilter.filterItems( $items, searchTerm, true, settings );
                resultsCount = $items.filter(':visible').length;
                $.fn.typeAndFilter.showFilteredMessage( $messages, settings.filteredMessage, resultsCount, searchTerm );
            });
            // 
            $this.on( 'clear', function () {
                searchTerm = '';
                $input.val('');
                $items.show();
                resultsCount = $items.filter(':visible').length;
                $.fn.typeAndFilter.showDefaultMessage( $messages, settings.allMessage, resultsCount );
            });
            // 
            $this.on( 'minTermError', function () {
                $.fn.typeAndFilter.showMinTermMessage( $messages, settings.minTermMessage, $input.val() );
            });
        });
    };

    $.fn.typeAndFilter.scrubText = function( text, minLength ) {
        var cleanText = text;
        // Set a default for minLength if non was set.
        if ( typeof minLength !== 'undefined' ) {
            minLength = minLength;
        } else {
            minLength = 3;
        }
        cleanText = cleanText.toLowerCase();
        cleanText = $.fn.typeAndFilter.removeExtraSpaces( cleanText );
        cleanText = $.fn.typeAndFilter.removeWordsOfLength( cleanText, minLength );
        // console.log( '\nOriginal text:', text, '\nClean text:', cleanText );
        return cleanText;
    };

    $.fn.typeAndFilter.removeExtraSpaces = function( text ) {
        return text.replace( /\s+/g, ' ' ).trim();
    };

    $.fn.typeAndFilter.removeWordsOfLength = function( text, minLength ) {
        // Convert the text into an array that we can filter.
        var words = text.split(' ');
        // Filters out words fromt he array that don't meet the minimum
        // length; then converts the array back into a string.
        return $.grep( words, function( word ) {
            return word.length >= minLength;
        }).join(' ');
    };

    $.fn.typeAndFilter.strictSearch = function( text, searchTerm ) {
        return text.indexOf( searchTerm ) > -1;
    };

    $.fn.typeAndFilter.fuzzySearch = function( text, searchTerm, options ) {
        var match = false,
            settings = $.extend( {
                fuzziness: 0.5,
                threshold: 0.35
            }, options ),
            words = text.split(' ');
        // Loop through each word
        $.each( words, function( index, value ) {
            var matchScore = value.score( searchTerm, settings.fuzziness );
            // console.log( 'searchTerm:', searchTerm, ' | word:', value, ' | score:', matchScore );
            if ( matchScore >= settings.threshold ) {
                match = true;
                // Return false to break out of the $.each loop.
                return false;
            }
        });
        return match;
    };

    $.fn.typeAndFilter.filterItems = function( $items, searchTerm, fuzzy, options ) {
        // Loop through each item, if it contains matching text then show it,
        // if it doesn't then hide it.
        $.each( $items, function() {
            var $this = $( this ),
                itemText = $.fn.typeAndFilter.scrubText( $this.text() ),
                match;
            // Choose which search to use.
            if ( fuzzy ) {
                match = $.fn.typeAndFilter.fuzzySearch( itemText, searchTerm, options );
            } else {
                match = $.fn.typeAndFilter.strictSearch( itemText, searchTerm );
            }
            // The match variable is used to set the visiblity, true for
            // visible and false for hidden.
            $this.toggle( match );
        });
    };

    $.fn.typeAndFilter.showMinTermMessage = function( $messagesContainer, template, searchTerm ) {
        var html = template.replace(/{{[\s]*term[\s]*}}/, searchTerm);
        $messagesContainer.html( html );
    };

    $.fn.typeAndFilter.showFilteredMessage = function( $messagesContainer, template, resultsCount, searchTerm ) {
        var html = template.replace(/{{[\s]*term[\s]*}}/, searchTerm);
            html = html.replace(/{{[\s]*count[\s]*}}/, resultsCount);
        $messagesContainer.html( html );
    };

    $.fn.typeAndFilter.showDefaultMessage = function( $messagesContainer, template, resultsCount ) {
        var html = template.replace(/{{[\s]*count[\s]*}}/, resultsCount);
        $messagesContainer.html( html );
    };

}( jQuery ));
