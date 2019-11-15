/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import { createFinancials } from '../dispatchers/update-models.js';

const financialModel = {
  values: {},

  createFinancialProperty: name => {
    if ( !financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = 0;
    }
  },

  setValue: ( name, value ) => {
    if ( financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = value;
      financialModel.calculateTotals();
    }
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
    let totalSchoolLoans = 0;
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
      } else if ( prop.substring( 0, 11 ) === 'schoolLoan_' ) {
        totalSchoolLoans += value;
      }
    }

    // Update the model
    financialModel.values.total_directCosts = totalDirectCosts;
    financialModel.values.total_indirectCosts = totalIndirectCosts;
    financialModel.values.total_grants = totalGrants;
    financialModel.values.total_scholarships = totalScholarships;
    financialModel.values.total_savings = totalSavings;
    financialModel.values.total_income = totalIncome;

    totalContributions = totalGrants + totalScholarships + totalSavings + totalIncome;

    financialModel.values.total_costs = totalDirectCosts + totalIndirectCosts;
    financialModel.values.total_grantsScholarships = totalGrants + totalScholarships;

    financialModel.values.total_fedLoans = totalFedLoans;
    financialModel.values.total_schoolLoans = totalSchoolLoans;

    totalLoans = totalFedLoans + totalSchoolLoans + totalPrivateLoans;

    financialModel.values.total_gap = totalDirectCosts + totalIndirectCosts - totalContributions -
            totalLoans;
  },

  /**
      * init - Initialize this model
      */
  init: () => {
    // These are test values used only for development purposes.

    financialModel.setValue( 'dirCost_tuition', 45520 );
    financialModel.setValue( 'dirCost_housing', 3500 );
    financialModel.setValue( 'indiCost_books', 1100 );
    financialModel.setValue( 'indiCost_other', 150 );
    financialModel.setValue( 'grant_state', 1200 );
    financialModel.setValue( 'grant_pell', 2000 );
    financialModel.setValue( 'scholarship_state', 1250 );
    financialModel.setValue( 'scholarship_school', 2550 );
    financialModel.setValue( 'fedLoan_directSub', 5000 );
    financialModel.setValue( 'fee_directSub', 0.0108 );
    financialModel.setValue( 'rate_directSub', 0.0678 );
    financialModel.setValue( 'fedLoan_directUnsub', 7000 );
    financialModel.setValue( 'fee_directUnsub', 0.0219 );
    financialModel.setValue( 'rate_directUnsub', 0.0987 );

    financialModel.calculateTotals();

  }
};

export {
  financialModel
};
