// This file contains the 'view' of all financial info, including costs, loans, etc

import { updateAffordingChart, updateCostOfBorrowingChart, updateExpensesView, updateMakePlanChart, updateMaxDebtChart } from '../dispatchers/update-view.js';
import numberToMoney from 'format-usd';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { createFinancial, recalculateFinancials, updateFinancial, updateFinancialsFromSchool } from '../dispatchers/update-models.js';
import { decimalToPercentString, stringToNum } from '../util/number-utils.js';
import { getFinancialValue, getStateValue } from '../dispatchers/get-model-values.js';
import { updateState } from '../dispatchers/update-state.js';

const financialView = {
  _financialItems: [],
  _inputChangeTimeout: null,
  _calculatingTimeout: null,
  _currentInput: null,
  _costsOfferButtons: null,
  _actionPlanChoices: null,
  _gradProgramContent: null,
  _undergradProgramContent: null,
  _otherBorrowingButtons: null,

  /**
   * Listeners for INPUT fields and radio buttons
   */
  _addButtonListeners: function() {
    financialView._costsOfferButtons.forEach( elem => {
      const events = {
        click: this._handleCostsButtonClick
      };
      bindEvent( elem, events );
    } );

    financialView._otherBorrowingButtons.forEach( elem => {
      const events = {
        click: this._handleOtherLoanButtonClick
      };
      bindEvent( elem, events );
    } );
  },

  /**
   * Listeners for INPUT fields and radio buttons
   */
  _addInputListeners: function() {
    financialView._financialInputs.forEach( elem => {
      const events = {
        keyup: this._handleInputChange,
        focusout: this._handleInputChange
      };
      bindEvent( elem, events );
    } );

    financialView._actionPlanChoices.forEach( elem => {
      const events = {
        click: this._handleActionPlanClick
      };
      bindEvent( elem, events );
    } );

  },

  /**
   * Event handling for action-plan choice clicks
   * @param {Object} event - Triggering event
   */
  _handleActionPlanClick: function( event ) {
    /* const target = event.target;
       financialView._actionPlanChoices.forEach( elem => {
         elem.classList.remove( 'highlighted' );
       } ); */

    /* if ( target.matches( '.m-form-field' ) ) {
         target.classList.add( 'highlighted' );
         target.querySelector( 'input' ).setAttribute( 'checked', true );
       } else {
         const div = closest( target, '.m-form-field' );
         div.classList.add( 'highlighted' );
         div.querySelector( 'input' ).setAttribute( 'checked', true );
       } */

    // financialView._actionPlanSeeSteps.removeAttribute( 'disabled' );
  },

  /**
   * Event handling for button choice - "Does your offer include costs?"
   * @param {Object} event - Triggering event
   */
  _handleCostsButtonClick: function( event ) {
    const target = event.target;
    const answer = target.dataset.costs_offerAnswer;
    const offerContent = document.querySelector( '[data-offer-costs-info="' + answer + '"]' );
    const costsContent = document.getElementById( 'costs_inputs-section' );

    // When button is first clicked, bring in school data if 'No'
    if ( getStateValue( 'costsButtonClicked' ) === false ) {
      updateState.byProperty( 'costsButtonClicked', answer );
      // If their offer does not have costs, use the Department of Ed data
      if ( answer === 'no' ) {
        updateFinancialsFromSchool();
      } else {
        recalculateFinancials();
      }
    }

    // Show the appropriate content
    document.querySelectorAll( '[data-offer-costs-info]' ).forEach( elem => {
      elem.classList.remove( 'active' );
    } );
    document.querySelectorAll( '[data-costs_offer-answer]' ).forEach( elem => {
      elem.classList.add( 'a-btn__disabled' );
    } );
    target.classList.remove( 'a-btn__disabled' );
    offerContent.classList.add( 'active' );
    costsContent.classList.add( 'active' );
  },

  /**
   * Event handling for private and PLUS loans
   * @param {Object} event - Triggering event
   */
  _handleOtherLoanButtonClick: function( event ) {
    const target = event.target;
    const value = target.dataset.borrowButton;
    console.log( value );
    if ( value === 'privateLoan' ) {
      updateState.byProperty( 'showPrivateLoans', 'yes' );
    } else if ( value === 'gradPlus' ) {
      updateState.byProperty( 'showPlusLoan', 'gradPlus' );
    } else if ( value === 'parentPlus' ) {
      updateState.byProperty( 'showPlusLoan', 'parentPlus' );
    }

  },

  /**
   * Event handling for financial-item INPUT changes
   * @param {Object} event - Triggering event
   */
  _handleInputChange: function( event ) {
    clearTimeout( financialView._inputChangeTimeout );
    const elem = event.target;
    const name = elem.dataset.financialItem;
    const isRate = name.substr( 0, 5 ) === 'rate_';
    const isFee = name.substr( 0, 4 ) === 'fee_';
    let value = stringToNum( elem.value );

    financialView._currentInput = elem;

    if ( isRate || isFee ) {
      value /= 100;
    }

    if ( elem.matches( ':focus' ) ) {
      financialView._inputChangeTimeout = setTimeout(
        function() {
          updateFinancial( name, value );
          financialView.updateFinancialItems();
          updateCostOfBorrowingChart();
          updateMakePlanChart();
          updateMaxDebtChart();
          updateAffordingChart();
        }, 500 );
    } else {
      updateFinancial( name, value );
      financialView.updateFinancialItems();
      updateCostOfBorrowingChart();
      updateMakePlanChart();
      updateMaxDebtChart();
      updateAffordingChart();
      updateExpensesView();
    }
  },

  /**
   * Event handling for "see steps" action plan button
   * @param {Object} event - Triggering event
   */
  _handleSeeStepsClick: function( event ) {
    // TODO - This could all be written better.
    const selected = document.querySelector( '.action-plan_choices .highlighted input[checked="true"]' );
    document.querySelectorAll( '[data-action-plan]' ).forEach( elem => {
      elem.classList.remove( 'active' );
    } );
    document.querySelector( '[data-action-plan="' + selected.value + '"]' ).classList.add( 'active' );
    document.querySelector( '.action-plan .action-plan_feeling-gauge' ).classList.add( 'active' );
  },

  updateFinancialItems: function() {
    this._financialItems.forEach( elem => {

      if ( !elem.matches( ':focus' ) ) {
        const prop = elem.dataset.financialItem;
        const isRate = prop.substr( 0, 5 ) === 'rate_';
        const isFee = prop.substr( 0, 4 ) === 'fee_';
        const isNumber = elem.dataset.isNumber === 'true';
        let val = getFinancialValue( prop );
        if ( isFee ) {
          val = decimalToPercentString( val, 3 );
        } else if ( isRate ) {
          val = decimalToPercentString( val, 2 );
        } else if ( isNumber ) {
          val = Math.round( val * 100 ) / 100;
        } else {
          val = numberToMoney( { amount: val, decimalPlaces: 0 } );
        }

        if ( elem.tagName === 'INPUT' ) {
          elem.value = val;
        } else {
          elem.innerText = val;
        }


      }
    } );

    /* financialView._financialSpans.forEach( elem => {
       elem.innerText = 'Calculating...';
       } ); */


    /* financialView._calculatingTimeout = setTimeout(
       function() {
       financialView._financialSpans.forEach( elem => {
       const prop = elem.dataset.financialItem;
       let val = getFinancialValue( prop );
       val = numberToMoney( { amount: val, decimalPlaces: 0 } );
       elem.innerText = val;
       } );
       },
       5 ); */
  },

  /* init - Initialize the financialView object */
  init: function( body ) {
    this._financialItems = document.querySelectorAll( '[data-financial-item]' );
    this._financialInputs = document.querySelectorAll( 'input[data-financial-item]' );
    this._financialSpans = document.querySelectorAll( 'span[data-financial-item]' );
    this._costsOfferButtons = document.querySelectorAll( '.costs_button-section button' );
    this._actionPlanChoices = document.querySelectorAll( '.action-plan_choices .m-form-field' );
    this._otherBorrowingButtons = document.querySelectorAll( '.other-borrowing-btns button' );
    this._addInputListeners();
    this._addButtonListeners();
  }

};

export {
  financialView
};
