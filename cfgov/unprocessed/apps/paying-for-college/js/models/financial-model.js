/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import { createFinancials } from '../dispatchers/update-models.js';
import { getConstantsValue, getSchoolValue } from '../dispatchers/get-model-values.js';
import { calculateDebt } from '../util/calculate-debt.js';

const financialModel = {
  values: {},

  createFinancialProperty: function( name, value ) {
    if ( !financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = 0;
    }
  },

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   */
  setValue: ( name, value ) => {
    if ( financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = value;
      financialModel.calculateTotals();
      financialModel.calculateDebt();
    }
  },

  extendValues: data => {
    for ( const key in data ) {
      if ( financialModel.values.hasOwnProperty( key ) ) {
        financialModel.values[key] = data[key];
      }
    }
    financialModel.calculateTotals();
    financialModel.calculateDebt();
  },

  calculateTotals: () => {
    let totalDirectCosts = 0;
    let totalIndirectCosts = 0;
    let totalGrants = 0;
    let totalScholarships = 0;
    let totalFedLoans = 0;
    let totalLoans = 0;
    let totalSavings = 0;
    let totalIncome = 0;
    let totalContributions = 0;
    let totalInstitutionalLoans = 0;
    const totalPrivateLoans = 0;

    // Calculate totals
    for ( const prop in financialModel.values ) {
      const value = financialModel.values[prop];
      if ( prop.substring( 0, 9 ) === 'indiCost_' ) {
        totalIndirectCosts += value;
      } else if ( prop.substring( 0, 8 ) === 'dirCost_' ) {
        totalDirectCosts += value;
      } else if ( prop.substring( 0, 6 ) === 'grant_' ) {
        totalGrants += value;
      } else if ( prop.substring( 0, 12 ) === 'scholarship_' ) {
        totalScholarships += value;
      } else if ( prop.substring( 0, 8 ) === 'savings_' ) {
        totalSavings += value;
      } else if ( prop.substring( 0, 7 ) === 'income_' ) {
        totalIncome += value;
      } else if ( prop.substring( 0, 8 ) === 'fedLoan_' ) {
        totalFedLoans += value;
      } else if ( prop.substring( 0, 10 ) === 'instiLoan_' ) {
        totalInstitutionalLoans += value;
      }
    }

    // Calculate totals
    totalContributions = totalGrants + totalScholarships + totalSavings + totalIncome;
    totalLoans = totalFedLoans + totalInstitutionalLoans + totalPrivateLoans;

    // Update the model
    financialModel.values.total_directCosts = totalDirectCosts;
    financialModel.values.total_indirectCosts = totalIndirectCosts;
    financialModel.values.total_grants = totalGrants;
    financialModel.values.total_scholarships = totalScholarships;
    financialModel.values.total_savings = totalSavings;
    financialModel.values.total_income = totalIncome;
    financialModel.values.total_costs = totalDirectCosts + totalIndirectCosts;
    financialModel.values.total_grantsScholarships = totalGrants + totalScholarships;
    financialModel.values.total_otherResources = totalSavings + totalIncome;
    financialModel.values.total_fedLoans = totalFedLoans;
    financialModel.values.total_schoolLoans = totalInstitutionalLoans;
    financialModel.values.total_borrowing = totalLoans;
    financialModel.values.total_gap = totalDirectCosts + totalIndirectCosts - totalContributions -
            totalLoans;

    //

  },

  calculateDebt: () => {
    const debtObject = calculateDebt( financialModel.values );
    for ( const key in debtObject ) {
      financialModel.values[key] = debtObject[key];
    }

    console.log( financialModel.values.total_debtMonthly10year );
  },

  /**
    * init - Initialize this model
    */
  init: () => {

    // These are test values used only for development purposes.

    /* financialModel.setValue( 'dirCost_tuition', 10892 );
       financialModel.setValue( 'dirCost_housing', 9384 );
       financialModel.setValue( 'indiCost_books', 1200 );
       financialModel.setValue( 'indiCost_other', 4420 ); */

    /* financialModel.setValue( 'grant_school', 4000 );
       financialModel.setValue( 'grant_pell', 5070 ); */

    // financialModel.setValue( 'fedLoan_directSub', 3500 );

    /* financialModel.setValue( 'fedLoan_directUnsub', 2000 );
       financialModel.setValue( 'savings_family', 827 ); */

    /* // "Step two"
       financialModel.setValue( 'instiLoan_institutional', 7500 );
       financialModel.setValue( 'rate_institutionalLoan', .0858 );
       financialModel.setValue( 'income_job', 2999 ); */


    financialModel.calculateTotals();

  }
};

export {
  financialModel
};
