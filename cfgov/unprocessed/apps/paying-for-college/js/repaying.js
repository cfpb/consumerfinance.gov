/* eslint-disable */
// TODO: Remove jquery.
import $ from 'jquery';

const decisionStackerTargets = {
  '0':  { 'question': '1', 'federal': 'a', 'non-federal': 'b', 'both': 'c' },
  '1a': { question: '2', yes: 'a', no: 'b' },
  '1b': { question: '2', yes: 'c', no: 'd' },
  '2a': { 'question': '3', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '2b': { 'question': '8', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '2c': { 'question': '3', 'yes': 'c', 'no': 'd', 'not-sure': 'd' },
  '2d': { 'question': '8', 'yes': 'c', 'no': 'd', 'not-sure': 'd' },
  '3a': { question: '4', yes: 'a', no: 'b' },
  '3b': { 'question': '8', 'yes': 'a', 'no': 'b', 'not-sure': 'b' },
  '3c': { module: 'm12' },
  '3d': { 'question': '8', 'yes': 'c', 'no': 'e', 'not-sure': 'e' },
  '4a': { question: '5', yes: 'a', no: 'b' },
  '4b': { module: 'm5' },
  '5a': { module: 'm4' },
  '5b': { question: '6', yes: 'a', no: 'b' },
  '6a': { module: 'm5', yes: 'a', no: 'b' },
  '6b': { question: '7', yes: 'a', no: 'b' },
  '7a': { module: 'm6' },
  '7b': { module: 'm7' },
  '8a': { question: '9', yes: 'a', no: 'b' },
  '8b': { question: '9', yes: 'a', no: 'c' },
  '8c': { question: '9', yes: 'e', no: 'd' },
  '8d': { question: '9', yes: 'e', no: 'g' },
  '8e': { question: '9', yes: 'f', no: 'g' },
  '9a': { module: 'm2' },
  '9b': { module: 'm1' },
  '9c': { module: 'm3' },
  '9d': { module: 'm9' },
  '9e': { module: 'm10' },
  '9f': { module: 'm13' },
  '9g': { module: 'm11' }
}; // end decisionStackerTargets


/* Decision tree where each previous choices are visible */
const pfcDecision = ( function() {
  let slideSpeed = 300,
      scrollSpeed = 500,
      writingHash = true;

  function assignButtons( code ) {
    // this function relies on decisionStackerTargets object
    if ( typeof decisionStackerTargets !== 'object' ) {
      return false;
    }
    const $elem = $( '#q' + decisionStackerTargets[code].question );
    const sectionOrigin = $elem.attr( 'data-ds-origin' );
    const sectionData = decisionStackerTargets[sectionOrigin];
    $elem.find( 'button' ).each( function() {
      const name = $( this ).attr( 'data-ds-name' );
      if ( sectionData.hasOwnProperty( name ) ) {
        $( this ).val( sectionData.question + sectionData[name] );
      }
    } );
  }

  function processHash( position ) {
    const hashes = location.hash.replace( '#', '' ).split( ':' );
    $( '.ds-buttons:visible button[data-ds-name="' + hashes[position] + '"]' ).click();
    if ( position + 1 < hashes.length ) {
      processHash( position + 1 );
    }
  }

  function scrollToDestination( destination ) {
    let scrollTop = $( destination ).offset().top,
        destinationBottom = $( destination ).offset().top + $( destination ).height();
    if ( destination.substring( 0, 2 ) == '#q' ) {
      scrollTop = $( '.ds-scroll-top' ).offset().top;
      if ( scrollTop + $( window ).height() < destinationBottom ) {
        scrollTop = destinationBottom - $( window ).height();
      }
    }
    $( 'html, body' ).animate( {
      scrollTop: scrollTop
    }, scrollSpeed );
  }

  $.fn.decisionStacker = function() {
    assignButtons( '0' );
    // Set buttons up to lead to the next section, show appropriate text.
    $( '.ds-section .ds-buttons button' ).click( function() {
      const code = $( this ).val();
      let destination = decisionStackerTargets[code].question;

      if ( writingHash === true ) {
        if ( location.hash !== '' ) {
          location.hash += ':';
        }
        location.hash += $( this ).attr( 'data-ds-name' );
      }

      // destination is a question
      if ( destination !== undefined ) {
        destination = '#q' + destination;
      }
      // destination is a module
      else {
        destination = '#' + decisionStackerTargets[code].module;
        $( '.ds-clear-all.ds-clear-after-m' ).show();
      }
      $( destination ).slideDown( slideSpeed, function() {
        scrollToDestination( destination );
      } );
      $( destination ).attr( 'data-ds-origin', code );
      $( this ).closest( '.ds-section' ).attr( 'data-ds-decision', $( this ).attr( 'data-ds-name' ) );
      assignButtons( code );
      const $section = $( this ).closest( '.ds-section' );
      $section.find( '[data-responds-to="' + $( this ).attr( 'data-ds-name' ) + '"]' ).show();
      $section.find( '.ds-content' ).slideUp( slideSpeed );
      $( '.ds-clear-all.ds-clear-after-q' ).show();

    } );
    $( '.ds-response-container .go-back' ).click( function() {
      let $section = $( this ).closest( '.ds-section' ),
          questionNumber = Number( $section.attr( 'data-ds-qnum' ) ),
          hash = '';
      $( '.ds-question:visible' ).each( function( i, val ) {
        if ( Number( $( this ).attr( 'data-ds-qnum' ) ) > questionNumber ) {
          $( this ).find( '.ds-content' ).show();
          $( this ).find( '.ds-response-container div' ).hide();
          $( this ).hide();
        } else if ( Number( $( this ).attr( 'data-ds-qnum' ) ) < questionNumber ) {
          // rebuild hash
          if ( i !== 0 ) {
            hash += ':';
          }
          hash += $( this ).attr( 'data-ds-decision' );
        }
      } );
      $section.find( '.ds-response-container div' ).hide();
      $( '.ds-module' ).hide();
      $section.find( '.ds-content' ).slideDown( slideSpeed, function() {
        scrollToDestination( '#q' + questionNumber );
      } );
      // hide clear all when user is on Question #1
      if ( questionNumber === 1 ) {
        $( '.ds-clear-all' ).hide();
      }
      // reset hash
      location.hash = hash;
    } );

    $( '.ds-clear-button' ).click( function() {
      $( '#q1 .go-back' ).click();
    } );
  };

  $( document ).ready( function() {
    if ( location.hash !== '' ) {
      scrollSpeed = 0;
      slideSpeed = 0;
      writingHash = false;
      processHash( 0 );
      scrollSpeed = 500;
      slideSpeed = 300;
      writingHash = true;
    }
  } );

} )( $ );

const pfcRepay = ( function() {

  $( '.ds-section' ).decisionStacker();

  $( '.read-more .read-more_target' ).click( function() {
    const $parent = $( this ).closest( '.read-more' );
    if ( $parent.hasClass( 'read-more_is-closed' ) ) {
      $parent.find( '.read-more_content' ).slideDown();
      $parent.find( '.read-more_open' ).hide();
      $parent.find( '.read-more_close' ).show();
      $parent.removeClass( 'read-more_is-closed' ).addClass( 'read-more_is-open' );
    } else {
      $parent.find( '.read-more_content' ).slideUp();
      $parent.find( '.read-more_open' ).show();
      $parent.find( '.read-more_close' ).hide();
      $parent.removeClass( 'read-more_is-open' ).addClass( 'read-more_is-closed' );
    }
  } );

} )( $ );
