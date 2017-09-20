/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/results' ) ) {
    return;
  }

  var radioButtons = document.querySelectorAll(
    '.comparison-chart_toggle input'
  );

  function switchComparisons( category ) {
    var allCategories = document.querySelectorAll( '.comparison_data-point' );
    [].forEach.call( allCategories, function( el ) {
      el.style.display = 'none';
    } );

    var showCategory = document.querySelectorAll(
      '[class^="comparison_data-point ' + category + '"]'
    );
    [].forEach.call( showCategory, function( el ) {
      el.style.display = 'inline-block';
    } );
  }

  [].forEach.call( radioButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        var category = input.id.split( '_' )[1];
        switchComparisons( category );
      }
    } );
  } );

} )();
