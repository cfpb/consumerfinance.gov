/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/
import { recalculateFinancials } from '../dispatchers/update-models.js';
import { updateFinancialViewAndFinancialCharts, updateNavigationView, updateSchoolItems, updateStateInDom, updateUrlQueryString } from '../dispatchers/update-view.js';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const stateModel = {
  stateDomElem: null,
  values: {
    activeSection: null,
    schoolSelected: null,
    gotStarted: false,
    costsQuestion: false,
    programType: null,
    programLength: null,
    programRate: null,
    programHousing: null
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
   */
  setValue: function( name, value ) {
    updateStateInDom( name, value );
    if ( name === 'activeSection' ) {
      // In case this method gets used to update activeSection...
      stateModel.setActiveSection( value );
    } else {
      stateModel.values[name] = value;
      updateUrlQueryString();
    }
    if ( stateModel.textVersions.hasOwnProperty( name ) ) {
      const key = name + 'Text';
      stateModel.values[key] = stateModel.textVersions[name][value];
      updateSchoolItems();
    }
    // When program values are updated, recalculate, updateView
    if ( name.indexOf( 'program' ) === 0 ) {
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
