/* schoolView specifically covers the school search and associated fields, such as
   program length and living situation. */
import { closest } from '../../../../js/modules/util/dom-traverse';
import { schoolSearch } from '../dispatchers/get-api-values';
import { bindEvent } from '../../../../js/modules/util/dom-events';
import { updateSchoolData } from '../dispatchers/update-models.js';
import { updateState } from '../dispatchers/update-state.js';
import { getSchoolValue, getStateValue } from '../dispatchers/get-model-values.js';
import { updateFinancialView, updateGradMeterChart, updateRepaymentMeterChart } from '../dispatchers/update-view.js';


const schoolView = {
  _searchSection: null,
  _searchBox: null,
  _searchResults: null,
  _keyupDelay: null,
  _programRadios: null,
  _schoolInfo: null,
  _schoolItems: [],
  _stateItems: [],

  /* _checkRadioButtonCount: if all radio buttons are clicked, enable the next button */

  _checkRadioButtonCount: function( ) {
    const checkedCount = schoolView._schoolInfo
      .querySelectorAll( 'input[checked="true"]' ).length;
    const questionCount = schoolView._schoolInfo
      .querySelectorAll( '.program-question' ).length;
    if ( checkedCount === questionCount ) {
      document.querySelector( 'button.btn__next-step' ).removeAttribute( 'disabled' );
    }
  },

  _formatSearchResults: function( responseText ) {
    const obj = JSON.parse( responseText );
    let html = '<ul>';
    for ( const key in obj ) {
      const school = obj[key];
      html += '\n<li><button data-school_id="' + school.id + '"><strong>' + school.schoolname + '</strong>';
      html += '<p><em>' + school.city + ', ' + school.state + '</em></p></button></li>';
    }
    html += '</li>';
    this._searchResults.innerHTML = html;
    this._searchResults.classList.add( 'active' );
  },

  _handleInputChange: function( event ) {
    clearTimeout( this._keyupDelay );
    schoolView._keyupDelay = setTimeout( function() {
      const searchTerm = schoolView._searchBox.value;
      // TODO - clean up searchbox text, remove non-alphanumeric characters
      schoolSearch( searchTerm )
        .then( resp => {
          schoolView._formatSearchResults( resp.responseText );
        } );
    }, 500 );
  },

  _handleResultButtonClick: function( event ) {
    const target = event.target;
    let button;
    // Find the button in the clickable area
    if ( target.tagName === 'BUTTON' ) {
      button = target;
    } else {
      button = closest( target, 'BUTTON' );
    }

    // If there's a school_id, then proceed with schoolInfo
    if ( typeof button.dataset.school_id !== 'undefined' ) {
      const iped = button.dataset.school_id;

      // Add schoolData to schoolModel
      updateSchoolData( iped );
    }
  },

  _handleProgramRadioClick: function( event ) {
    const container = closest( event.target, '.m-form-field' );
    const input = container.querySelector( 'input' );
    input.setAttribute( 'checked', true );

    // Update the model with program info
    const prop = input.getAttribute( 'name' );
    const value = input.value;
    updateState.byProperty( prop, value );

    schoolView._checkRadioButtonCount();

  },

  /* Add all event listeners for school search view  */
  _addListeners: () => {
    const searchEvents = {
      keyup: schoolView._handleInputChange
    };
    bindEvent( schoolView._searchBox, searchEvents );

    const searchResultsEvent = {
      click: schoolView._handleResultButtonClick
    };
    bindEvent( schoolView._searchResults, searchResultsEvent );

    const radioEvents = {
      click: schoolView._handleProgramRadioClick
    };
    schoolView._programRadios.forEach( elem => {
      bindEvent( elem, radioEvents );
    } );

  },

  updateSchoolView: () => {
    updateFinancialView();
    updateGradMeterChart();
    updateRepaymentMeterChart();
    schoolView._updateSchoolRadioButtons();
    schoolView.updateSchoolItems();
  },

  updateSchoolItems: function() {
    this._schoolItems.forEach( elem => {

      const prop = elem.dataset.schoolItem;
      let val = getSchoolValue( prop );
      if ( typeof val === 'undefined') val = '';

      elem.innerText = val;

    } );

    this._stateItems.forEach( elem => {

      const prop = elem.dataset.stateItem;
      let val = getStateValue( prop );

      if ( typeof val === 'undefined') val = '';
      
      elem.innerText = val;

    } );

  },

  _updateSchoolRadioButtons: () => {
    const campus = getSchoolValue( 'onCampusAvail' );
    const control = getSchoolValue( 'Public' );
    const buttons = [ 'programLength', 'programType', 'programHousing', 'programRate', 'programStudentType' ];


    schoolView._searchResults.classList.remove( 'active' );
    schoolView._searchBox.value = getSchoolValue( 'school' );
    schoolView._schoolInfo.classList.add( 'active' );

    buttons.forEach( name => {
      const val = getStateValue( name );
      if ( typeof val !== 'undefined' ) {
        schoolView.clickRadioButton( name, val );
      }
    } );

    schoolView._checkRadioButtonCount();

  },

  clickRadioButton: ( name, value ) => {
    if ( value !== null ) {
      const input = document.querySelector( 'INPUT[name="' + name + '"][value="' + value + '"]' );
      const label = closest( input, '.m-form-field__radio' ).querySelector( 'LABEL' );
      label.click();
    }

    schoolView._checkRadioButtonCount();
  },

  init: body => {
    // Set up nodeLists
    schoolView._searchSection = body.querySelector( '#college-costs_school-search' );
    schoolView._searchBox = body.querySelector( '#search__school-input' );
    schoolView._searchResults = body.querySelector( '#search-results' );
    schoolView._programRadios = body.querySelectorAll( '.school-search_additional-info label' );
    schoolView._schoolInfo = body.querySelector( '.school-search_additional-info' );
    schoolView._schoolItems = document.querySelectorAll( '[data-school-item]' );
    schoolView._stateItems = document.querySelectorAll( '[data-state-item]' );

    // Initialize listeners
    schoolView._addListeners();
  }

};

export {
  schoolView
};
