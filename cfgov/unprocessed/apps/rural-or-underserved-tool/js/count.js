import {
  addClass,
  changeElHTML,
  changeElText,
  getEl,
  getEls,
} from './dom-tools.js';

let types = {};
let totalCount = 0;

/**
 * Reset the counter.
 */
function reset() {
  changeElHTML('.counter', '0');
  types = {};
  totalCount = 0;
}

/**
 * Update the count of addresses.
 * @param {number} number - The number of this address.
 */
function updateAddressCount(number) {
  changeElText('#addressCount', number);
}

/**
 * Add one to the total address count.
 */
function incrementTotal() {
  const totalCountElement = getEl('#totalCnt');
  const addressCount = parseInt(getEl('#addressCount').textContent, 10);

  // add one to the total
  totalCount++;

  changeElText(totalCountElement, totalCount);

  // hide spinner
  if (totalCount === addressCount) {
    addClass('#spinner', 'u-hidden');
  }
}

/**
 * Update the address count by type.
 * @param {string} type - The address type
 *   (duplicate, notFound, notRural, rural).
 */
function updateCount(type) {
  let noun = 'addresses';
  let verb = 'are';
  const countElements = getEls('.' + type + '-cnt');
  // add one to correct type
  let typeCount = types[type] || 0;
  types[type] = ++typeCount;
  changeElText(countElements, typeCount);

  if (typeCount === 1) {
    noun = 'address';
    verb = 'is';
  }

  changeElText('.' + type + 'Verb', verb);
  changeElText('.' + type + 'Case', noun + ' ' + verb);

  incrementTotal();
}

export { reset, updateAddressCount, incrementTotal, updateCount };
