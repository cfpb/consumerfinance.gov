/*
 * ======================================================================
 * Aria Button
 * ======================================================================
 */

'use strict';

var $ = require( 'jquery' );

function init() {

  $.fn.cfpbAriaButton = function( userSettings ) {

    return this.each( function() {

      var $this = $( this );

      // Add aria attributes.
      $this.attr( 'role', 'button' );
      $this.attr( 'aria-pressed', 'false' );
      $this.attr( 'tabindex', '0' );

      // Toggle the aria-pressed attributes.
      $this.click( function() {
        togglePressedVal( $this );
      } );
      $this.keyup( function( event ) {
        // Space key pressed.
        if ( event.which === 32 ) {
          event.preventDefault();
          togglePressedVal( $this );
        }
      });
      // Prevent the spacebar from scrolling the page.
      $this.keydown( function( event ) {
        // Space key pressed.
        if ( event.which === 32 ) {
          event.preventDefault();
        }
      } );
    } );

    function togglePressedVal( jqueryObject ) {
      var toggledPressedVal = toggleBoolean( jqueryObject.attr( 'aria-pressed' ) );
      jqueryObject.attr( 'aria-pressed', toggledPressedVal );
    }

    function toggleBoolean( userBoolean ) {
      var typedBoolean;
      if ( typeof userBoolean === 'boolean' ) {
        typedBoolean = userBoolean;
      } else if ( typeof userBoolean === 'string' ) {
        typedBoolean = userBoolean === 'true' ? true : false;
      }
      return !typedBoolean;
    }
  };
}

module.exports = { init: init };
