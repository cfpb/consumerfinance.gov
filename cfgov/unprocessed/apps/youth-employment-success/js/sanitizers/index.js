const MONEY_REGEXP = /((\d*,?)*\.{1}\d*)/;
const MONEY_ONLY_REGEXP = /[^\d\.,]/;
const ALL_ZEROES_REGEXP = /^0+/g;
const NON_DECIMAL_ZERO_REGEXP = /^(0(?!\.\d{0,2}))/g;
const DIGITS_ONLY_REGEXP = /\D+/;

/**
 * From great Stack overflow answer here:
 * https://stackoverflow.com/a/2901298
 */
const COMMA_REGEXP = new RegExp( /\B(?=(\d{3})+(?!\d))/, 'g' );

/**
 * Add commas every 3 digits
 * @param {String} str The number string to add commas to
 * @returns {String} The number string with commas inserted every 3 digits
 */
function addCommas( str ) {
  return str.replace( /,/g, '' ).replace( COMMA_REGEXP, ',' );
}

/**
 * Removes all leading zeros from a string.
 * @param {String} str The string to strip
 * @returns {String} The string with leading zeros removed
 */
function stripLeadingZeros( str ) {
  // replace all zeros with at most 1 zero
  const withSingleZero = str.replace( ALL_ZEROES_REGEXP, '0' );

  if ( withSingleZero.length > 1 ) {
    return withSingleZero.replace( NON_DECIMAL_ZERO_REGEXP, '' );
  }

  return withSingleZero;
}

/**
 * Verify that the given string matches the money regex
 * @param {String} str The string to match against
 * @returns {String} Either the match, or the raw string for further processing
 */
function matchMoney( str ) {
  const matches = str.match( MONEY_REGEXP );

  if ( matches && matches.length ) {
    return matches[0];
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
const stripNonMoneyCharacters = stripInvalidChars( new RegExp( MONEY_ONLY_REGEXP, 'g' ) );
const truncateTo2 = truncateTo( 2 );

const _moneySanitizers = [
  stripLeadingZeros,
  stripNonMoneyCharacters,
  matchMoney,
  truncateTo2,
  addCommas
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
