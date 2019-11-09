/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import { createFinancials } from '../dispatchers/update-models.js';

const financialModel = {
    values: {},

    createFinancialProperty: ( name ) => {
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

        // Calculate totals
        for ( let prop in financialModel.values ) {
            const value = financialModel.values[prop];
            if ( prop.substring( 0, 9 ) === 'indiCost_' ) {
                totalIndirectCosts += value;
            } else if ( prop.substring( 0, 8 ) === 'dirCost_' ) {
                totalDirectCosts += value;
            } else if ( prop.substring( 0, 6 ) === 'grant_' ) {
                totalGrants += value;
            } else if ( prop.substring( 0, 12 ) === 'scholarship_' ) {
                totalScholarships += value;
            } else if ( prop.substring( 0, 8 ) === 'fedLoan_' ) {
                totalFedLoans += value;
            }
        }

        // Update the model
        financialModel.values.total_directCosts = totalDirectCosts;
        financialModel.values.total_indirectCosts = totalIndirectCosts;
        financialModel.values.total_grants = totalGrants;
        financialModel.values.total_scholarships = totalScholarships;

        financialModel.values.total_costs = totalDirectCosts + totalIndirectCosts;
        financialModel.values.total_grantsScholarships = totalGrants + totalScholarships;
        financialModel.values.total_fedLoans = totalFedLoans;
    },

    /**
      * init - Initialize this model
      */
    init: () => {

        // These are test values used only for development purposes.

        financialModel.setValue( 'dirCost_tuition', 1500 );
        financialModel.setValue( 'dirCost_housing', 233 );
        financialModel.setValue( 'indiCost_books', 999 );
        financialModel.setValue( 'indiCost_other', 123 );
        financialModel.setValue( 'grant_state', 3211 );
        financialModel.setValue( 'grant_pell', 123 );
        financialModel.setValue( 'scholarship_state', 1555 );
        financialModel.setValue( 'scholarship_school', 1919 );
        financialModel.setValue( 'fedLoan_directSub', 12345 );
        financialModel.setValue( 'fee_directSub', .0108 );
        financialModel.setValue( 'rate_directSub', .0678 );
        financialModel.setValue( 'fedLoan_directUnsub', 13333 );
        financialModel.setValue( 'fee_directUnsub', .0219 );
        financialModel.setValue( 'rate_directUnsub', .0987 );
        
        financialModel.calculateTotals();


    }
};

export {
  financialModel
};
