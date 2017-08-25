/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/results' ) ) {
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

  var radioButtons = document.querySelectorAll( '.histogram_toggle input' );
  var selectBoxes = document.querySelectorAll(
    '.histogram_select-demographic select'
  );

  function switchDemographicSelector( category ) {
    [].forEach.call( selectBoxes, function( el ) {
      el.style.display = 'none';
    } );

    var demographicSelector = document.querySelector( '#select-' + category );
    demographicSelector.style.display = 'inline-block';
  }

  function switchHistogram( select ) {
    if ( select.name ) {
      // var category = select.id.split( '-' )[1];
      var grouping = select.value;
      var nicename = select.options[select.selectedIndex].dataset.nicename;
      var image = document.querySelector( '#histogram_image' );
      var filename = '/static/img/histogram_' + grouping + '_1540x560.png';
      var groupingText = document.querySelector(
        '#histogram_title_grouping'
      );
      var groupingMeanBox = document.querySelector(
        '#score-box__avg'
      );
      var groupingMeanValue = document.querySelector(
        '#score-value__avg'
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
  }

  [].forEach.call( radioButtons, function( el ) {
    el.addEventListener( 'click', function( event ) {
      var input = event.target;

      if ( input.name && input.checked ) {
        var category = input.id.split( '_' )[1];
        var select = document.querySelector( '#select-' + category );
        switchDemographicSelector( category );
        switchHistogram( select );
      }
    } );
  } );

  [].forEach.call( selectBoxes, function( el ) {
    el.addEventListener( 'change', function( event ) {
      var select = event.target;
      switchHistogram( select );
    } );
  } );

  populateScores();

} )();
