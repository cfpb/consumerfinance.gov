/* ==========================================================================
   Sliding/Pushing Menu
   ========================================================================== */

'use strict';

require( './jquery/cfpb-aria-button' ).init();
var $ = require( 'jquery' );

function init() {
  var $body = $( 'body' ),
      $slidingNav = $( '.sliding-nav' ),
      $slidingNavTrigger = $( '.sliding-nav_trigger' ),
      $slidingNavNav = $( '.sliding-nav_nav' ),
      $slidingNavPage = $( '.sliding-nav_page' ),
      $slidingNavPageOverlay = $( '.sliding-nav_page-overlay' );

  $slidingNavTrigger.click( function( e ) {
    e.preventDefault();

    // First deal with the filters button if it exists.
    if ( $( '.l-sidenav' ).hasClass( 'is-open' ) ) {
      $( '.l-sidenav-btn' ).trigger( 'click' );
    }

    if ( $slidingNav.hasClass( 'is-open' ) ) {
      window.setTimeout( function() {
        $slidingNavPage.removeClass( 'is-scroll-disabled' );
      }, 200 );
      $slidingNav.removeClass( 'is-open' );
      $slidingNavPageOverlay.off( 'click' );
    } else {
      $slidingNav.addClass( 'is-open' );
      $( window ).scroll( slidingNavStopScroll );
      $slidingNavPageOverlay.click( function( evt ) {
        evt.preventDefault();
        $( $slidingNavTrigger[0] ).trigger( 'click' );
      } );
    }
    $body.scrollTop( 0 );
  } );

  function slidingNavStopScroll() {
    if ( parseInt( $slidingNavPage.css( 'margin-right' ), 10 ) < 0 ) {
      $slidingNavPage.addClass( 'is-scroll-disabled' );
      $slidingNavNav.css( 'min-height', $( window ).height() );
      $( window ).off( 'scroll', slidingNavStopScroll );
    }
  }

  // Expanding list
  // TODO: Determine if we should actually use the cfpbAriaButton plugin.
  $( '.list-expanding_trigger' ).cfpbAriaButton();
  $( '.list-expanding_trigger' ).click( function( e ) {
    e.preventDefault();
    $( this ).next().find( '.list-expanding_child-list' ).slideToggle( 100 );
  } );
  $( '.list-expanding_trigger' ).keyup( function( e ) {
    // Space key pressed.
    if ( e.which === 32 ) {
      e.preventDefault();
      $( this ).next().find( '.list-expanding_child-list' ).slideToggle( 100 );
    }
  } );
  // Hide the child lists initially.
  $( '.list-expanding_child-list' ).hide();
}

// Expose public methods.
module.exports = { init: init };
