/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/results' ) ) {
    return;
  }

  var score = Number( location.search.slice( 1 ) );
  var min = 14;
  var max = 95;

  function populateScores() {
    var scoreBoxes = document.querySelectorAll( '.score-box' );
    var scoreBoxLR = 'left';
    var scoreValues = document.querySelectorAll( '.score-value' );
    var scorePercentage = ( score - min ) / ( max - min ) * 100 + 1.875;

    if ( scorePercentage > 50 ) {
      scorePercentage = 100 - scorePercentage;
      scoreBoxLR = 'right';
    }

    [].forEach.call( scoreBoxes, function( el ) {
      if ( el.classList ) {
        el.classList.add( 'score-box__' + scoreBoxLR );
      } else {
        el.className += ' score-box__' + scoreBoxLR;
      }
      el.setAttribute( 'style',
                       scoreBoxLR + ': ' + scorePercentage.toString() + '%' );
    } );

    [].forEach.call( scoreValues, function( el ) {
      el.textContent = score;
    } );
  }

  populateScores();

} )();
