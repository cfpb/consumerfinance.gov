/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import { createFinancials } from '../dispatchers/update-models.js';
import { getConstantsValue, getExpensesValue, getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { calculateDebt } from '../util/calculate-debt.js';
import { stringToNum } from '../util/number-utils.js';

const financialModel = {

  /* Note: financialModel's values should all be numeric. Other information (degree type,
     housing situation, etc) is stored in the stateModel, schoolModel */
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
      financialModel.recalculate();
    }
  },

  extendValues: data => {
    for ( const key in data ) {
      if ( financialModel.values.hasOwnProperty( key ) ) {
        financialModel.values[key] = data[key];
      }
    }
    financialModel.recalculate();
  },

  recalculate: () => {
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
    let totalWorkStudy = 0;
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
      } else if ( prop.substring( 0, 10 ) === 'workStudy_' ) {
        totalWorkStudy += value;
      }
    }

    // Calculate more totals
    totalContributions = totalGrants + totalScholarships + totalSavings + totalIncome + totalWorkStudy;
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
    financialModel.values.total_workStudy = totalWorkStudy;
    financialModel.values.total_otherResources = totalSavings + totalIncome;
    financialModel.values.total_fedLoans = totalFedLoans;
    financialModel.values.total_schoolLoans = totalInstitutionalLoans;
    financialModel.values.total_borrowing = totalLoans;
    financialModel.values.total_funding = totalContributions + totalLoans;
    financialModel.values.total_gap = financialModel.values.total_costs -
      financialModel.values.total_funding;

    /* Borrowing total
       TODO - Update this once year-by-year DIRECT borrowing is in place */
    financialModel.values.total_borrowingAtGrad = totalLoans * financialModel.values.other_programLength;


    if ( financialModel.values.total_gap < 0 ) {
      financialModel.values.total_gap = 0;
    }

  },

  /**
 * Import financial values from the schoolModel based on stateModel
 */
  updateModelFromSchoolModel: () => {
    const rate = getStateValue( 'programRate' );
    const type = getStateValue( 'programType' );
    const housing = getStateValue( 'programHousing' );

    const rateProperties = {
      inState: 'InS',
      outOfState: 'Oss',
      inDistrict: 'InDis'
    };
    const housingProperties = {
      onCampus: 'OnCampus',
      offCampus: 'OffCampus',
      withFamily: 'OffCampus'
    };
    const otherProperties = {
      onCampus: 'OnCampus',
      offCampus: 'OffCampus',
      withFamily: 'WFamily'
    };
    let tuitionProp = 'tuition';
    let housingProp = 'roomBrd';
    let otherProp = 'other';

    // Set the tuition property name to use
    if ( type === 'graduate' ) {
      tuitionProp += 'Grad';
    } else {
      tuitionProp += 'Under';
    }
    tuitionProp += rateProperties[rate];

    // Get correct tuition based on property name
    financialModel.values.dirCost_tuition = stringToNum( getSchoolValue( tuitionProp ) );

    // Get program length
    financialModel.values.other_programLength = getStateValue( 'programLength' );

    // Get housing costs
    housingProp += housingProperties[housing];
    financialModel.values.dirCost_housing = stringToNum( getSchoolValue( housingProp ) );

    // Get Other costs
    otherProp += otherProperties[housing];
    financialModel.values.indiCost_other = stringToNum( getStateValue( otherProp ) );

    // Get Books costs
    financialModel.values.indiCost_books = stringToNum( getSchoolValue( 'books' ) );

    financialModel.recalculate();

    console.log( financialModel.values );
  },

  calculateDebt: () => {
    const debtObject = calculateDebt( financialModel.values );
    for ( const key in debtObject ) {
      financialModel.values[key] = debtObject[key];
    }
  },

  /**
    * init - Initialize this model
    */
  init: () => {
    // A few properties must be created manually here
    financialModel.createFinancialProperty( 'other_programLength' );

    // These are test values used only for development purposes.

    financialModel.calculateTotals();

  }
};

export {
  financialModel
};
