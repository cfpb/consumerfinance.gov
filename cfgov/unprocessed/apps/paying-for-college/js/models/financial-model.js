/*
This file contains the model for financial data, which encompasses the costs
of college, grants, loans, etc. It also includes debt calculations
based on these costs.
*/

import {
  getConstantsValue,
  getSchoolValue,
  getStateValue
} from '../dispatchers/get-model-values.js';
import {
  initializeFinancialValues,
  recalculateExpenses
} from '../dispatchers/update-models.js';
import {
  updateFinancialViewAndFinancialCharts,
  updateUrlQueryString
} from '../dispatchers/update-view.js';
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
    financialModel._updateRates();
    financialModel._calculateTotals();
    debtCalculator();

    // set monthly salary value
    financialModel.values.salary_monthly = financialModel.values.salary_annual / 12;

    // set text of "hours to cover payment"
    const hours = Math.floor( financialModel.values.debt_repayHours * 100 ) / 100;
    const weeks = Math.floor( financialModel.values.debt_repayWorkWeeks * 100 ) / 100;
    const coverString = hours + 'hours, or ' + weeks + 'forty-hour work weeks';
    updateState.byProperty( 'hoursToCoverPaymentText',  )

    recalculateExpenses();

    // Debt Guide Difference
    financialModel.values.other_debtGuideDifference =
        Math.abs( financialModel.values.debt_totalAtGrad - financialModel.values.salary_annual );

    financialModel._updateStateWithFinancials();

  },

  /**
   * setValue - Used to set a value
   * @param {String} name - Property name
   * @param {Number} value - New value of property
   * @param {Boolean} updateView - (defaults true) should view be updated?
   */
  setValue: ( name, value, updateView ) => {
    if ( financialModel.values.hasOwnProperty( name ) ) {
      financialModel.values[name] = stringToNum( value );
      financialModel.recalculate();

      if ( updateView !== false ) {
        updateUrlQueryString();
        updateFinancialViewAndFinancialCharts();
      }
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

    // Enforce the limits if constants are loaded
    if ( getStateValue( 'constantsLoaded' ) === true ) {
      const errors = financialModel._enforceLimits();
    }

    // Calculate totals
    for ( const prop in vals ) {
      const prefix = prop.split( '_' )[0];
      if ( totals.hasOwnProperty( prefix ) ) {
        // For loans, get net amount after fees
        let val = vals[prop];
        if ( prop.indexOf( 'Loan' ) > 0 ) {
          val = financialModel._amountAfterFee( prop );
        }

        vals[totals[prefix]] += val;
      }
    }

    // Calculate more totals
    vals.total_borrowing = vals.total_fedLoans + vals.total_publicLoans + vals.total_privateLoans +
        vals.total_plusLoans;
    vals.total_grantsScholarships = vals.total_grants + vals.total_scholarships;
    vals.total_otherResources = vals.total_savings + vals.total_income;
    vals.total_workStudyFellowAssist = vals.total_workStudy + vals.total_fellowAssist;
    vals.total_contributions = vals.total_grantsScholarships + vals.total_otherResources +
        vals.total_workStudyFellowAssist;
    vals.total_costs = vals.total_directCosts + vals.total_indirectCosts + vals.otherCost_additional;
    vals.total_funding = vals.total_contributions + vals.total_borrowing;
    vals.total_gap = Math.round( vals.total_costs - vals.total_funding );
    vals.total_excessFunding = Math.round( vals.total_funding - vals.total_costs );

    /* Borrowing total
       TODO - Update this once year-by-year DIRECT borrowing is in place */
    vals.total_borrowingAtGrad = vals.total_borrowing * vals.other_programLength;

    if ( vals.total_gap < 0 ) {
      vals.total_gap = 0;
    }
  },

  /**
   * Check and enforce various limits on federal loans and grants
   * NOTE: an error indicates the number went over "max", we don't log errors when
   * a value is below 0.
   * @returns {Object} An object of errors found during enforcement
   */
  _enforceLimits: () => {
    let unsubCap = 0;
    const errors = {};

    // get the caps from the constants model

    // First, enforce subsidized cap
    const subResult = enforceRange( financialModel.values.fedLoan_directSub,
      0,
      getConstantsValue( 'subCaps' ).yearOne );
    if ( subResult !== false ) {
      financialModel.values.fedLoan_directSub = subResult.value;
      // Reserve for later error handling
      if ( subResult.error !== false ) {
        errors.fedLoan_directSub = subResult.error;
      }
    }

    // Calculate unsubsidized loan cap based on subsidized loan amount
    if ( getStateValue( 'programType' ) === 'graduate' ) {
      // If graduate, zero out subsidized and parentPlus loans, set unsubsidized cap
      financialModel.values.fedLoan_directSub = 0;
      financialModel.values.plusLoan_parentPlus = 0;
      unsubCap = getConstantsValue( 'unsubsidizedCapGrad' );
    } else {
      // if undergraduate, zero out gradPlus loans, fellowships, set unsubsidized cap
      financialModel.values.plusLoan_gradPlus = 0;
      financialModel.values.fellowAssist_fellowship = 0;
      financialModel.values.fellowAssist_assistantship = 0;

      if ( getStateValue( 'programDependency' ) === 'independent' ) {
        unsubCap = Math.max( 0, getConstantsValue( 'totalIndepCaps' ).yearOne );
      } else {
        unsubCap = Math.max( 0, getConstantsValue( 'totalCaps' ).yearOne );
      }
    }

    // enforce unsub range
    const unsubResult = enforceRange( financialModel.values.fedLoan_directUnsub,
      0,
      unsubCap );
    if ( unsubResult !== false ) {
      financialModel.values.fedLoan_directUnsub = unsubResult.value;
      if ( unsubResult.error !== false ) {
        errors.fedLoan_directUnsub = unsubResult.error;
      }
    }


    // Set other limits based on the constants model
    const limits = {
      grant_pell: [ 0, getConstantsValue( 'pellCap' ) ],
      grant_mta: [ 0, getConstantsValue( 'militaryAssistanceCap' ) ]
    };

    // Check values for min/max violations, log errors
    for ( const key in limits ) {
      let value = 0;
      const result = enforceRange( financialModel.values[key], limits[key][0], limits[key][1] );
      if ( result !== false ) {
        value = result.value;
        if ( result.error !== false ) {
          errors[key] = result.error;
        }
      }
      financialModel.values[key] = value;
    }

    return errors;

  },

  /**
   * _amountAfterFee - return net loan amount, after fee has been removed. Also, add
   * a value to the Object of this net amount.
   * @param {String} prop - Property name of the loan
   * @returns {Number} net value of loan after fee
   */
  _amountAfterFee( prop ) {
    const vals = financialModel.values;
    const loanName = prop.split( '_' )[1];
    let fee = 0;
    if ( vals.hasOwnProperty( 'fee_' + loanName ) ) {
      fee = vals['fee_' + loanName];
    }
    const net = vals[prop] - ( vals[prop] * fee );
    vals['net_' + loanName] = net;

    return net;
  },

  /**
   * Set loan rates based on program type
   */
  _updateRates: () => {
    if ( getStateValue( 'programLevel' ) === 'graduate' ) {
      financialModel.values.rate_directUnsub = getConstantsValue( 'unsubsidizedRateGrad' );
    } else {
      financialModel.values.rate_directUnsub = getConstantsValue( 'unsubsidizedRateUndergrad' );
    }
  },

  /**
   * _updateStateWithFinancials: Based on financial situation, update the application state
   */
  _updateStateWithFinancials: () => {
    updateState.byProperty( 'uncoveredCosts',
      ( financialModel.values.total_gap > 0 ).toString() );

    updateState.byProperty( 'excessFunding',
      ( financialModel.values.total_excessFunding > 0 ).toString() );

    updateState.byProperty( 'debtRuleViolation',
      ( financialModel.values.debt_totalAtGrad > financialModel.values.salary_annual ).toString() );
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
      outOfState: 'Ooss',
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

    // If no rate, assume in-state
    if ( rateProperties.hasOwnProperty( rate ) ) {
      tuitionProp += rateProperties[rate];
    } else {
      tuitionProp += 'InS';
    }

    // Get correct tuition based on property name
    financialModel.values.dirCost_tuition = stringToNum( getSchoolValue( tuitionProp ) );

    // Get program length
    financialModel.values.other_programLength = getStateValue( 'programLength' );

    // Get housing costs
    housingProp += housingProperties[housing];
    if ( housing === 'withFamily' ) {
      financialModel.values.dirCost_housing = 0;
    } else {
      financialModel.values.dirCost_housing = stringToNum( getSchoolValue( housingProp ) );
    }


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
