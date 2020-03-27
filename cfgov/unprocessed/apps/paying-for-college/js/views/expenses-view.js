// This file contains the 'view' of expenses budget after graduation
import numberToMoney from 'format-usd';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { getExpensesValue } from '../dispatchers/get-model-values.js';
import { updateAffordingChart } from '../dispatchers/update-view.js';
import { updateExpense } from '../dispatchers/update-models.js';

const expensesView = {
  _currentInput: null,
  _expensesItems: null,
  _expensesInputs: null,
  _inputChangeTimeout: null,

  /**
   * Event handling for expenses-item INPUT changes
   * @param {Object} event - Triggering event
   */
  _handleInputChange: function( event ) {
    clearTimeout( expensesView._inputChangeTimeout );
    const elem = event.target;
    const name = elem.dataset.expensesItem;
    let value = stringToNum( elem.value );

    expensesView._currentInput = elem;

    if ( elem.matches( ':focus' ) ) {
      expensesView._inputChangeTimeout = setTimeout(
        function() {
          updateExpense( name, value );
          expensesView.updateExpensesItems();
          updateCostOfBorrowingChart();
          updateAffordingChart();
        }, 500 );
    } else {
      updateExpense( name, value );
      expensesView.updateExpensesItems();
      updateCostOfBorrowingChart();
      updateAffordingChart();
    }
  },

   _addInputListeners: function() {
    expensesView._expensesInputs.forEach( elem => {
      const events = {
        keyup: this._handleInputChange,
        focusout: this._handleInputChange
      };
      bindEvent( elem, events );
    } );
  },

  /**
   * Initialize the Expenses View
   */
  init: () => {
    expensesView._expensesItems = document.querySelectorAll( '[data-expenses-item]' );
    expensesView._expensesInputs = document.querySelectorAll( 'input[data-expenses-item]' );
    expensesView._addInputListeners();
  },

  /**
   *  Update the elements of the expenses view based on expensesModel
   */
  _updateExpensesItems: () => {
    expensesView._expensesItems.forEach( elem => {
      if ( !elem.matches( ':focus' ) ) {
        const prop = elem.dataset.expensesItem;
        const isRate = prop.substr( 0, 5 ) === 'rate_';
        const isFee = prop.substr( 0, 4 ) === 'fee_';
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
    updateAffordingChart();
   }

};

export {
  expensesView
}
