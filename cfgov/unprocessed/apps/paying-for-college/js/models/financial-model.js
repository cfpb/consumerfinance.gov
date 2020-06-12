/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import { getConstantsValue, getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { initializeFinancialValues, recalculateExpenses } from '../dispatchers/update-models.js';
import { updateUrlQueryString } from '../dispatchers/update-view.js';
import { updateState } from '../dispatchers/update-state.js';
import { debtCalculator } from '../util/debt-calculator.js';
import { enforceRange, stringToNum } from '../util/number-utils.js';

// Please excuse some uses of underscore for code/HTML property clarity!
/* eslint camelcase: ["error", {properties: "never"}] */

const financialModel = {

  /* Note: financialModel's values should all be numeric. Other information (degree type,
     housing situation, etc) is stored in the stateModel, schoolModel */
  values: {},

  createFinancialProperty: function( name ) {
    if ( !financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = 0;
    }
  },

  /**
   * extendValues - Update multiple values at once using an Object
   * @param {Object} data - an Object of new financial values
   */
  extendValues: data => {
    for ( const key in data ) {
      if ( financialModel.values.hasOwnProperty( key ) ) {
        financialModel.values[key] = stringToNum( data[key] );
      }
    }
    financialModel.recalculate();
  },

  /**
   * recalculate - Public method that runs private recalculation
   * subfunctions
   */
  recalculate: () => {
    financialModel._calculateTotals();
    debtCalculator();
    recalculateExpenses();

    financialModel._updateStateWithFinancials();
  },

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   */
  setValue: ( name, value ) => {
    if ( financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = stringToNum( value );
      financialModel.recalculate();
      updateUrlQueryString();
    }
  },

  /**
   * _calculateTotals - Recalculate all relevant totals
   */
  _calculateTotals: () => {
    const vals = financialModel.values;
    const totals = {
      dirCost: 'total_directCosts',
      indiCost: 'total_indirectCosts',
      grant: 'total_grants',
      scholarship: 'total_scholarships',
      savings: 'total_savings',
      fellowAssist: 'total_fellowAssist',
      income: 'total_income',
      fedLoan: 'total_fedLoans',
      publicLoan: 'total_publicLoans',
      workStudy: 'total_workStudy',
      plusLoan: 'total_plusLoans',
      privLoan: 'total_privateLoans'
    };

    // Reset all totals to 0
    for ( const key in totals ) {
      vals[totals[key]] = 0;
    }

    // Enforce the limits
    const errors = financialModel._enforceLimits();

    // Calculate totals
    for ( const prop in vals ) {
      const prefix = prop.split( '_' )[0];
      if ( totals.hasOwnProperty( prefix ) ) {
        vals[totals[prefix]] += vals[prop];
      }
    }

    // Calculate more totals
    vals.total_borrowing = vals.total_fedLoans + vals.total_publicLoans + vals.total_privateLoans +
        vals.total_plusLoans;
    vals.total_contributions = vals.total_grants + vals.total_scholarships + vals.total_savings +
        vals.total_workStudy;
    vals.total_costs = vals.total_directCosts + vals.total_indirectCosts + vals.otherCost_additional;
    vals.total_grantsScholarships = vals.total_grants + vals.total_scholarships;
    vals.total_otherResources = vals.total_savings + vals.total_income;
    vals.total_funding = vals.total_contributions + vals.total_borrowing;
    vals.total_gap = vals.total_costs - vals.total_funding;
    vals.total_excessFunding = vals.total_funding - vals.total_costs;

    /* Borrowing total
       TODO - Update this once year-by-year DIRECT borrowing is in place */
    vals.total_borrowingAtGrad = vals.total_borrowing * vals.other_programLength;


    if ( vals.total_gap < 0 ) {
      vals.total_gap = 0;
    }

    console.log( financialModel.values );

  },

  /* _enforceLimits - Check and enforce various limits on federal loans
     and grants
     @returns {Object} An object of errors found during enforcement */
  _enforceLimits: () => {
    // Determine unsubsidized cap based on status
    let unsubCapKey = 'unsubsidizedCapYearOne';
    if ( getStateValue( 'programType' ) === 'graduate' ) {
      unsubCapKey = 'unsubsidizedCapGrad';
    } else if ( getStateValue( 'programDependency' ) === 'independent' ) {
      unsubCapKey = 'unsubsidizedCapIndepYearOne';
    }

    const limits = {
      grant_pell: [ 0, getConstantsValue( 'pellCap' ) ],
      grant_mta: [ 0, getConstantsValue( 'militaryAssistanceCap' ) ],
      fedLoan_directSub: [ 0, getConstantsValue( 'subsidizedCapYearOne' ) ],
      fedLoan_directUnsub: [ 0, getConstantsValue( unsubCapKey ) ]
    };
    const errors = {};

    for ( const key in limits ) {
      const result = enforceRange( financialModel.values[key], limits[key][0], limits[key][1] );
      financialModel.values[key] = result.value;
      if ( result.error !== false ) {
        errors[key] = result.error;
      }
    }

    return errors;

  },

  /**
   * _updateStateWithFinancials: Based on financial situation, update the application state
   */
  _updateStateWithFinancials: () => {
    updateState.byProperty( 'uncoveredCosts',
      ( financialModel.values.total_gap > 0 ).toString() );

    updateState.byProperty( 'excessFunding',
      ( financialModel.values.total_funding > financialModel.values.total_costs ).toString() );

    updateState.byProperty( 'debtRuleViolation',
      ( financialModel.values.debt_totalAtGrad > financialModel.values.salary_annual ).toString() );
  },


  /**
   * updateModelFromSchoolModel - Import financial values from the schoolModel
   * based on stateModel
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

  },

  /**
    * init - Initialize this model
    */
  init: () => {
    initializeFinancialValues();
    // A few properties must be created manually here
    financialModel.createFinancialProperty( 'other_programLength' );

    // These are test values used only for development purposes.

    financialModel._calculateTotals();

  }
};

export {
  financialModel
};
