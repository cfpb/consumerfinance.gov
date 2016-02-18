/**
 * jquery.type-and-filter.js
 *
 * Filters a list as you type using fuzzy or strict search for matching.
 * Fuzzy search depends on git://github.com/joshaven/string_score#0.1.20
 *
 * A public domain work of the Consumer Financial Protection Bureau
 */

'use strict';

var $ = require( 'jquery' );
var score = require( 'string_score' );
var standardType = require( '../util/standard-type' );

function init() {
  $.fn.typeAndFilter = function( userSettings ) {
    return $( this ).each( function() {
      var settings = $.extend( {
            minLength:               3,
            fuzzy:                   true,
            fuzziness:               0.5,
            threshold:               0.35,
            keyup:                   false,
            $form:                   $(),
            $button:                 $(),
            $clear:                  $(),
            $input:                  $(),
            $items:                  $(),
            allMessage:              'Showing all {{ count }}.',
            filteredMessageSingular:
              'There is 1 result for "{{ term }}".',
            filteredMessageMultiple:
              'There are {{ count }} results for "{{ term }}"',
            minTermMessage:
              'The search term "{{ term }}" is not long enough. ' +
              '<span class="short-desc">' +
              'Please use a minimum of 3 characters.</span>',
            clickCallback: standardType.noopFunct
          }, userSettings ),
          $this = $( this ),
          $form = settings.$form,
          $button = settings.$button,
          $input = settings.$input,
          $items = settings.$items,
          $clear = settings.$clear,
          searchTerm,
          resultsCount;
      // Only proceed if we have both the search input and enough items
      // to filter.
      if ( $input.length === 0 && $items.length < 2 ) {
        return;
      }

      //
      // Set event handlers
      //

      // Check to see if we should perform the filter on button click.
      if ( $button.length > 0 ) {
        $button.on( 'click', function() {
          $this.trigger( 'attemptSearch' );
        } );
      }
      // Check to see if we should perform the filter as you type.
      //
      // TODO: Set a timeout before triggering search so that we're not
      // triggering back to back searches.
      if ( settings.keyup ) {
        $input.on( 'keyup paste', function() {
          $this.trigger( 'attemptSearch' );
        } );
      }
      // Show the clear button only when there is text in the input.
      $input.on( 'keyup paste', function() {
        $input.trigger( 'valChange' );
      } );
      // Reset everything when the clear button is pressed
      $clear.on( 'click', function() {
        $this.trigger( 'clear' );
      } );
      // Set plugin-specific events
      $this
        // Logic to decide if a search will be performed.
        // Searches require a minimum search term length of 3 characters.
        .on( 'attemptSearch', function() {
          searchTerm = $.fn.typeAndFilter.scrubText( $input.val() );
          if ( searchTerm.length >= 3 ) {
            $this.trigger( 'search' );
          } else {
            $form.trigger( 'cf_notifier:notify', {
              message:
                settings.minTermMessage
                  .replace( /{{[\s]*term[\s]*}}/, $input.val() ),
              state:          'error',
              insertLocation: 'appendTo'
            } );
            $input.addClass( 'error' );
          }
        } )
        // Perform the search.
        .on( 'search', function() {
          $.fn.typeAndFilter.filterItems( $items, searchTerm, true, settings );
          resultsCount = $items.filter( ':visible' ).length;
          var message = settings.filteredMessageMultiple;
          var state = 'success';
          if ( resultsCount === 1 ) {
            message = settings.filteredMessageSingular;
          }
          if ( resultsCount === 0 ) {
            state = 'warning';
          }

          message = message.replace( /{{[\s]*term[\s]*}}/, searchTerm );
          message = message.replace( /{{[\s]*count[\s]*}}/, resultsCount );

          $form.trigger( 'cf_notifier:notify', {
            message:        message,
            state:          state,
            insertLocation: 'appendTo'
          } );
        } )
        // Reset/clear the plugin.
        .on( 'clear', function() {
          searchTerm = '';
          $input
            .val( '' )
            .trigger( 'valChange' )
            .focus();
          $items.show();
          resultsCount = $items.filter( ':visible' ).length;
          var message =
            settings.allMessage.replace( /{{[\s]*count[\s]*}}/, resultsCount );
          $form.trigger( 'cf_notifier:clear' );
        } )
        // Remove the validation class during these two events.
        .on( 'search clear', function() {
          $input.removeClass( 'error' );
        } );
      $input
        // Show clear button if the input contains text; hide if empty.
        .on( 'valChange', function() {
          if ( $input.val().length > 0 ) {
            $clear.show();
          } else {
            $clear.hide();
          }
        } );

      //
      // Initial dom manipulation setup.
      //
      resultsCount = $items.length;
      // Hide the clear button unless there is text in the input.
      $input.trigger( 'valChange' );
    } );
  };

  $.fn.typeAndFilter.scrubText = function( text, minLength ) {
    var cleanText = text;
    // Set a default for minLength if non was set.
    if ( typeof minLength === 'undefined' ) {
      minLength = 3;
    }
    cleanText = cleanText.toLowerCase();
    cleanText = $.fn.typeAndFilter.removeExtraSpaces( cleanText );
    cleanText = $.fn.typeAndFilter.removeWordsOfLength( cleanText, minLength );
    cleanText = $.fn.typeAndFilter.removePlurality( cleanText );
    return cleanText;
  };

  $.fn.typeAndFilter.removeExtraSpaces = function( text ) {
    return text.replace( /\s+/g, ' ' ).trim();
  };

  $.fn.typeAndFilter.removeWordsOfLength = function( text, minLength ) {
    // Convert the text into an array that we can filter.
    var words = text.split( ' ' );
    // Filters out words from the array that don't meet the minimum
    // length; then converts the array back into a string.
    return $.grep( words, function( word ) {
      return word.length >= minLength;
    } ).join( ' ' );
  };

  $.fn.typeAndFilter.removePlurality = function( text ) {
    return text.replace( /([i][e][s])$|([^aiou])s$/, '$1$2' );
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
        words = text.split( ' ' );
    // Loop through each word
    $.each( words, function( index, value ) {
      var matchScore = value.score( searchTerm, settings.fuzziness );
      if ( matchScore >= settings.threshold ) {
        match = true;
        // Return false to break out of the $.each loop.
        return false;
      }
      return true;
    } );
    return match;
  };

  $.fn.typeAndFilter.filterItems =
    function( $items, searchTerm, fuzzy, options ) {
      // TODO: If query is a multi-word phrase, search for exact phrase first
      // if ( searchTerm.split(' ').length > 1 ) {
      //     var match = $.fn.typeAndFilter.strictSearch( searchTerm, value );
      //     ...
      // }

      // Loop through each item, if it contains matching text then show it,
      // if it doesn't then hide it.
      var terms = searchTerm.split( ' ' ),
          itemsLength = $items.length,
          termsLength = terms.length;
      for ( var i = 0; i < itemsLength; i++ ) {
        for ( var j = 0; j < termsLength; j++ ) {
          var match,
              $this = $items.eq( i ),
              itemText = $.fn.typeAndFilter.scrubText( $this.text() );
          // Choose which search to use.
          if ( fuzzy ) {
            match = $.fn.typeAndFilter.fuzzySearch( itemText, terms[j], options );
          } else {
            match = $.fn.typeAndFilter.strictSearch( itemText, terms[j] );
          }
          // The match variable is used to set the visiblity, true for
          // visible and false for hidden.
          $this.toggle( match );

          // If we find a match then break out of the loop so we don't
          // unmatch this during subsequent comparisons.
          if ( match ) {
            break;
          }
        }
      }
    };
}

module.exports = { init: init };
