import {
  applyAll,
  addEl,
  removeEl,
  addClass,
  removeClass,
  getEl,
} from './dom-tools.js';

let count = 1;

/**
 * Reset the address inputs to be only one input like when the page loaded.
 */
function reset() {
  count = 1;

  applyAll('.input-address', function (element) {
    if (element.getAttribute('name') === 'address1') {
      element.value = '';
      removeClass(element, 'error');
    } else {
      removeEl(element);
    }
  });

  removeClass('#add-another', 'u-hidden');
}

/**
 * Add a new address input (up to 10).
 */
function add() {
  count++;
  if (count === 10) {
    addClass('#add-another', 'u-hidden');
  }

  const previous = count - 1;

  if (getEl('#address' + previous).value === '') {
    addClass('#address' + previous, 'error');
  } else {
    removeClass('#address' + previous, 'error');
  }

  const addressElementContainer = getEl('#address1').cloneNode(true);
  addressElementContainer.setAttribute('id', 'address' + count);
  const addressElement = addressElementContainer.querySelector('input');
  addressElement.setAttribute('name', 'address' + count);
  addressElement.value = '';
  addEl('.input-container', addressElementContainer);
  addressElement.focus();
}

/**
 * Add an error class to an address input if it is empty.
 * @param {object} evt - A blur event object.
 */
function toggleError(evt) {
  const target = evt.target;
  if (evt.target.value === '') {
    addClass(target, 'error');
  } else {
    removeClass(target, 'error');
  }
}

export { reset, add, toggleError };
