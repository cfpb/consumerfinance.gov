/* ==========================================================================
   Desktop Menu Transitions
   Do not apply a transition when hovering from one menu to the next
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var es = require( './util/expanded-state.js' );

function init() {
  var $primaryNav = $( '.js-primary-nav' );
  var $primaryTrigger = $( '.js-primary-nav_trigger' );
  var $primaryLink = $( '.js-primary-nav_link' );
  var $subNavs = $( '.js-sub-nav' );
  var $subBack = $( '.js-sub-nav_back' );

  /* TODO: Add Unit Tests */
  $primaryTrigger.on( 'click', function() {
    es.set.toggleExpandedState( $primaryNav );
    es.set.toggleExpandedState( $primaryTrigger );
    es.set.toggleExpandedState( $( 'body' ) );
  } );

  $primaryLink.on( 'click', function( event ) {
    event.preventDefault();

    var $this = $( this );
    var $thisSubNav = $this.siblings( '.js-sub-nav' );
    var $otherSubNavs = $subNavs.not( $thisSubNav );

    if ( es.get.isOneExpanded( $otherSubNavs ) ) {
      es.set.toggleExpandedState( $primaryLink, 'false' );
      es.set.toggleExpandedState(
        $otherSubNavs,
        'false',
        es.set.toggleExpandedState( $thisSubNav )
      );
    } else {
      es.set.toggleExpandedState( $thisSubNav );
    }

    es.set.toggleExpandedState( $this );
  } );

  $subBack.on( 'click', function() {
    var $thisSubNav = $( this ).closest( '.js-sub-nav' );

    es.set.toggleExpandedState( $primaryLink, 'false' );
    es.set.toggleExpandedState( $thisSubNav, 'false' );
  } );

/*
  TODO: wrap in a breakpoint handler along with other hover
  events to open the menu after #907 is merged

  $primaryNav.on( 'mouseleave', function() {
    es.set.toggleExpandedState( $subNavs, false );
  } );
*/
}

// Expose public methods.
module.exports = { init: init };
