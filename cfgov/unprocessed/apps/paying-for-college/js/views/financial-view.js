// This file contains the 'view' of all financial info, including costs, loans, etc

import numberToMoney from 'format-usd';
import { updateState } from '../dispatchers/update-state.js';
import { updateFinancial, createFinancial } from '../dispatchers/update-models.js';
import { getState } from '../dispatchers/get-state.js';
import { getFinancialValue } from '../dispatchers/get-model-values.js';
import { stringToNum } from '../util/number-utils.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const financialView = {
  _sections: null,
  _financialItems: null,
  _inputChangeTimeout: null,
  _calculatingTimeout: null,
  _currentInput: null,

  /**
   * Listeners for INPUT fields
   */
  _addInputListeners: function() {
    financialView._financialItems.forEach( elem => {
      const events = {
        keyup: this._handleInputChange,
        focusout: this._handleInputChange
        };
        bindEvent( elem, events );
    } );
  },


  /**
   * Find financial items on page
   */
  _findFinancialItems: function() {
    this._financialItems = document.querySelectorAll( '[data-financial-item]' );
    this._financialInputs = document.querySelectorAll( 'input[data-financial-item]' );
    this._financialSpans = document.querySelectorAll( 'span[data-financial-item]' );
  },

  /**
   * Event handling for INPUT changes
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

        if ( elem.tagName === "INPUT" ) {
          elem.value = val;          
        } else {
          elem.innerText = val;
        }

              
      }
    } );

    // financialView._financialSpans.forEach( elem => {
    //   elem.innerText = 'Calculating...';
    // } );


    // financialView._calculatingTimeout = setTimeout(
    //   function() {
    //     financialView._financialSpans.forEach( elem => {
    //       const prop = elem.dataset.financialItem;
    //       let val = getFinancialValue( prop );
    //       val = numberToMoney( { amount: val, decimalPlaces: 0 } );
    //       elem.innerText = val;
    //     } );
    //   },
    //   5 );    
  },

  updateSection: function() {
    const activeName = getState( 'activeSection' );
    const query = '.college-costs_tool-section[data-tool-section="' + activeName + '"]';
    const activeSection = document.querySelector( query );

    this._sections.forEach( elem => {
      elem.classList.remove( 'active' );
    } );

    activeSection.classList.add( 'active' );
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
    this._sections = body.querySelectorAll( '.college-costs_tool-section' );
    this._findFinancialItems();
    this._addInputListeners();

    this.updateSection();

    this.initializeFinancialValues();

  }

};

export {
  financialView
};
