const _centsPerDollar = 100;
const _decimals = 2;
const _dollarsToPrecisionRegexp = new RegExp( `(\\d+\\.?\\d{0,${ _decimals }})` );

/**
 * Converts an input string into a scaled dollar value, or zero.
 * @param {String} dollars Amount as string
 * @returns {Number} Scaled amount in dollars and cents,
 *  fixed to no more than 2 decimal places.
 */
function toDollars( dollars ) {
  const safeDollars = typeof dollars === 'string' ? dollars : String( dollars );
  const matches = safeDollars.match( _dollarsToPrecisionRegexp );
  const dollarsFixed = ( matches && matches[0] ) || 0;

  return dollarsFixed * _centsPerDollar / _centsPerDollar;
}

const dollars = {
  toDollars,

  /**
   * Adds two dollar values
   * @param {Number} a The first value to add
   * @param {Number} b The second value to add
   * @returns {Number} The sum of the two values
   */
  add( a, b ) {
    return toDollars( a ) + toDollars( b );
  },

  /**
   * Subtracts two dollar values
   * @param {Number} a The first value to subtract
   * @param {Number} b The second value to subtract
   * @returns {Number} The difference of the two values
   */
  subtract( a, b ) {
    const subtracted = toDollars( a ) - toDollars( b );

    return subtracted % 1 ? subtracted.toFixed( 2 ) : subtracted;
  }
};

export default dollars;
