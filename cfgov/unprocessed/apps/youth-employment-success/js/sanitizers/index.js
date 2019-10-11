const MONEY_REGEXP = /[^\d+\.{1}\d+]/;
const DIGITS_ONLY_REGEXP = /\D+/;

/**
 * Removes all leading zeros from a string with more than 1 character.
 * @param {String} str The string to strip
 * @returns {String} The string with leading zeros removed
 */
function stripLeadingZeros( str ) {
  if ( str.length && str.length > 1 ) {
    let index = 0;

    while ( index < str.length ) {
      const char = str[index];

      if ( char !== '0' ) {
        return str.slice( index );
      }

      index += 1;
    }
  }

  return str;
}

/**
 * Remove invalid characters from a string
 * @param {RegExp} matcher A regular expression that represents the values to be stripped from a string
 * @returns {Function} Curried function that accepts a string to be updated
 */
function stripInvalidChars( matcher ) {
  return function strip( str ) {
    const stripped = str.replace( matcher, '' );
    return stripped;
  };
}

/**
 * Truncate a string to a number of places following a decimal point
 * @param {Number} length The number of places to truncate to
 * @returns {Function} Curried function that accepts a string to be truncated
 */
function truncateTo( length ) {
  return function truncater( str ) {
    const decimalIndex = str.indexOf( '.' );
    const whole = str.slice( 0, decimalIndex );
    const decimal = str.slice( decimalIndex );

    if ( decimal.length > length + 1 ) {
      return `${ whole }${ decimal.slice( 0, length + 1 ) }`;
    }

    return str;
  };
}

const stripNonDigitChars = stripInvalidChars( new RegExp( DIGITS_ONLY_REGEXP, 'g' ) );
const stripNonMoneyChars = stripInvalidChars( new RegExp( MONEY_REGEXP, 'g' ) );
const truncateTo2 = truncateTo( 2 );

const _moneySanitizers = [
  stripLeadingZeros,
  stripNonMoneyChars,
  truncateTo2
];
const _numberSanitizers = [
  stripLeadingZeros,
  stripNonDigitChars
];

/**
 * Sanitize a string by reducing it through the function chain in _moneySanitizers
 * @param {String} str The string to sanitize
 * @returns {String} The sanitized string
 */
function sanitizeMoney( str ) {
  return _moneySanitizers.reduce( ( memo, sanitizer ) => sanitizer( memo ), str );
}

/**
 * * Sanitize a string by reducing it through the function chain in _numberSanitizers
 * @param {String} str The string to sanitize
 * @returns {String} The sanitized string
 */
function sanitizeNumbers( str ) {
  return _numberSanitizers.reduce( ( memo, sanitizer ) => sanitizer( memo ), str );
}

const sanitizeMap = {
  money: sanitizeMoney,
  number: sanitizeNumbers
};

export default sanitizeMap;
