// This file contains the 'view' of expenses budget after graduation
import { updateExpense, updateRegion } from '../dispatchers/update-models.js';
import { getExpensesValue } from '../dispatchers/get-model-values.js';
import numberToMoney from 'format-usd';
import { selectorMatches } from '../util/other-utils';
import { stringToNum } from '../util/number-utils.js';
import { updateAffordingChart, updateCostOfBorrowingChart, updateUrlQueryString } from '../dispatchers/update-view.js';

const expensesView = {
  _currentInput: null,
  _expensesItems: [],
  _expensesInputs: [],
  _inputChangeTimeout: null,
  _regionSelect: null,

  /**
   * Initialize the Expenses View
   */
  init: () => {
    expensesView._expensesItems = document.querySelectorAll( '[data-expenses-item]' );
    expensesView._expensesInputs = document.querySelectorAll( 'input[data-expenses-item]' );
    expensesView._regionSelect = document.querySelector( '#expenses__region' );

    _addInputListeners();
  },

  /**
   *  Update the elements of the expenses view based on expensesModel
   */
  _updateExpensesItems: () => {
    expensesView._expensesItems.forEach( elem => {
      if ( !selectorMatches( elem, ':focus' ) ) {
        const prop = elem.dataset.expensesItem;
        let val = getExpensesValue( prop );
        val = numberToMoney( { amount: val, decimalPlaces: 0 } );

        if ( elem.tagName === 'INPUT' ) {
          elem.value = val;
        } else {
          elem.innerText = val;
        }
      }
    } );
  },

  /**
   * Update the Expenses View
   */
  updateExpensesView: () => {
    expensesView._updateExpensesItems();
    updateCostOfBorrowingChart();
    updateAffordingChart();
    updateUrlQueryString();
  }
};

/**
 * Add event listeners to inputs.
 */
function _addInputListeners() {
  expensesView._expensesInputs.forEach( elem => {
    elem.addEventListener( 'keyup', _handleInputChange );
    elem.addEventListener( 'focusout', _handleInputChange );
  } );

  expensesView._regionSelect.addEventListener( 'change', _handleRegionChange );
}

/**
 * Event handling for expenses-item INPUT changes.
 * @param {KeyboardEvent} event - Triggering event.
 */
function _handleInputChange( event ) {
  clearTimeout( expensesView._inputChangeTimeout );
  const elem = event.target;
  const name = elem.dataset.expensesItem;
  const value = stringToNum( elem.value );

  expensesView._currentInput = elem;

  if ( selectorMatches( elem, ':focus' ) ) {
    expensesView._inputChangeTimeout = setTimeout(
      function() {
        updateExpense( name, value );
      }, 500 );
  } else {
    updateExpense( name, value );
  }

  updateUrlQueryString();
}

/**
 * Handle change of region selection.
 */
function _handleRegionChange() {
  updateRegion( expensesView._regionSelect.value );
  updateAffordingChart();
  updateUrlQueryString();
}

export {
  expensesView
};
