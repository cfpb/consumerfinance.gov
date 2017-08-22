/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/results' ) ) {
    return;
  }

  var score = Number( location.search.slice( 1 ) );
  var min = 14;
  var max = 95;
  var average = 39;
  var high = 64;

  var resourcesByScore = [
    {
      graph: 'improvement.png',
      wellBeing: 'Could be improved'
    },
    {
      graph: 'average.png',
      wellBeing: 'Average'
    },
    {
      graph: 'high.png',
      wellBeing: 'High'
    }
  ];

  var imgPath = window.location.pathname.replace( 'results.html', '' ) +
    'static/img/';

  function getResourcesByScore() {
    if ( score < average ) return resourcesByScore[0];
    if ( score < high ) return resourcesByScore[1];
    return resourcesByScore[2];
  }

  function loadResources( resources ) {
    var scoreBox = document.querySelector( '#score-box' );
    var scoreValue = document.querySelector( '#score-value' );
    var scorePercentage = ( score - min ) / ( max - min ) * 100;
    var compareLink = document.querySelector( '#compare-link' );
    // var blurb = document.querySelector( '#well-being-blurb' );
    // var graph = document.querySelector( '#score-graph' );

    if ( scorePercentage > 50 ) {
      scorePercentage = 100 - scorePercentage;
      scoreBox.style.right = scorePercentage.toString() + '%';
      scoreBox.className = 'score-box__right';
    } else {
      scoreBox.style.left = scorePercentage.toString() + '%';
    }
    scoreValue.textContent = score;
    compareLink.setAttribute( 'href', '../compare/?' + score );
    // blurb.textContent = blurb.textContent + ' ' + resources.wellBeing;
    // graph.setAttribute( 'src', imgPath + resources.graph );
  }

  // $( document ).ready( function() {
  //   var score = Number( location.search.slice( 1 ) );
  //   loadResources( score, getResourcesByScore( score ) );
  // } );

  loadResources( getResourcesByScore() );

} )();
