/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
*/

import { bindEvent } from '../../../../js/modules/util/dom-events';
import { setUrlQueryString } from '../util/url-parameter-utils.js';
import { updateNavigationView, updateSchoolItems } from '../dispatchers/update-view.js';

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

  setValue: function( name, value ) {
    stateModel.setStateInDom( name, value );
    if ( name !== 'activeSection' ) {
      stateModel.values[name] = value;
    } else if ( value !== stateModel.values.activeSection ) {
      stateModel.values.activeSection = value;
      window.history.pushState( stateModel.values, null, '' );
      updateNavigationView();
    }
    if ( stateModel.textVersions.hasOwnProperty( name ) ) {
      const key = name + 'Text';
      stateModel.values[key] = stateModel.textVersions[name][value];
      console.log( name, stateModel.values[key] );
      updateSchoolItems();
    }

    setUrlQueryString();
  },

  /**
   * setStateInDom - manages dataset for the MAIN element, which helps display UI elements
   * properly
   * @param {String} property - The state property to modify
   * @param {String} value - The new value of the property
   * NOTE: if the value is null or the Boolean 'false', the data attribute will be removed
   */
  setStateInDom: function( property, value ) {
    if ( value === false || value === null ) {
      stateModel.stateDomElem.removeAttribute( property );
    } else {
      stateModel.stateDomElem.setAttribute( 'data-state_' + property, value );
    }
  },

  /* _addPopStateListener - Add a listener for "pop" events */
  _addPopStateListener: function() {
    const events = {
      popstate: stateModel._handlePopState
    };
    bindEvent( window, events );
  },

  _handlePopState: function( event ) {
    if ( event.state ) {
      // window.history.replaceState( this.values, null, '' );
      stateModel.values.activeSection = event.state.activeSection;
      // stateModel.setValue( 'activeSection', event.state.activeSection );
    }

    updateNavigationView();

  },

  init: function() {
    window.history.replaceState( this.values, null, '' );
    this.stateDomElem = document.querySelector( 'main.college-costs' );
    this._addPopStateListener();

  }

};

export {
  stateModel
};
