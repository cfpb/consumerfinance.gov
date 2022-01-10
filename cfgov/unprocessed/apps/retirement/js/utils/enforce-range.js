/**
 * This function ensures ( min <= n <= max ) by setting n to the min
 * or the max if it falls outside the range. If min or max is set to
 * false, then that limit is not enforced.
 * @param {number} n The number to be forced into the range
 * @param {number|bool} min The minimum value, or false if not enforced
 * @param {number|bool} max The maximum value, or false if not enforced
 * @returns {number} The number after range is enforced
*/
function enforceRange( n, min, max ) {
  if ( max < min || typeof n !== typeof min ) {
    return false;
  }
  if ( n > max && max !== false ) {
    n = max;
  }
  if ( n < min && min !== false ) {
    n = min;
  }
  return n;
}

export default enforceRange;
