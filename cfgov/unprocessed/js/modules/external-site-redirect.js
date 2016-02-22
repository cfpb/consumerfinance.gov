/* ==========================================================================
   External Site Redirect
   Used on all pages.
   Adds listener that redirects to /external-site/
   if clicked link URL is external.
   ========================================================================== */

'use strict';
var $ = require( 'jquery' );

/**
 * Set up event handler for links and determine if link is external or not.
 */
function init() {
  $( '#main, footer' ).on( 'click', 'a', function( event ) {

    var url = this.href;
    // Regex to determine if link URL is external.
    // Futher explanation can be viewed
    // at https://regex101.com/r/xT7sL5/2.
    var externalURLArray =
        ( /(https?:\/\/(?:www\.)?(?!.*gov)(?!(content\.)?localhost).*)/g )
        .exec( url );

    if ( $.isArray( externalURLArray ) ) {
      event.preventDefault();
      window.location = '/external-site/?ext_url=' +
                        encodeURIComponent( externalURLArray[1] );
    }

  } );
}

// Expose public methods.
module.exports = { init: init };
