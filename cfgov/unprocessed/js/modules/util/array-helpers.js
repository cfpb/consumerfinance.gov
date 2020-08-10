/* ==========================================================================
   Arrays
   Utilities for checking arrays.
   ========================================================================== */

/**
 * Searches an array for the first object with the matching key:value pair.
 * @param   {Array}  array - List to query through for the expected value.
 * @param   {string} key   - The key to check the value against.
 * @param   {string} val   - The value to match to the key.
 * @returns {number}       Returns the index of a match, otherwise -1.
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

/**
 * Ensure each primitive item in an array is unique.
 * Does not check uniqueness of objects.
 * @param  {Array} array - List of values.
 * @returns {Array}      Return processed list.
 */
function uniquePrimitives( array ) {
  return array.filter( ( val, i, self ) => self.indexOf( val ) === i );
}

export {
  indexOfObject,
  uniquePrimitives
};
