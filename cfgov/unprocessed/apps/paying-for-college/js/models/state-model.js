/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/

import { bindEvent } from '../../../../js/modules/util/dom-events';
import { updateUrlQueryString, updateNavigationView, updateSchoolItems, updateStateInDom } from '../dispatchers/update-view.js';

const stateModel = {
  stateDomElem: null,
  values: {
    activeSection: null,
    schoolSelected: null,
    gotStarted: false,
    costsButtonClicked: false,
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
   * setValue - Public method to update model values
   * @param {String} name - the name of the property to update
   * @param {*} value - the value to be assigned
   */
  setValue: function( name, value ) {
    updateStateInDom( name, value );
    if ( name !== 'activeSection' ) {
      stateModel.values[name] = value;
      updateUrlQueryString();
    } else if ( value !== stateModel.values.activeSection ) {
      stateModel.values.activeSection = value;
      window.history.pushState( stateModel.values, null, '' );
      updateNavigationView();
    }
    if ( stateModel.textVersions.hasOwnProperty( name ) ) {
      const key = name + 'Text';
      stateModel.values[key] = stateModel.textVersions[name][value];
      updateSchoolItems();
    }
  }

};

export {
  stateModel
};
