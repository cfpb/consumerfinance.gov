'use strict';

/**
 * Turns a string into a number.
 * Assumes each number in the string should be preserved (unlike parseInt)
 * Assumes the first instance of a decimal point is the intended one
 * @param  {string} numberString  A string representing a number
 * @returns {number} The assumed numeric value of numberString
 */
function handleStringInput( numberString ) {
  if ( typeof numberString === 'number' ) {
    return numberString;
  }
  var signMaker = 1,
      minusPosition = numberString.indexOf( numberString.match( '-' ) ),
      digitPosition = numberString.indexOf( numberString.match( /\d/ ) );

  // If an 'e' is the only non-numeric character, we assume scientific notation
  if ( numberString.replace( /[0-9\.\-]/g, '' ) === 'e' ) {
    return Number( numberString );
  }

  // If a '-' appears before the first digit, we assume numberString is negative
  if ( numberString.indexOf( numberString.match( '-' ) ) !== -1 &&
    minusPosition < digitPosition ) {
    signMaker = -1;
  }

  // Strip non-numeric values, maintaining periods
  numberString = numberString.replace( /[^0-9\.]+/g, '' );

  /**
   * Function passed to the JavaScript .replace() method to be invoked after
    the match has been performed. Strips any periods after the first.
   * @param  {String} match -   The matched substring.
   * @param  {Number} offset -  The offset of the matched substring within the
    whole string being examined.
   * @param  {String} full - The full string being examined.
   * @returns {String} period or empty string
   */
  function replaceCommas( match, offset, full ) {
    if ( offset === full.indexOf( '.' ) ) {
      return '.';
    }
    return '';
  }
  numberString = numberString.replace( /\./g, replaceCommas );

  // Get number value of string, then multiply by signMaker and return
  return Number( numberString ) * signMaker;

}

module.exports = handleStringInput;
