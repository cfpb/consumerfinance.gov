/**
 * Turns a string into a number.
 * Assumes each number in the string should be preserved (unlike parseInt)
 * Assumes the first instance of a decimal point is the intended one
 * @param  {string} numberString  A string representing a number
 * @returns {number} The assumed numeric value of numberString
 */
function stringToNum( numberString ) {
  if ( typeof numberString === 'number' ) {
    return numberString;
  } else if ( typeof numberString !== 'string' ) {
    return 0;
  }
  let signMaker = 1;
  const minusPosition = numberString.indexOf( numberString.match( '-' ) );
  const digitPosition = numberString.indexOf( numberString.match( /\d/ ) );

  // If a '-' appears before the first digit, we assume numberString is negative
  if ( numberString.indexOf( numberString.match( '-' ) ) !== -1 &&
    minusPosition < digitPosition ) {
    signMaker = -1;
  }

  // Strip non-numeric values, maintaining periods
  numberString = numberString.replace( /[^0-9\.]+/g, '' );

  // Strip any periods after the first
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

/**
 * decimalToPercentString - Format decimal into a percentage string
 * @param {Number} number - Number to be formatted
 * @param {Number} decimalPlaces - Number of decimal places to display, default 2
 * @returns {String} Formatted percentage version of decimal
 */
function decimalToPercentString( number, decimalPlaces ) {
  if ( typeof decimalPlaces === 'undefined' ) decimalPlaces = 2;
  return Number( number )
    .toLocaleString( 'en-US',
      { style: 'percent',
        minimumFractionDigits: decimalPlaces } );
}

/**
 * enforceRange - Force a number between a range
 * @param {Number} n - Number to be checked
 * @param {Number} min - Minimum value of n
 * @param {Number} max - Maximum value of n
 * @returns {Object} Error data on whether the min or max was enforced
 */
function enforceRange( n, min, max ) {
  let error = false;

  if ( typeof min === 'undefined' ) min = false;
  if ( typeof max === 'undefined' ) max = false;

  if ( max < min || typeof n !== typeof min ) {
    return false;
  }

  if ( max !== false && n > max ) {
    n = max;
    error = 'max';
  }

  if ( min !== false && n < min ) {
    n = min;
    error = 'min';
  }

  return {
    value: n,
    error: error
  };
}

/**
 * isNumeric - Verify that a value contains only number or decimal characters
 * @param {*} value Value to be checked
 * @returns {Boolean} True if value only contains numeric characters, false otherwise
 */
function isNumeric( value ) {
  return ( /^[\d.]+$/ ).test( value );
}

export {
  enforceRange,
  stringToNum,
  decimalToPercentString,
  isNumeric
};
