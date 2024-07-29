// This file contains the 'view' of all financial info, including costs, loans, etc

import { convertStringToNumber } from '../../../../../js/modules/util/format.js';
import { decimalToPercentString } from '../util/number-utils.js';
import {
  getFinancialValue,
} from '../dispatchers/get-model-values.js';
import { updateFinancial } from '../dispatchers/update-models.js';
import { formatUSD } from '../../../../../js/modules/util/format.js';
import { selectorMatches } from '../util/other-utils.js';
import { updateUrlQueryString } from '../dispatchers/update-view.js';

const financialView = {
  _financialItems: [],
  _inputChangeTimeout: null,
  _calculatingTimeout: null,
  _currentInput: null,
  // _costsOfferButton: null,
  _gradProgramContent: null,
  _undergradProgramContent: null,

  /**
   * Event handling for "see steps" action plan button.
   */
  _handleSeeStepsClick: function () {
    // TODO - This could all be written better.
    const selected = document.querySelector(
      '.action-plan__choices .highlighted input[checked="true"]',
    );
    document.querySelectorAll('[data-action-plan]').forEach((elem) => {
      elem.classList.remove('active');
    });
    document
      .querySelector('[data-action-plan="' + selected.value + '"]')
      .classList.add('active');
    document
      .querySelector('.action-plan .action-plan__feeling-gauge')
      .classList.add('active');
  },

  updateFinancialItems: function () {
    this._financialItems.forEach((elem) => {
      if (!selectorMatches(elem, ':focus')) {
        const prop = elem.dataset.financialItem;
        const isRate = prop.slice(0, 5) === 'rate_';
        const isFee = prop.slice(0, 4) === 'fee_';
        const isHours = prop.slice(-5) === 'Hours';
        const isNumber = elem.dataset.isNumber === 'true';
        let val = getFinancialValue(prop);

        // Prevent improper property values from presenting on the page
        if (val === false || val === null || isNaN(val)) val = 0;
        if (isFee) {
          val = decimalToPercentString(val, 3);
        } else if (isRate) {
          val = decimalToPercentString(val, 2);
        } else if (isNumber) {
          val = Math.round(val * 100) / 100;
        } else if (isHours) {
          val = Math.round(val * 10) / 10 + ' hours';
        } else {
          val = formatUSD({ amount: val, decimalPlaces: 0 });
        }

        if (elem.tagName === 'INPUT') {
          elem.value = val;
        } else {
          elem.innerText = val;
        }
      }
    });
  },

  /* init - Initialize the financialView object */
  init: function () {
    this._financialItems = document.querySelectorAll('[data-financial-item]');
    this._financialInputs = document.querySelectorAll(
      'input[data-financial-item]',
    );
    this._financialSpans = document.querySelectorAll(
      'span[data-financial-item]',
    );
    // this._costsOfferButton = document.querySelector(
    //   '.costs__button-section button',
    // );
    _addInputListeners();
    _addButtonListeners();
  },
};

/**
 * Listeners for INPUT fields and radio buttons.
 */
function _addInputListeners() {
  financialView._financialInputs.forEach((elem) => {
    elem.addEventListener('keyup', _handleInputChange);
    elem.addEventListener('focusout', _handleInputChange);
    elem.addEventListener('click', _handleInputClick);
  });
}

/**
 * Listeners for INPUT fields and radio buttons.
 */
function _addButtonListeners() {
  // TODO: Remove this, assumimg it is not going to be used
  // financialView._costsOfferButton.addEventListener(
  //   'click',
  //   _handleCostsButtonClick,
  // );
}

/**
 * Event handling for financial-item INPUT changes.
 * @param {KeyboardEvent} event - The triggering keyboard event.
 */
function _handleInputChange(event) {
  clearTimeout(financialView._inputChangeTimeout);
  const elem = event.target;
  const name = elem.dataset.financialItem;
  const isRate = name.slice(0, 5) === 'rate_';
  const isFee = name.slice(0, 4) === 'fee_';
  let value = convertStringToNumber(elem.value);

  financialView._currentInput = elem;

  if (isRate || isFee) {
    value /= 100;
  }

  if (selectorMatches(elem, ':focus')) {
    financialView._inputChangeTimeout = setTimeout(function () {
      updateFinancial(name, value);
      updateUrlQueryString();
    }, 500);
  } else {
    updateFinancial(name, value);
    updateUrlQueryString();
  }
}

/**
 * Event handling for input clicks.
 * @param {MouseEvent} event - The triggering click event object.
 */
function _handleInputClick(event) {
  const target = event.target;
  if (target.value === '$0') {
    target.value = '';
  }
}

/**
 * Event handling for button choice - "Does your offer include costs?".
 */
// function _handleCostsButtonClick() {
//   const checkedButton = document.querySelector(
//     'input[name="costs-offer-radio"]:checked',
//   );
//   let answer = '';

//   if (checkedButton !== null) {
//     answer = checkedButton.value;

//     // When the button is clicked, bring in school data if 'No'
//     if (getStateValue('costsQuestion') === false) {
//       updateState.byProperty('costsQuestion', answer);
//       // If their offer does not have costs, use the Department of Ed data
//       if (answer === 'n') {
//         updateFinancialsFromSchool();
//       } else {
//         recalculateFinancials();
//       }
//     }

//     updateUrlQueryString();
//   }
// }

export { financialView };
