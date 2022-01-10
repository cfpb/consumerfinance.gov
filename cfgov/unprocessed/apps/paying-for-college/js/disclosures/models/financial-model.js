// TODO: Remove jquery.
const $ = require( 'jquery' );

const recalculate = require( 'student-debt-calc' );
const getViewValues = require( '../dispatchers/get-view-values' );

const financialModel = {
  values: {},

  /**
   * Initiates the model
   * @param {object} apiData - Data received from the schoolData API
   */
  init: function( apiData ) {
    this.values = getViewValues.init( apiData );
    // we don't use directPlus in the UI
    this.values.directPlus = 0;
    this.calc();
  },

  /**
   * Checks if the school offers Perkins loans, zeros value if not
   */
  checkPerkins: function() {
    if ( this.values.offersPerkins === false ) {
      this.values.perkins = 0;
    }
  },

  /**
   * Adds various scholarships to form the 'scholarships' property
   */
  sumScholarships: function() {
    const model = financialModel.values;
    // model.scholarships as a sum of UI inputs
    model.scholarships =
      model.schoolGrants +
      model.stateGrants +
      model.otherScholarships;
  },

  /**
   * Performs calculations using student-debt-calc package
   */
  calc: function() {
    this.sumScholarships();
    this.checkPerkins();
    this.values = recalculate( this.values );
    this.sumTotals();
    this.roundValues();
  },

  /**
   * Sums totals for various view elements
   */
  sumTotals: function() {
    const model = financialModel.values;

    model.privateLoanTotal = 0;

    for ( let x = 0; x < model.privateLoanMulti.length; x++ ) {
      model.privateLoanTotal += model.privateLoanMulti[x].amount;
    }

    // Modify values using tuition repayment plan values
    model.tuitionRepayYearly = model.tuitionRepay / Math.max( model.programLength, 1 );
    model.summaryLoanTotal = model.borrowingTotal + model.tuitionRepayYearly;
    model.gap -= model.tuitionRepayYearly;
    model.totalDebt += model.tuitionRepayDebt;
    model.loanLifetime += model.tuitionRepayMonthly * model.tuitionRepayTerm;
    model.loanMonthly += model.tuitionRepayMonthly;
    model.borrowingTotal += model.tuitionRepayYearly;
    model.overborrowing = this.recalcOverborrowing();

    // Calculate totals
    model.costAfterGrants = model.costOfAttendance - model.grantsTotal;
    model.totalProgramDebt = ( model.borrowingTotal - model.tuitionRepayYearly ) *
      Math.max( model.programLength, 1 );
    model.totalProgramDebt += model.tuitionRepay;

  },

  /**
   * Rounds values for which we do not want to display decimals
   */
  roundValues: function() {
    const model = financialModel.values;
    const roundedKeys = [
      'totalDebt',
      'loanMonthly',
      'loanLifetime',
      'tuitionRepayYearly'
    ];
    for ( let x = 0; x < roundedKeys.length; x++ ) {
      const key = roundedKeys[x];
      model[key] = Math.round( model[key] );
    }
  },

  /**
   * Updates the financial model with values from school and program data.
   * @param { object } schoolValues - contains school and program data values.
   */
  updateModelWithProgram: function( schoolValues ) {
    schoolValues.undergrad = true;
    if ( schoolValues.level.indexOf( 'Graduate' ) !== -1 || schoolValues.level === '4' ) {
      schoolValues.undergrad = false;
    }
    $.extend( this.values, schoolValues );
  },

  /**
   * recalculates overborrowing so that it includes tuition payment plans
   * @returns {number} - Overborrowing value
   */
  recalcOverborrowing: function() {
    const model = this.values;
    let overBorrow = 0;
    if ( model.costOfAttendance <
         model.grantsSavingsTotal + model.borrowingTotal ) {
      overBorrow = model.borrowingTotal +
                   model.grantsSavingsTotal -
                   model.costOfAttendance;
      if ( overBorrow > 0 && model.borrowingTotal > 0 ) {
        overBorrow = Math.min( overBorrow, model.borrowingTotal );
      } else {
        overBorrow = 0;
      }
    }
    return overBorrow;
  }

};

module.exports = financialModel;
