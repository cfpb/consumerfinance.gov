/* global $ */
/* eslint no-extra-semi: "off" */
'use strict';

( function() {

  if ( !location.pathname.match( '/results' ) ) {
    return;
  }

  var score = Number( location.search.slice( 1 ) );
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
    var scoreDisplay = document.querySelector( '#score-value' );
    var blurb = document.querySelector( '#well-being-blurb' );
    var graph = document.querySelector( '#score-graph' );

    scoreDisplay.textContent = scoreDisplay.textContent + ' ' + score;
    blurb.textContent = blurb.textContent + ' ' + resources.wellBeing;
    graph.setAttribute( 'src', imgPath + resources.graph );
  }

  // $( document ).ready( function() {
  //   var score = Number( location.search.slice( 1 ) );
  //   loadResources( score, getResourcesByScore( score ) );
  // } );

  loadResources( getResourcesByScore() );

} )();
