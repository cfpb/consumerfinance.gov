/* ==========================================================================
 Polyfill for querySelector and querySelectorAll.
 Copied from https://gist.github.com/chrisjlee/8960575.
 ========================================================================== */

'use strict';

if ( !document.querySelectorAll ) {
  document.querySelectorAll = function( selectors ) {
    var style = document.createElement( 'style' ), elements = [], element;
    document.documentElement.firstChild.appendChild( style );
    document._qsa = [];

    style.styleSheet.cssText = selectors +
                               '{x-qsa:expression' +
                               '(document._qsa && document._qsa.push(this))}';
    window.scrollBy( 0, 0 );
    style.parentNode.removeChild( style );

    while ( document._qsa.length ) {
      element = document._qsa.shift();
      element.style.removeAttribute( 'x-qsa' );
      elements.push( element );
    }
    document._qsa = null;
    return elements;
  };
}

if ( !document.querySelector ) {
  document.querySelector = function( selectors ) {
    var elements = document.querySelectorAll( selectors );
    return elements.length ? elements[0] : null;
  };
}
