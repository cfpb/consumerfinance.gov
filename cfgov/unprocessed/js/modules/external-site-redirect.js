/* ==========================================================================
   External Site Redirect
   Used on all pages.
   Adds listener that redirects to /external-site/
   if clicked link URL is external.
   ========================================================================== */

'use strict';

/**
 * Set up event handler for links and determine if link is external or not.
 */
function init() {
  var elements = document.querySelectorAll( '#main, body > footer' );

  for ( var i = 0; i < elements.length; ++i ) {
    elements[i].addEventListener( 'click', _handleClick, false );
  }
}

/**
 * Handle the element click event.
 * @param {MouseEvent} event A click event.
 */
function _handleClick( event ) {
  var element = event.target;
  if ( element && element.tagName !== 'A' ) element = element.parentNode;
  if ( element === null || element.tagName !== 'A' ) return;

  // Regex to determine if link URL is external.
  // Futher explanation can be viewed
  // at https://regex101.com/r/xT7sL5/6.
  var externalURLArray =
    ( /(https?:\/\/(?:www\.)?(?![^\?]+gov)(?!(content\.)?localhost).*)/g )
    .exec( element.href );

  if ( Array.isArray( externalURLArray ) ) {
    event.preventDefault();
    window.location.href = '/external-site/?ext_url=' +
     encodeURIComponent( externalURLArray[1] );
  }
}

// Expose public methods.
module.exports = { init: init };
