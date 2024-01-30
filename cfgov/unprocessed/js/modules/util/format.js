/**
 * Turns a string into a number.
 * Assumes each number in the string should be preserved (unlike parseInt)
 * Assumes the first instance of a decimal point is the intended one.
 * @param  {string} numberString - A string representing a number.
 * @returns {number} The assumed numeric value of numberString
 */
function convertStringToNumber(numberString) {
  if (typeof numberString === 'number') {
    return numberString;
  } else if (typeof numberString !== 'string') {
    return 0;
  }

  let signMaker = 1;
  const minusPosition = numberString.indexOf(numberString.match('-'));
  const digitPosition = numberString.indexOf(numberString.match(/\d/));

  // If a '-' appears before the first digit, we assume numberString is negative
  if (minusPosition !== -1 && minusPosition < digitPosition) {
    signMaker = -1;
  }

  // Strip non-numeric values, maintaining periods
  numberString = numberString.replace(/[^0-9.]+/g, '');

  numberString = numberString.replace(/\./g, stripExtraPeriods);

  // Get number value of string, then multiply by signMaker and return
  return Number(numberString) * signMaker;
}

/**
 * Strip any periods after the first.
 * @param {string} match - The matched substring.
 * @param {number} offset - The numeric offset of the matched substring.
 * @param {string} full - The full string to be matched against.
 * @returns {string} new string to replace.
 */
function stripExtraPeriods(match, offset, full) {
  if (offset === full.indexOf('.')) {
    return '.';
  }
  return '';
}

/**
 * @param {string} numberString - A string representing a number.
 * @returns {string} The number in a comma-separated format.
 */
function commaSeparate(numberString) {
  const string = numberString.toString();
  // split string of number by the decimal point
  const parts = string.split('.');
  // format the whole number part of the string with a regex
  let formattedValue = parts[0].replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
  // Add back decimal part if it exists
  if (typeof parts[1] !== 'undefined') {
    formattedValue += '.' + parts[1];
  }

  return formattedValue;
}

/**
 * @param {object} opts - The options object
 * @param {number|string} opts.amount - The number or string to be formatted
 * @param {number} opts.decimalPlaces - Optionally specify the number of decimal places
 *   you'd like in the returned string
 * @returns {string}      The number in USD format.
 */
function formatUSD(opts) {
  const num = opts.amount;
  let decPlaces = 0;
  let sign = '';
  let numericValue = num;
  let stringValue = '';
  let formattedString = '';

  // Handle a String as input
  if (typeof num === 'string') {
    numericValue = convertStringToNumber(num);
  }

  // Determine sign
  if (numericValue < 0) {
    sign = '-';
  }

  opts = opts || {};

  // Determine decimal places
  decPlaces = Math.abs(opts.decimalPlaces);
  if (isNaN(decPlaces)) {
    decPlaces = 2;
  }

  // Get absolute value, apply decimal places limit, return string
  stringValue = Math.abs(numericValue).toFixed(decPlaces);

  // Get a comma-separated string of the absolute value of numericValue
  stringValue = commaSeparate(stringValue);

  // Construct the formattedString
  formattedString = sign + '$' + stringValue;

  return formattedString;
}

export { convertStringToNumber, commaSeparate, formatUSD };
