/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/
import { getSchoolValue } from '../dispatchers/get-model-values.js';
import {
  recalculateFinancials,
  updateFinancial
} from '../dispatchers/update-models.js';
import {
  updateFinancialViewAndFinancialCharts,
  updateNavigationView,
  updateSchoolItems,
  updateStateInDom,
  updateUrlQueryString
} from '../dispatchers/update-view.js';

const urlVals = [
  'pid', 'programHousing', 'programType', 'programProgress', 'programLength',
  'programRate', 'programDependency', 'costsQuestion', 'expensesRegion',
  'impactOffer', 'impactLoans', 'utmSource', 'utm_medium', 'utm_campaign'
];

const stateModel = {
  stateDomElem: null,
  values: {
    activeSection: false,
    constantsLoaded: false,
    hoursToCoverPaymentText: '',
    showSchoolErrors: false,
    schoolSelected: false,
    gotStarted: false,
    gradMeterCohort: 'cohortRankByHighestDegree',
    gradMeterCohortName: 'U.S.',
    costsQuestion: false,
    programType: 'not-selected',
    programLength: 'not-selected',
    programLevel: 'not-selected',
    programRate: 'not-selected',
    programHousing: 'not-selected',
    programDependency: 'not-selected',
    programProgress: 'not-selected',
    repayMeterCohort: 'cohortRankByHighestDegree',
    repayMeterCohortName: 'U.S.'
  },
  textVersions: {
    programType: {
      certificate: 'certificate',
      associates: 'Associates\'s Degree',
      bachelors: 'Bachelor\'s Degree',
      graduate: 'Graduate\'s Degree'
    },
    programLength: {
      1: '1 year',
      2: '2 years',
      3: '3 years',
      4: '4 years',
      5: '5 years',
      6: '6 years'
    },
    programHousing: {
      onCampus: 'On campus',
      offCampus: 'Off campus (you will pay rent/mortgage)',
      withFamily: 'With family (you will not pay rent/mortgage)'
    },
    programRate: {
      inState: 'In-state',
      outOfState: 'Out of state',
      inDistrict: 'In district'
    }
  },
  sectionOrder: [
    'school-info',
    'costs',
    'grants-scholarships',
    'work-study',
    'federal-loans',
    'school-loans',
    'other-resources',
    'loan-counseling',
    'make-a-plan',
    'max-debt-guideline',
    'cost-of-borrowing',
    'affording-your-loans',
    'school-results',
    'summary',
    'action-plan',
    'save-and-finish'
  ],

  /**
  * Check whether required fields are selected
  * @returns {Boolean} false if the school form is incomplete, true otherwise
  */
  _checkRequiredFields: function() {
    // Don't check required fields until the
    if ( stateModel.showSchoolErrors === false ) {
      return false;
    }
    const smv = stateModel.values;
    const control = getSchoolValue( 'control' );
    stateModel.values.schoolErrors = 'no';
    updateStateInDom( 'schoolErrors', 'no' );

    const displayErrors = {
      // These are true if the error should be shown, false otherwise
      schoolSelected: getSchoolValue( 'schoolID' ) === false,
      programTypeSelected: smv.programType === 'not-selected',
      programLengthSelected: smv.programLength === 'not-selected',
      rateSelected: smv.programRate === 'not-selected' && control === 'Public',
      housingSelected: smv.programHousing === 'not-selected',
      dependencySelected:  smv.programLevel === 'undergrad' && smv.programDependency === 'not-selected'
    };

    // Change values to "required" which triggers error notification CSS rules
    for ( const key in displayErrors ) {
      if ( displayErrors[key] === true ) {
        stateModel.values[key] = 'required';
        updateStateInDom( key, 'required' );
        stateModel.values.schoolErrors = 'yes';
        updateStateInDom( 'schoolErrors', 'yes' );
      } else {
        stateModel.values[key] = false;
        updateStateInDom( key, false );
      }
    }

    if ( stateModel.values.schoolErrors === 'no' ) {
      stateModel.values.showSchoolErrors = false;
      updateStateInDom( 'showSchoolErrors', false );
    }

    return true;
  },

  /**
   * set the salaryAvailable property based on other values
   */
  _setSalaryAvailable: () => {
    let available = 'yes';
    const smv = stateModel.values;
    if ( smv.programLevel === 'graduate' && smv.pid === false ) {
      available = 'no';
    }
    stateModel.values.salaryAvailable = available;
    updateStateInDom( 'salaryAvailable', available );
  },

  /**
   * set programLevel property based on programType
   */
  _setProgramLevel: () => {
    const programType = stateModel.values.programType;
    let programLevel = 'undergrad';
    if ( programType === 'graduate' ) {
      programLevel = 'graduate';
    }

    stateModel.values.programLevel = programLevel;
    updateStateInDom( 'programLevel', programLevel );
  },

  /**
   * update the application state based on the 'property' parameter.
   * @param {string} property  What property to update based on
   */
  _updateApplicationState: property => {
    const urlParams = [ 'pid', 'programHousing', 'programType', 'programProgress',
      'programLength', 'programRate', 'programDependency', 'costsQuestion',
      'expensesRegion', 'impactOffer', 'impactLoans', 'utmSource', 'utm_medium',
      'utm_campaign' ];

    const finUpdate = [ 'programType', 'programRate', 'programDependency',
      'programLength', 'programHousing' ];

    // Properties which require a URL querystring update:
    if ( urlParams.indexOf( property ) > 0 ) {
      updateUrlQueryString();
    }

    // Properties which require a financialModel and financialView update:
    if ( finUpdate.indexOf( property ) > 0 ) {
      recalculateFinancials();
      updateFinancialViewAndFinancialCharts();
    }

    if ( stateModel.textVersions.hasOwnProperty( property ) ) {
      const value = stateModel.values[property];
      const key = property + 'Text';
      stateModel.values[key] = stateModel.textVersions[property][value];
      updateSchoolItems();
    }

    // When the meter buttons are clicked, updateSchoolItems
    if ( property.indexOf( 'MeterThird' ) > 0 ) {
      updateSchoolItems();
    }

    // Update state values which are based on other values
    stateModel._setProgramLevel();
    stateModel._setSalaryAvailable();
    stateModel._checkRequiredFields();
  },

  /**
   * pushStateToHistory - Push current application state to window.history
   */
  pushStateToHistory: () => {
    const historyState = {
      activeSection: stateModel.values.activeSection
    };
    window.history.pushState( historyState, null, window.location.search );
  },

  /**
   * replaceStateInHistory - Replace current application state in window.history
   * @param {String} queryString - The queryString to put in the history object
   */
  replaceStateInHistory: queryString => {
    const historyState = {
      activeSection: stateModel.values.activeSection
    };
    if ( typeof queryString === 'undefined' ) queryString = window.location.search;
    window.history.replaceState( historyState, null, queryString );
  },

  /**
   * setValue - Public method to update model values
   * @param {String} name - the name of the property to update
   * @param {*} value - the value to be assigned
   * @param {Boolean} updateURL - whether or not to update the URL
   */
  setValue: function( name, value, updateURL ) {
    // In case this method gets used to update activeSection...
    if ( name === 'activeSection' ) {
      stateModel.setActiveSection( value );
    }
    if ( name === 'programLength' ) {
      updateFinancial( 'other_programLength', value, true );
    }
    stateModel.values[name] = value;
    updateStateInDom( name, value );

    stateModel._updateApplicationState( name );
  },

  /**
   * setActiveSection - Method to update the app's active section
   * @param {*} value - the value to be assigned
   * @param {Boolean} popState - true if the update is the result of a popState event
   */
  setActiveSection: function( value, popState ) {
    updateStateInDom( 'activeSection', value );
    stateModel.setValue( 'save-for-later', false );
    stateModel.values.activeSection = value;
    if ( popState !== true ) {
      stateModel.pushStateToHistory();
    }
    updateNavigationView();
  }

};

export {
  stateModel
};
