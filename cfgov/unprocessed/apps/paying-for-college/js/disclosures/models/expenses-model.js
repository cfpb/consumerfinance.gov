const getFinancial = require( '../dispatchers/get-financial-values' );

const expensesModel = {
  values: {},

  expenseKeys: [
    'Retirement',
    'Transportation',
    'Entertainment',
    'Food',
    'Housing',
    'Other',
    'Healthcare',
    'Clothing',
    'Taxes'
  ],

  /**
   * Initializes this model
   * @param {object} expenses - object containing unformatted API values
   */
  init: function( expenses ) {
    this.values.stored = expenses;
  },

  /**
   * Takes model values and performs calculations
   */
  calc: function() {
    const model = this.values;
    const financialValues = getFinancial.values();
    // monthly expenses
    model.totalMonthlyExpenses =
      Math.round( model.housing + model.food +
      model.transportation + model.healthcare +
      model.retirement + model.other + model.entertainment +
      model.clothing + model.taxes );

    model.monthlyLeftover = Math.round( financialValues.monthlySalary -
      model.totalMonthlyExpenses - financialValues.loanMonthly );

    this.values = model;
  },

  /**
   * Turns a salary number into a salary range for use in retrieving
   * the correct BLS expense values.
   * @param {number} salary - Number value of salary
   * @returns {string} salaryRange - String representing salary range
   */
  getSalaryRange: function( salary ) {
    const rangeFinder = {
      'less_than_5000': [ 0, 4999 ],
      '5000_to_9999':   [ 5000, 9999 ],
      '10000_to_14999': [ 10000, 14999 ],
      '15000_to_19999': [ 15000, 19999 ],
      '20000_to_29999': [ 20000, 29999 ],
      '30000_to_39999': [ 30000, 39999 ],
      '40000_to_49999': [ 40000, 49999 ],
      '50000_to_69999': [ 50000, 69999 ],
      '70000_or_more':  [ 70000, Infinity ]
    };

    let arr;
    for ( const key in rangeFinder ) {
      if ( rangeFinder.hasOwnProperty( key ) ) {
        arr = rangeFinder[key];
        if ( salary >= arr[0] && salary <= arr[1] ) {
          return key;
        }
      }
    }

    /* TODO: Update to a string and check that nothing breaks.
       Docs specify `getSalaryRange` returns a string,
       but it returns a boolean here. */
    return false;
  },

  /**
   * Changes the various expenses values based on the region
   * and salary parameters. Uses the 'stored' Object in this
   * model to find correct values.
   * @param {string} region - BLS region code
   * @param {number} salary - Annual salary
   */
  resetCurrentValues: function( region, salary ) {
    for ( let x = 0; x < this.expenseKeys.length; x++ ) {
      const key = this.expenseKeys[x];
      const expense = key.toLowerCase();
      const salaryRange = this.getSalaryRange( salary );
      const val = this.values.stored[key][region][salaryRange];

      this.values[expense] = Math.round( val / 12 );
    }
    this.calc();
  }

};

module.exports = expensesModel;
