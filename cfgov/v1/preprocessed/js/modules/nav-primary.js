/* ==========================================================================
   Desktop Menu Transitions
   Do not apply a transition when hovering from one menu to the next
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var es = require( './util/expanded-state.js' );

/**
 * Set up DOM references and event handlers.
 */
function init() {
  var $primaryNav = $( '.js-primary-nav' );
  var $primaryTrigger = $( '.js-primary-nav_trigger' );
  var $primaryLink = $( '.js-primary-nav_link' );
  var $subNavs = $( '.js-sub-nav' );
  var $subBack = $( '.js-sub-nav_back' );

  $primaryTrigger.on( 'click', function() {
    if ( es.get.isThisExpanded( $primaryNav ) ) {
      es.set.toggleExpandedState( $primaryNav, 'false', function() {
        $primaryTrigger.focus();
      } );
    } else {
      es.set.toggleExpandedState( $primaryNav, 'true', function() {
        $primaryLink.first().focus();
      } );
    }

    es.set.toggleExpandedState( $primaryTrigger );
    es.set.toggleExpandedState( $( 'body' ) );
  } );

  $primaryLink.on( 'click', function( event ) {
    event.preventDefault();

    var $this = $( this );
    var $thisSubNav = $this.siblings( '.js-sub-nav' );
    var $otherSubNavs = $subNavs.not( $thisSubNav );
    var firstLink = $thisSubNav.find( 'a' ).first();

    if ( es.get.isOneExpanded( $otherSubNavs ) ) {
      es.set.toggleExpandedState( $primaryLink, 'false' );
      es.set.toggleExpandedState(
        $otherSubNavs,
        'false',
        function() {
          es.set.toggleExpandedState( $thisSubNav );
          firstLink.focus();
        }
      );
    } else if ( es.get.isThisExpanded( $thisSubNav ) ) {
      es.set.toggleExpandedState( $thisSubNav, 'false', function() {
        $this.focus();
      } );
    } else {
      es.set.toggleExpandedState( $thisSubNav, null, function() {
        firstLink.focus();
      } );
    }

    es.set.toggleExpandedState( $this );
  } );

  $subBack.on( 'click', function() {
    var $thisSubNav = $( this ).closest( '.js-sub-nav' );
    var $thisPrimaryLink = $( this )
                           .closest( '.js-primary-nav_item' )
                           .find( '.js-primary-nav_link' );
    es.set.toggleExpandedState( $primaryLink, 'false' );
    es.set.toggleExpandedState( $thisSubNav, 'false', function() {
      $thisPrimaryLink.focus();
    } );
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
