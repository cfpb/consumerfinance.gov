/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/compare' ) ) {
    return;
  }

  var score = Number( location.search.slice( 1 ) );
  var min = 14;
  var max = 95;

  var means = {
    'all-adults': 54,
    '18-30': 51,
    '31-45': 52,
    '46-61': 54,
    '62+': 60,
    'men': 54,
    'women': 54,
    'income-level-1': 48,
    'income-level-2': 52,
    'income-level-3': 56,
    'income-level-4': 59,
    'income-level-5': 63
  };

  function populateScores() {
    var scoreBoxes = document.querySelectorAll( '.score-box__user' );
    var scoreBoxLR = 'left';
    var scoreValues = document.querySelectorAll( '.score-value' );
    // +1.875 is a manual adjustment to compensate for space between bars
    var scorePercentage = ( score - min ) / ( max - min ) * 100 + 1.875;
    var resultsLink = document.querySelector( '#results-link' );

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
      el.setAttribute(
        'style', scoreBoxLR + ': ' + scorePercentage.toString() + '%'
      );
    } );

    [].forEach.call( scoreValues, function( el ) {
      el.textContent = score;
    } );

    resultsLink.setAttribute( 'href', '../results-alt/?' + score );
  }

  var radioButtons = document.querySelectorAll( '.histogram_toggle input' );
  [].forEach.call( radioButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        var bits = input.id.split( '_' );
        var category = bits[0];
        var grouping = bits[1];
        var nicename = input.getAttribute( 'data-nicename' );
        var image = document.querySelector( '#histogram_image__' + category );
        var filename = '/static/img/histogram_' + grouping + '_1540x560.png';
        var groupingText = document.querySelector(
          '#histogram_title_grouping__' + category
        );
        var groupingMeanBox = document.querySelector(
          '#score-box__avg__' + category
        );
        var groupingMeanValue = document.querySelector(
          '#score-value__avg__' + category
        );
        // +1.875 is a manual adjustment to compensate for space between bars
        var groupingMeanPercentage = 100 - ( ( means[grouping] - min ) /
                                     ( max - min ) * 100 + 1.875 );
        image.setAttribute( 'src', filename );
        groupingText.textContent = nicename;
        groupingMeanValue.textContent = means[grouping];
        // average score boxes will always be right-aligned
        groupingMeanBox.style.right = groupingMeanPercentage.toString() + '%';
      }
    } );
  } );

  populateScores();

} )();
