/* eslint no-extra-semi: "off" */
'use strict';

var Analytics = require( '../../../../modules/Analytics' );
var Expandable = require( '../../../../organisms/Expandable' );

var expandableDom = document.querySelectorAll( '.content .o-expandable' );
var expandable;
if ( expandableDom ) {
  for ( var i = 0, len = expandableDom.length; i < len; i++ ) {
    expandable = new Expandable( expandableDom[i] );
    expandable.init();
  }
}

( function() {

  if ( !location.pathname.match( '/results' ) ) {
    return;
  }

  var toggleButtons = document.querySelectorAll(
    '.comparison-chart_toggle-button'
  );

  function switchComparisons( category ) {
    var allCategories = document.querySelectorAll( '.comparison_data-point' );
    var selectedButtonClass = 'comparison-chart_toggle-button__selected';

    // Hide all categories ...
    [].forEach.call( allCategories, function( el ) {
      el.style.display = 'none';
    } );
    // ... and deselect all toggle buttons ...
    [].forEach.call( toggleButtons, function( el ) {
      if ( el.classList ) {
        el.classList.remove( selectedButtonClass );
      } else {
        // Support browsers who don't have the classList API
        el.className = el.className.replace(
          new RegExp( '(^|\\b)' + selectedButtonClass
                                  .split( ' ' )
                                  .join( '|' ) + '(\\b|$)', 'gi' ),
          ' '
        );
      }
    } );
    // ... so that we can show only the right category data ...
    var showCategory = document.querySelectorAll( '[class^="comparison_data-point ' + category + '"]' );
    [].forEach.call( showCategory, function( el ) {
      el.style.display = 'inline-block';
    } );
    // ... and then highlight the correct button.
    var selectedButton = document.querySelector( '[data-compare-by="' + category + '"]' );
    if ( selectedButton.classList ) {
      selectedButton.classList.add(selectedButtonClass);
    } else {
      // Support browsers who don't have the classList API
      selectedButton.className += ' ' + selectedButtonClass;
    }
  }

  [].forEach.call( toggleButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;
      var category = input.dataset.compareBy;
      switchComparisons( category );

      var action = input.getAttribute( 'data-gtm-action' );
      var label = input.getAttribute( 'data-gtm-label' );
      var category = input.getAttribute( 'data-gtm-category' );

      if ( Analytics.tagManagerIsLoaded ) {
        sendEvent( action, label, category );
      } else {
        Analytics.addEventListener( 'gtmLoaded', sendEvent );
      }
    } );
  } );

} )();
