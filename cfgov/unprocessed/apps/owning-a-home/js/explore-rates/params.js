import { getSelection } from './dom-values';

let UNDEFINED;

/* List all the parameters the user can change and set
   their default values.

   dp-constant: track the down payment interactions
   request: Keep the AJAX request accessible so we can terminate it if needed.
*/
const _params = {
  'credit-score': 700,
  'down-payment': '20,000',
  'dp-constant': '',
  'house-price': '200,000',
  location: 'AL',
  'loan-amount': UNDEFINED,
  'rate-structure': 'fixed',
  'loan-term': 30,
  'loan-type': 'conf',
  'arm-type': '5-1',
  edited: false,
  isJumbo: false,
  prevLoanType: '',
  prevLocation: '',
  request: UNDEFINED,
};

/**
 * @returns {object} Underlying object of parameters.
 */
function getAllParams() {
  return _params;
}

/**
 * Retrieve a value from inside the params object.
 * @param {string} key - The key for a property within the params object.
 * @returns {string|number|Array|undefined} The key on the params object to get.
 */
function getVal(key) {
  return _params[key];
}

/**
 * Set a value inside the params object.
 * @param {string} key - The key on the params object to set.
 * @param {string|number|Array|undefined} val - The value to set on `key`.
 */
function setVal(key, val) {
  _params[key] = val;
}

/**
 * Update the values inside the internal params object.
 */
function update() {
  _params.prevLoanType = _params['loan-type'];
  _params.prevLocation = _params.location;

  let val;
  let param;
  for (param in _params) {
    if (Object.prototype.hasOwnProperty.call(_params, param)) {
      val = getSelection(param);
      if (
        param !== 'prevLoanType' &&
        param !== 'prevLocation' &&
        val !== UNDEFINED &&
        val !== null
      ) {
        _params[param] = getSelection(param);
      }
    }
  }
}

export { getAllParams, getVal, setVal, update };
