/* ==========================================================================
   Atomic Checkers.

   Utilities for helping validate atomic design element architecture.
   ========================================================================= */

'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

/**
 * @param {HTMLNode} element
 *   The DOM element within which to search for the atomic element class.
 * @param {string} baseClass The CSS class name for the atomic element.
 * @param {string} atomicName
 *   The name of the atomic element in CapitalizedCamelCase.
 * @returns {HTMLNode} The DOM element for the atomic element.
 * @throws {Error} If DOM element passed into the atomic element is not valid.
 */
function validateDomElement( element, baseClass, atomicName ) {
  var msg;
  var dom;
  if ( !element || !element.classList ) {
    msg = element + ' passed to ' + atomicName + '.js is not valid. ' +
          'Check that element is a valid DOM node';
    throw new Error( msg );
  }

  dom = element.classList.contains( baseClass ) ?
        element : element.querySelector( '.' + baseClass );

  if ( !dom ) {
    msg = baseClass + ' not found on or in passed DOM node.';
    throw new Error( msg );
  }

  return dom;
}

// Expose public methods.
module.exports = {
  validateDomElement: validateDomElement
};
