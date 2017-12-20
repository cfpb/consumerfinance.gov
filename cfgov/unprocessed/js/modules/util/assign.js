/* ==========================================================================
   Assign
   Code copied from the following with moderate modifications :
   - https://github.com/maslennikov/shallow-extend
   Copyright (c) 2014 Alexey Maslennikov
   ========================================================================== */

/**
 * @param {object} object - JavaScript object.
 * @returns {boolean} True if object is plain Javascript object.
 */
function _isPlainObject( object ) {
  return Object.prototype.toString.call( object ) === '[object Object]';
}

/**
 * Copies properties of all sources to the destination object overriding its own
 * existing properties. When assigning from multiple sources, fields of every
 * next source will override same named fields of previous sources.
 *
 * @param {Object} destination object.
 * @returns {Object} assigned destination object.
 */
function assign( destination ) {
  destination = destination || {};
  let hasOwnProp;
  for ( let i = 1; i < arguments.length; i++ ) {
    const source = arguments[i] || {};
    hasOwnProp = Object.hasOwnProperty.bind( source );
    for ( const key in source ) {
      if ( hasOwnProp( key ) ) {
        const value = source[key];
        if ( _isPlainObject( value ) ) {
          assign( destination[key] = {}, value );
        } else {
          destination[key] = source[key];
        }
      }
    }
  }
  return destination;
}

// Expose public methods.
module.exports = { assign: assign };
