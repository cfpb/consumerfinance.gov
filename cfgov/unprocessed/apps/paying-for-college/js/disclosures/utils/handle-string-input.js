/**
 * Turns a string into a number.
 * Assumes each number in the string should be preserved (unlike parseInt).
 * Assumes the first instance of a decimal point is the intended one.
 *
 * @param {string} numberString - A string representing a number.
 * @returns {number} The assumed numeric value of numberString.
 */
function handleStringInput(numberString) {
  if (typeof numberString === 'number') {
    return numberString;
  }

  if (typeof numberString === 'undefined') {
    return 0;
  }

  let signMaker = 1;
  const minusPosition = numberString.indexOf(numberString.match('-'));
  const digitPosition = numberString.indexOf(numberString.match(/\d/));

  // If a '-' appears before the first digit, we assume numberString is negative
  if (
    numberString.indexOf(numberString.match('-')) !== -1 &&
    minusPosition < digitPosition
  ) {
    signMaker = -1;
  }

  // Strip non-numeric values, maintaining periods
  numberString = numberString.replace(/[^0-9.]+/g, '');

  /**
   * This helper function places commas in the string. It's set up to
   * be passed as a parameter to String.replace()
   *
   * @param {string} match - The matched substring.
   * @param {number} offset - The numeric offset of the matched substring.
   * @param {string} full - The full string to be matched against.
   * @returns {string} new string to replace.
   */
  function replaceCommas(match, offset, full) {
    if (offset === full.indexOf('.')) {
      return '.';
    }
    return '';
  }
  numberString = numberString.replace(/\./g, replaceCommas);

  // Get number value of string, then multiply by signMaker and return
  return Number(numberString) * signMaker;
}

module.exports = handleStringInput;
