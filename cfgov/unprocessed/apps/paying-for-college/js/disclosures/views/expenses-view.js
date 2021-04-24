// TODO: Remove jquery.
const $ = require( 'jquery' );

const Analytics = require( '../utils/Analytics' );
const getDataLayerOptions = Analytics.getDataLayerOptions;
const getExpenses = require( '../dispatchers/get-expenses-values' );
const publish = require( '../dispatchers/publish-update' );
const formatUSD = require( 'format-usd' );
const stringToNum = require( '../utils/handle-string-input' );

const expensesView = {
  $elements: $( '[data-expenses]' ),
  $reviewAndEvaluate: $( '[data-section="review"], [data-section="evaluate"]' ),
  currentInput: '',

  init: function() {
    this.expenseInputChangeListener();
    this.keyupListener();
    this.regionSelectListener();
    this.feedbackBtnListener();
  },

  /**
   * Helper function that updates the value or text of an element
   * @param {object} $ele - jQuery object of the element to update
   * @param {number|string} value - The new value
   * @param {Boolean} currency - True if value is to be formatted as currency
   */
  updateElement: function( $ele, value, currency ) {
    const originalValue = $ele.val() || $ele.text();
    const isSummaryLineItem = $ele.attr( 'data-line-item' ) === 'true';
    if ( currency === true ) {
      value = formatUSD( { amount: value, decimalPlaces: 0 } );
    }
    if ( $ele.prop( 'tagName' ) === 'INPUT' ) {
      $ele.val( value );
    } else if ( isSummaryLineItem && originalValue !== value ) {
      setTimeout( function() {
        expensesView.removeRecalculationMessage( $ele, value );
      }, 2000 );
      expensesView.addSummaryRecalculationMessage( $ele );
    } else {
      $ele.text( value );
    }
  },

  /**
   * Helper function that updates expenses elements
   * @param {object} values - expenses model values
   */
  updateExpenses: function( values ) {
    const expensesHigherThanSalary = $( '.aid-form_higher-expenses' );
    this.$elements.each( function() {
      const $ele = $( this );
      const name = $ele.attr( 'data-expenses' );
      const currency = true;
      if ( expensesView.currentInput !== $ele.attr( 'id' ) ) {
        expensesView.updateElement( $ele, values[name], currency );
      }
      if ( values.monthlyLeftover > 0 ) {
        expensesHigherThanSalary.hide();
        Analytics.sendEvent( getDataLayerOptions( 'Total left at the end of the month',
          'Zero left to pay' ) );
      } else { expensesHigherThanSalary.show(); }
    } );
  },

  /**
   * Function that updates the view with new values
   * @param {object} values - expense model values
   */
  updateView: function( values ) {
    // handle non-private-loan fields
    this.updateExpenses( values );
  },

  /**
   * Helper function for handling user entries in expenses model INPUT fields
   * @param {string} id - The id attribute of the element to be handled
   */
  inputHandler: function( id ) {
    const $ele = $( '#' + id );
    const value = stringToNum( $ele.val() );
    const key = $ele.attr( 'data-expenses' );
    publish.expensesData( key, value );
    expensesView.updateView( getExpenses.values() );
  },

  /**
   * Helper function to indicate that a offer summary line item has
   * successfully recalculated
   * @param {object} element - jQuery object of the recalculated summary element
   */
  addSummaryRecalculationMessage: function( element ) {
    element.siblings().hide();
    element.text( 'Updating...' );
  },

  /**
   * Helper function to remove all indicators that data has recalculated
   * @param {object} element - jQuery object of the recalculated summary element
   * @param {string} value - the recalculated value of the element
   */
  removeRecalculationMessage: function( element, value ) {
    element.text( value );
    element.siblings().show();
  },

  /**
   * Listener function for keyup in expenses INPUT fields
   */
  keyupListener: function() {
    this.$reviewAndEvaluate.on( 'keyup focusout', '[data-expenses]', function() {
      clearTimeout( expensesView.keyupDelay );
      expensesView.currentInput = $( this ).attr( 'id' );
      if ( $( this ).is( ':focus' ) ) {
        expensesView.keyupDelay = setTimeout( function() {
          expensesView.inputHandler( expensesView.currentInput );
          expensesView.updateView( getExpenses.values() );
        }, 500 );
      } else {
        expensesView.inputHandler( expensesView.currentInput );
        expensesView.currentInput = 'none';
        expensesView.updateView( getExpenses.values() );
      }
    } );
  },

  /**
   * Listener function for change events on expenses INPUT fields
   */
  expenseInputChangeListener: function() {
    $( '[data-expenses]' ).one( 'change', function() {
      const expenses = $( this ).data( 'expenses' );
      if ( expenses ) {
        Analytics.sendEvent( getDataLayerOptions( 'Value Edited', expenses ) );
      }
    } );
  },

  /**
   * Listener for the BLS region SELECT
   */
  regionSelectListener: function() {
    $( '#bls-region-select' ).change( function() {
      const region = $( this ).val();
      publish.updateRegion( region );
      expensesView.updateView( getExpenses.values() );
      Analytics.sendEvent( getDataLayerOptions( 'Region Changed', region ) );
    } );
  },

  /**
   * Listener for the Feedback BUTTON
   */
  feedbackBtnListener: function() {
    $( '[data-qa=feedback-btn]' ).click( function() {
      Analytics.sendEvent( getDataLayerOptions(
        'Was this page helpful?', 'Tell us how' ) );
    } );
  }


};

module.exports = expensesView;
