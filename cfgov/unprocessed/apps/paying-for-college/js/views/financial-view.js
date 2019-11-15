// This file contains the 'view' of all financial info, including costs, loans, etc

import numberToMoney from 'format-usd';
import { closest } from '../../../../js/modules/util/dom-traverse';
import { updateState } from '../dispatchers/update-state.js';
import { createFinancial, updateFinancial } from '../dispatchers/update-models.js';
import { getState } from '../dispatchers/get-state.js';
import { getFinancialValue } from '../dispatchers/get-model-values.js';
import { stringToNum } from '../util/number-utils.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const financialView = {
  _financialItems: null,
  _inputChangeTimeout: null,
  _calculatingTimeout: null,
  _currentInput: null,
  _actionPlanChoices: null,

  /**
   * Listeners for INPUT fields and radio buttons
   */
  _addInputListeners: function() {
    financialView._financialItems.forEach( elem => {
      const events = {
        keyup: this._handleInputChange,
        focusout: this._handleInputChange
      };
      bindEvent( elem, events );
    } );

    financialView._actionPlanChoices.forEach( elem => {
        const events = {
            click: this._handleActionPlanClick
        }
        bindEvent( elem, events );
    } );

    bindEvent( financialView._actionPlanSeeSteps, { click: this._handleSeeStepsClick } );

  },

  /**
   * Event handling for action-plan choice clicks
   * @param {Object} event - Triggering event
   */
  _handleActionPlanClick: function( event ) {
    const target = event.target;
    financialView._actionPlanChoices.forEach( elem => {
        elem.classList.remove( 'highlighted' );
    } );

    if ( target.matches( '.m-form-field' ) ) {
      console.log( 'form-field' );
        target.classList.add( 'highlighted' );
        target.querySelector( 'input' ).setAttribute( 'checked', true );
    } else {
        console.log( 'not form-field' );
        const div = closest( target, '.m-form-field' );
        div.classList.add( 'highlighted' );
        div.querySelector( 'input' ).setAttribute( 'checked', true );
    }

    financialView._actionPlanSeeSteps.removeAttribute( 'disabled' );
  },

  /**
   * Event handling for financial-item INPUT changes
   * @param {Object} event - Triggering event
   */
  _handleInputChange: function( event ) {
    clearTimeout( financialView._inputChangeTimeout );
    const elem = event.target;
    const name = elem.dataset.financialItem;
    const value = stringToNum( elem.value );

    financialView._currentInput = elem;

    if ( elem.matches( ':focus' ) ) {
      financialView._inputChangeTimeout = setTimeout(
        function() {
          updateFinancial( name, value );
          financialView.updateFinancialItems();
        }, 500 );
    } else {
      updateFinancial( name, value );
      financialView.updateFinancialItems();
    }
  },

  /**
   * Event handling for "see steps" action plan button
   * @param {Object} event - Triggering event
   */
   _handleSeeStepsClick: function( event ) {
    // TODO - This could all be written better.
    const selected = document.querySelector( '.action-plan_choices .highlighted input[checked="true"]');
    document.querySelectorAll( '[data-action-plan]' ).forEach( elem => {
      elem.classList.remove( 'active' );  
    } );
    document.querySelector( '[data-action-plan="' + selected.value + '"]' ).classList.add( 'active' );
    document.querySelector( '.action-plan .action-plan_feeling-gauge' ).classList.add( 'active' );
   },

  updateFinancialItems: function() {
    clearTimeout( this._calculatingTimeout );

    this._financialItems.forEach( elem => {
        
      if ( !elem.matches( ':focus' ) ) {
        const prop = elem.dataset.financialItem;
        const isRate = prop.substr( 0, 5 ) === 'rate_';
        const isFee = prop.substr( 0, 4 ) === 'fee_';
        let val = getFinancialValue( prop );
        if ( isRate || isFee ) {
          val = ( val * 100 ) + '%';
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

  /**
    * initializeFinancialValues - Create financial model values based on the input
    * fields that exist in the financial view
    */
  initializeFinancialValues: function() {
    this._financialItems.forEach( elem => {
      createFinancial( elem.dataset.financialItem );
    } );
  },

  init: function( body ) {
    this._financialItems = document.querySelectorAll( '[data-financial-item]' );
    this._financialInputs = document.querySelectorAll( 'input[data-financial-item]' );
    this._financialSpans = document.querySelectorAll( 'span[data-financial-item]' );
    this._actionPlanChoices = document.querySelectorAll( '.action-plan_choices .m-form-field' );
    this._actionPlanSeeSteps = document.getElementById( 'action-plan_see-your-steps' );
    this._addInputListeners();
    this.initializeFinancialValues();

  }

};

export {
  financialView
};
