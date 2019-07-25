import DT from './dom-tools';

let types = {};
let totalCount = 0;

/**
 * Reset the counter.
 */
function reset() {
  DT.changeElHTML( '.counter', '0' );
  types = {};
  totalCount = 0;
}

/**
 * Update the count of addresses.
 * @param {number} number - The number of this address.
 */
function updateAddressCount( number ) {
  DT.changeElText( '#addressCount', number );
}

/**
 * Add one to the total address count.
 */
function incrementTotal() {
  const totalCountElement = DT.getEl( '#totalCnt' );
  const addressCount = parseInt( DT.getEl( '#addressCount' ).textContent, 10 );

  // add one to the total
  totalCount++;

  DT.changeElText( totalCountElement, totalCount );

  // hide spinner
  if ( totalCount === addressCount ) {
    DT.addClass( '#spinner', 'u-hidden' );
  }
}

/**
 * Update the address count by type.
 * @param {string} type -
 *   The address type (duplicate, notFound, notRural, rural).
 */
function updateCount( type ) {
  let noun = 'addresses';
  let verb = 'are';

  const countElements = DT.getEls( '.' + type + 'Cnt' );
  // add one to correct type
  let typeCount = types[type] || 0;
  types[type] = ++typeCount;
  DT.changeElText( countElements, typeCount );

  if ( typeCount === 1 ) {
    noun = 'address';
    verb = 'is';
  }

  DT.changeElText( '.' + type + 'Verb', verb );
  DT.changeElText( '.' + type + 'Case', noun + ' ' + verb );

  this.incrementTotal();
}

export default {
  reset,
  updateAddressCount,
  incrementTotal,
  updateCount
};
