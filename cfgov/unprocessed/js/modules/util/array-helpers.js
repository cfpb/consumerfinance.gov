/* ==========================================================================
   Arrays

   Utilities for checking arrays.
   ========================================================================== */

'use strict';

/**
 * @param   {array} array    An array to query through for the expected value.
 * @param   {string} val     The value to query for.
 * @returns {boolean|object} Returns false if the array is empty or there's
 *                           no match, otherwise returns the matched object
 *                           containing the value.
 */
function valInArray( array, val ) {
  var match = false;

  if ( !array.length > 0 ) {
    return match;
  }

  array.forEach( function( item, index ) {
    if ( item.value === val ) {
      match = {
        index: index,
        item: item
      };
    }
  } );

  return match;
}

module.exports = {
  valInArray: valInArray
};
