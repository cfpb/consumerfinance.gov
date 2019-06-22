// TODO: Remove jquery.
const $ = require( 'jquery' );

const financialModel = require( '../models/financial-model' );
const expensesModel = require( '../models/expenses-model' );

const publishUpdate = {

  /**
   * Function which updates financial model with new value
   * @param {string} prop - financial model property name
   * @param {number|string} val - new value
   */
  financialData: function( prop, val ) {
    financialModel.values[prop] = val;
    financialModel.calc( financialModel.values );
    expensesModel.calc();
  },

  /**
   * Function which updates financial model by extending it with an object
   * @param {object} object - an object of financial model values
   */
  extendFinancialData: function( object ) {
    $.extend( financialModel.values, object );
    financialModel.calc( financialModel.values );
    expensesModel.calc();
  },

  /**
   * Function which updates privateLoanMulti array in financial model with new
   * value
   * @param {number} index - The index of the private loan being updated
   * @param {string} prop - private loan object property name
   * @param {number|string} val - new value
   */
  updatePrivateLoan: function( index, prop, val ) {
    financialModel.values.privateLoanMulti[index][prop] = val;
    financialModel.calc( financialModel.values );
    expensesModel.calc();
  },

  /**
   * Function which removes a private loan from the privateLoanMulti array
   * @param {number} index - The index of the private loan being removed
   */
  dropPrivateLoan: function( index ) {
    financialModel.values.privateLoanMulti.splice( index, 1 );
    financialModel.calc( financialModel.values );
    expensesModel.calc();
  },

  /**
   * Function which adds a private loan object to the privateLoanMulti array in
   * financial model
   */
  addPrivateLoan: function() {
    const newLoanObject = { amount: 0,
      fees: 0,
      rate: 0.079,
      deferPeriod: 0
    };
    financialModel.values.privateLoanMulti.push( newLoanObject );
    financialModel.calc( financialModel.values );
    expensesModel.calc();
  },

  /**
   * Function which updates expenses model with new value
   * @param {string} prop - expenses model property name
   * @param {number|string} val - new value
   */
  expensesData: function( prop, val ) {
    expensesModel.values[prop] = val;
    expensesModel.calc();
  },

  /**
   * Function which updates expenses model with a new
   * region.
   * @param {string} region - region code
   */
  updateRegion: function( region ) {
    const salary = financialModel.values.medianSalary;
    expensesModel.resetCurrentValues( region, salary );
    expensesModel.calc();
  }

};

module.exports = publishUpdate;
