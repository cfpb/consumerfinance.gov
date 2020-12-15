/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/
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
  'pid', 'programHousing', 'programType', 'programLength',
  'programRate', 'programStudentType', 'costsQuestion', 'expensesRegion',
  'impactOffer', 'impactLoans', 'utmSource', 'utm_medium', 'utm_campaign'
];

const stateModel = {
  stateDomElem: null,
  values: {
    activeSection: false,
    constantsLoaded: false,
    schoolSelected: false,
    gotStarted: false,
    gradMeterCohort: 'cohortRankByHighestDegree',
    gradMeterCohortName: 'U.S.',
    costsQuestion: false,
    programType: false,
    programLength: false,
    programLevel: false,
    programRate: false,
    programHousing: false,
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
    updateStateInDom( name, value );
    if ( name === 'activeSection' ) {
      // In case this method gets used to update activeSection...
      stateModel.setActiveSection( value );
    } else {
      stateModel.values[name] = value;
      if ( updateURL !== false && urlVals.indexOf( name ) > -1 ) {
        updateUrlQueryString();
      }
    }
    if ( stateModel.textVersions.hasOwnProperty( name ) ) {
      const key = name + 'Text';
      stateModel.values[key] = stateModel.textVersions[name][value];
      updateSchoolItems();
    }

    // When the meter buttons are clicked, updateSchoolItems
    if ( name.indexOf( 'MeterThird' ) > 0 ) {
      updateSchoolItems();
    }

    // When program values are updated, recalculate, updateView
    if ( name.indexOf( 'program' ) === 0 ) {
      if ( name === 'programType' && value === 'graduate' ) {
        stateModel.setValue( 'programLevel', 'graduate' );
      } else if ( name === 'programType' ) {
        stateModel.setValue( 'programLevel', 'undergrad' );
      }

      if ( name === 'programLength' ) {
        updateFinancial( 'other_programLength', value );
      }

      recalculateFinancials();
      updateFinancialViewAndFinancialCharts();
    }
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
