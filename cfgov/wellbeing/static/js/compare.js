/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/compare' ) ) {
    return;
  }

  var score = Number( location.search.slice( 1 ) );
  var min = 14;
  var max = 95;

  function loadResources() {
    var scoreBox = document.querySelector( '#score-box' );
    var scoreValues = document.querySelectorAll( '.score-value' );
    var scorePercentage = ( score - min ) / ( max - min ) * 100 + 1.875;
    var resultsLink = document.querySelector( '#results-link' );

    if ( scorePercentage > 50 ) {
      scorePercentage = 100 - scorePercentage;
      scoreBox.style.right = scorePercentage.toString() + '%';
      scoreBox.className = 'score-box__right';
    } else {
      scoreBox.style.left = scorePercentage.toString() + '%';
    }

    [].forEach.call( scoreValues, function( el ) {
      el.textContent = score;
    } );
    resultsLink.setAttribute( 'href', '../results/?' + score );
  }

  var radioButtons = document.querySelectorAll( '.histogram_toggle input' );
  [].forEach.call( radioButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        var bits = input.id.split( '_' );
        var category = bits[0];
        var grouping = bits[1];
        var image = document.querySelector( '#histogram_image__' + category );
        var filename = '/static/img/histogram_' + grouping + '_1740x430.png';
        image.setAttribute( 'src', filename );
      }
    } );
  } );

  loadResources();

} )();
