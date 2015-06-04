/* ==========================================================================
   Shallow Extends
   Copyright (c) 2014 Alexey Maslennikov
   ========================================================================== */

'use strict';


/**
* @param {object} JavaScript object.
* @returns {boolean} True if object is plain Javascript object.
*/

function _isPlainObject( object ) {
  return toString.call( object ) === '[object Object]';
}

/**
* Copies properties of all sources to the destination object overriding its own
* existing properties. When extending from multiple sources, fields of every
* next source will override same named fields of previous sources.
*
* @param {object} destination object.
* @returns {bbject} extended destination object.
*/

function extend( destination ) {
  destination = destination || {};

  for ( var i = 1; i < arguments.length; i++ ) {
    var source = arguments[i] || {};
    for ( var key in source ) {
      if ( source.hasOwnProperty( key ) ) {
        var value = source[key];
        if ( _isPlainObject( value ) ) {
          extend( destination[key] = {}, value );
        }else {
          destination[key] = source[key];
        }
      }
    }
  }
  return destination;
}

// Expose public methods.
module.exports = { extend: extend };
