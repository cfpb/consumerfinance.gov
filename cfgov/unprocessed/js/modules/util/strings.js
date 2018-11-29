/**
 * Escapes a string.
 * @param   {string} s The string to escape.
 * @returns {string}   The escaped string.
 */
function stringEscape( s ) {
  return s.replace( /[-\\^$*+?.()|[\]{}]/g, '\\$&' );
}

/**
 * Tests whether a string contains special characters.
 * @param   {string}  s The string to test.
 * @returns {boolean}
 *   True if string `s` contains special characters, false otherwise.
 */
function stringValid( s ) {
  return !( /[~`!.#$%^&*+=[\]\\';,/{}|\\":<>?]/g ).test( s );
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
  stringValid,
  stringMatch
};
