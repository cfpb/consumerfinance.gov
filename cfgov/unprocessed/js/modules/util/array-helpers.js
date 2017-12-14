/* ==========================================================================
   Arrays
   Utilities for checking arrays.
   ========================================================================== */


/**
 * Searches an array for the first object with the matching key:value pair
 * @param   {Array}  array  An array to query through for the expected value.
 * @param   {string} key    The key to check the value against.
 * @param   {string} val    The value to match to the key.
 * @returns {number}        Returns the index of a match, else -1
 */
function indexOfObject( array, key, val ) {
  let match = -1;

  if ( !array.length > 0 ) {
    return match;
  }

  array.forEach( function( item, index ) {
    if ( item[key] === val ) {
      match = index;
    }
  } );

  return match;
}

module.exports = {
  indexOfObject: indexOfObject
};
