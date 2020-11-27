// This file contains the 'view' of all financial info, including costs, loans, etc

import numberToMoney from 'format-usd';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { recalculateFinancials, updateFinancial, updateFinancialsFromSchool } from '../dispatchers/update-models.js';
import { decimalToPercentString, stringToNum } from '../util/number-utils.js';
import { getFinancialValue, getStateValue } from '../dispatchers/get-model-values.js';
import { selectorMatches } from '../util/other-utils';
import { updateState } from '../dispatchers/update-state.js';

const financialView = {
  _financialItems: [],
  _inputChangeTimeout: null,
  _calculatingTimeout: null,
  _currentInput: null,
  _costsOfferButtons: null,
  _gradProgramContent: null,
  _undergradProgramContent: null,

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
  },

  /**
   * Listeners for INPUT fields and radio buttons
   */
  _addInputListeners: function() {
    financialView._financialInputs.forEach( elem => {
      const events = {
        keyup: this._handleInputChange,
        focusout: this._handleInputChange,
        click: this._handleInputClick
      };
      bindEvent( elem, events );
    } );

  },

  /**
   * Event handling for button choice - "Does your offer include costs?"
   * @param {object} event - Triggering event
   */
  _handleCostsButtonClick: function( event ) {
    const target = event.target;
    const answer = target.dataset.costs_offerAnswer;
    const offerContent = document.querySelector( '[data-offer-costs-info="' + answer + '"]' );
    const costsContent = document.getElementById( 'costs_inputs-section' );

    // When the button is clicked, bring in school data if 'No'
    if ( getStateValue( 'costsQuestion' ) === false ) {
      updateState.byProperty( 'costsQuestion', answer );
      // If their offer does not have costs, use the Department of Ed data
      if ( answer === 'n' ) {
        updateFinancialsFromSchool();
      } else {
        recalculateFinancials();
      }
    }
  },

  /**
   * Event handling for financial-item INPUT changes
   * @param {object} event - Triggering event
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

    if ( selectorMatches( elem, ':focus' ) ) {
      financialView._inputChangeTimeout = setTimeout(
        function() {
          updateFinancial( name, value );
        }, 500 );
    } else {
      updateFinancial( name, value );
    }
  },

  /**
   * Event handling for input clicks
   * @param {object} event - the triggering event
   */
  _handleInputClick: function( event ) {
    const target = event.target;
    if ( target.value === '$0' ) {
      target.value = '';
    }
  },

  /**
   * Event handling for "see steps" action plan button
   * @param {object} event - Triggering event
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
      if ( !selectorMatches( elem, ':focus' ) ) {
        const prop = elem.dataset.financialItem;
        const isRate = prop.substr( 0, 5 ) === 'rate_';
        const isFee = prop.substr( 0, 4 ) === 'fee_';
        const isNumber = elem.dataset.isNumber === 'true';
        let val = getFinancialValue( prop );

        // Prevent improper property values from presenting on the page
        if ( val === false || val === null || isNaN( val ) ) val = 0;
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
  },

  /* init - Initialize the financialView object */
  init: function( body ) {
    this._financialItems = document.querySelectorAll( '[data-financial-item]' );
    this._financialInputs = document.querySelectorAll( 'input[data-financial-item]' );
    this._financialSpans = document.querySelectorAll( 'span[data-financial-item]' );
    this._costsOfferButtons = document.querySelectorAll( '.costs_button-section button' );
    this._addInputListeners();
    this._addButtonListeners();
  }

};

export {
  financialView
};
