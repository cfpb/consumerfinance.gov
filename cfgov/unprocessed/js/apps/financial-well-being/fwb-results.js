/* eslint no-extra-semi: "off" */
'use strict';

var Analytics = require( '../../modules/Analytics' );
var Expandable = require( '../../organisms/Expandable' );

var expandableDom = document.querySelectorAll( '.content .o-expandable' );
var expandable;
if ( expandableDom ) {
  for ( var i = 0, len = expandableDom.length; i < len; i++ ) {
    expandable = new Expandable( expandableDom[i] );
    expandable.init();
  }
}

function init() {

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
        el.classList.remove( selectedButtonClass );
    } );
    // ... so that we can show only the right category data ...
    var showCategory = document.querySelectorAll( '[class^="comparison_data-point ' + category + '"]' );

    [].forEach.call( showCategory, function( el ) {
      el.style.display = 'inline-block';
    } );
    // ... and then highlight the correct button.
    var selectedButton = document.querySelector( '[data-compare-by="' + category + '"]' );

    selectedButton.classList.add( selectedButtonClass );
  }

  function sendEvent( action, label, category ) {
    var eventData = Analytics.getDataLayerOptions( action, label, category );
    Analytics.sendEvent( eventData );
  }

  [].forEach.call( toggleButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;
      var category = input.getAttribute( 'data-compare-by' );
      switchComparisons( category );

      var action = input.getAttribute( 'data-gtm-action' );
      var label = input.getAttribute( 'data-gtm-label' );
      category = input.getAttribute( 'data-gtm-category' );

      if ( Analytics.tagManagerIsLoaded ) {
        sendEvent( action, label, category );
      } else {
        Analytics.addEventListener( 'gtmLoaded', sendEvent );
      }
    } );
  } );

}

module.exports = { init: init };
