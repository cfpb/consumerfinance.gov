/**
 * decimalToPercentString - Format decimal into a percentage string.
 * @param {number} number - Number to be formatted.
 * @param {number} decimalPlaces - Number of decimal places to display,
 *   default 2.
 * @returns {string} Formatted percentage version of decimal.
 */
function decimalToPercentString(number, decimalPlaces) {
  if (typeof decimalPlaces === 'undefined') decimalPlaces = 2;
  return Number(number).toLocaleString('en-US', {
    style: 'percent',
    minimumFractionDigits: decimalPlaces,
  });
}

/**
 * enforceRange - Force a number between a range.
 * @param {number} n - Number to be checked.
 * @param {number} min - Minimum value of n.
 * @param {number} max - Maximum value of n.
 * @returns {object} Error data on whether the min or max was enforced.
 */
function enforceRange(n, min, max) {
  let error = false;

  if (typeof min === 'undefined') min = false;
  if (typeof max === 'undefined') max = false;

  if (max < min || typeof n !== typeof min) {
    return false;
  }

  if (max !== false && n > max) {
    n = max;
    error = 'max';
  }

  if (min !== false && n < min) {
    n = min;
    error = 'min';
  }

  return {
    value: n,
    error: error,
  };
}

/**
 * isNumeric - Verify that a value contains only number or decimal characters.
 * @param {*} value - Value to be checked.
 * @returns {boolean} True if value only contains numeric characters,
 *   false otherwise.
 */
function isNumeric(value) {
  return /^[\d.]+$/.test(value);
}

export { enforceRange, decimalToPercentString, isNumeric };
