/**
 * Converts a number to a money string.
 * @param {number} num - A number to be converted.
 * @returns {string} money A string representing currency.
 */
function numToMoney( num ) {
  let money;
  // When num is a string, we should, ironically, strip its numbers first.
  if ( typeof num === 'string' ) {
    num = Number( num.replace( /[^0-9\.]+/g, '' ) );
  }
  if ( typeof num === 'object' ) {
    num = 0;
  }

  // Whether amount is negative or not.
  const sign = num < 0 ? '-' : '';

  const numProc = String(
    parseInt( num = Math.abs( Number( num ) || 0 ).toFixed( 0 ), 10 )
  );
  let groups = 0;
  if ( numProc.length > 3 ) {
    groups = numProc.length % 3;
  }

  money = sign + '$';

  const separator = ',';
  if ( groups > 0 ) {
    money += numProc.substr( 0, groups ) + separator;
  }
  money += numProc.substr( groups )
    .replace( /(\d{3})(?=\d)/g, '$1' + separator );

  return money;
}

export default numToMoney;
