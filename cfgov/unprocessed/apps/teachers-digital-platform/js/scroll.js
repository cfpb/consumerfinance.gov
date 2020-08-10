const smoothscroll = require( 'smoothscroll-polyfill' );
const scrollIntoView = require( '../../../js/modules/util/scroll' ).scrollIntoView;

const scroll = {
  init: () => {
    let jumplinks = document.querySelectorAll( '[data-scroll]' );

    smoothscroll.polyfill();

    // IE doesn't support forEach w/ node lists so convert it to an array.
    jumplinks = Array.prototype.slice.call( jumplinks );
    jumplinks.forEach( function( jumplink ) {
      jumplink.addEventListener( 'click', function( event ) {
        const target = document.querySelector( jumplink.hash );
        // Disable default browser behavior.
        event.preventDefault();

        // Scroll smoothly to the target.
        scrollIntoView( target, { behavior: 'smooth', block: 'start', offset: 0 } );

        // Update url hash.
        if ( history.pushState ) {
          history.pushState( null, null, jumplink.hash );
        } else {
          location.hash = jumplink.hash;
        }

        // Wait half a second for scrolling to finish.
        setTimeout( function() {

          // Make sure focus is set to the target.
          target.setAttribute( 'tabindex', '-1' );
          target.focus( { preventScroll: true } );
        }, 500 );
      }, false );
    } );
  }
};

module.exports = scroll;
