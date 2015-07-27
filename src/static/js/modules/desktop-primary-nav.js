/* ==========================================================================
   Desktop Menu Transitions
   Do not apply a transition when hovering from one menu to the next
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  var $desktopMenu = $( '.primary-nav' ),
      $desktopMenuTrigger = $( '.primary-nav_top-level-list > li' ),
      $subNavs = $( '.sub-nav_wrapper' ),
      mouseIsInsideMenu = false,
      mouseIsInsideMenuItem = false,
      aMenuItemWasOpened = false,
      isSmall = $( '.sliding-nav_trigger' ).is( ':visible' );

  // On window resize, set the isSmall variable again.
  $( window ).resize( function() {
    isSmall = $( '.sliding-nav_trigger' ).is( ':visible' );
  } );

  // Set default state for all sub-navs.
  $subNavs.attr( 'aria-expanded', 'false' );

  $desktopMenu.mouseleave( function() {
    // Update the mouse and menu state
    aMenuItemWasOpened = false;
    mouseIsInsideMenu = false;

    // Always use a transition when the mouse leaves the entire menu
    $desktopMenu.addClass( 'has-transition' );
  } );

  $desktopMenuTrigger.click( function() {
    if ( !isSmall ) {
      var $subNav = $( this ).find( '.sub-nav_wrapper' );
      var isExpanded = $subNav.attr( 'aria-expanded' ) === 'true';
      $subNav.attr( 'aria-expanded', !isExpanded );
    }
  } );

  $desktopMenuTrigger.mouseenter( function() {

    if ( !isSmall ) {
      var $subNav = $( this ).find( '.sub-nav_wrapper' );
      // Update aria-expanded
      $subNav.attr( 'aria-expanded', 'true' );

      // Show the child list, previously hidden by default for the mobile menu.
      $subNav.find( '.sub-nav_title' ).css('display', 'block');
      $subNav.find( '.list-expanding_child-list' ).css('display', 'inline-block');

      if ( aMenuItemWasOpened === false ) {
        $desktopMenu.addClass( 'has-transition' );
      } else {
        $desktopMenu.removeClass( 'has-transition' );
      }

      // Update the mouse and menu state
      mouseIsInsideMenu = true;
      mouseIsInsideMenuItem = true;
      aMenuItemWasOpened = true;
    }

  } );

  $desktopMenuTrigger.mouseleave( function() {

    if ( !isSmall ) {
      // Update the menu item state
      mouseIsInsideMenuItem = false;

      // Use a delay to check if the mouse is inside of the menu but not in a
      // list item.
      window.setTimeout( function updateAMenuItemWasOpened() {
        if ( mouseIsInsideMenuItem === false && mouseIsInsideMenu ) {
          aMenuItemWasOpened = false;
        }
      }, 100 );

      // Update aria-expanded
      $( this ).find( '.sub-nav_wrapper' ).attr( 'aria-expanded', 'false' );
    }
  } );
}

// Expose public methods.
module.exports = { init: init };
