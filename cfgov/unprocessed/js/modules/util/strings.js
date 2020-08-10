/**
 * Escapes a string.
 * @param   {string} s The string to escape.
 * @returns {string}   The escaped string.
 */
function stringEscape( s ) {
  return s.replace( /[-\\^$*+?.()|[\]{}]/g, '\\$&' );
}

/**
 * Tests whether a string matches another.
 * @param   {string}  x The control string.
 * @param   {string}  y The comparison string.
 * @returns {boolean}   True if `x` and `y` match, false otherwise.
 */
function stringMatch( x, y ) {
  return RegExp( stringEscape( y.trim() ), 'i' ).test( x );
}

export {
  stringEscape,
  stringMatch
};
