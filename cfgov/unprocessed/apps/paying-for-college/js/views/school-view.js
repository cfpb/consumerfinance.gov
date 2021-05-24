/* schoolView specifically covers the school search and associated fields, such as
   program length and living situation. */
import {
  getProgramList,
  getSchoolValue,
  getStateValue
} from '../dispatchers/get-model-values.js';
import {
  recalculateFinancials,
  refreshExpenses,
  updateFinancial,
  updateSchoolData
} from '../dispatchers/update-models.js';
import {
  updateFinancialView,
  updateFinancialViewAndFinancialCharts,
  updateGradMeterChart,
  updateRepaymentMeterChart
} from '../dispatchers/update-view.js';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';
import { decimalToPercentString, stringToNum } from '../util/number-utils.js';
import { schoolSearch } from '../dispatchers/get-api-values';
import { updateState } from '../dispatchers/update-state.js';

const schoolView = {
  _searchSection: null,
  _searchBox: null,
  _searchResults: null,
  _programRadios: null,
  _schoolInfo: null,
  _schoolItems: [],
  _stateItems: [],
  _programSelect: null,

  updateSchoolView: () => {
    updateFinancialView();
    updateGradMeterChart();
    updateRepaymentMeterChart();
    schoolView._updateSchoolRadioButtons();
    schoolView.updateSchoolItems();
    schoolView._updateProgramList();
  },

  updateSchoolItems: function() {
    this._schoolItems.forEach( elem => {

      const prop = elem.dataset.schoolItem;
      let val = getSchoolValue( prop );
      // Prevent improper values from being displayed on the page
      if ( typeof val === 'undefined' || val === false || val === null ) {
        val = '';
      }

      if ( elem.dataset.numberDisplay === 'percentage' ) {
        val = decimalToPercentString( val, 0 );
      }

      elem.innerText = val;

    } );

    this._stateItems.forEach( elem => {
      const prop = elem.dataset.stateItem;
      let val = getStateValue( prop );
      // Prevent improper values from being displayed on the page
      if ( typeof val === 'undefined' || val === false || val === null ) {
        val = '';
      }
      elem.innerText = val;
    } );

  },

  /**
   * updateViewWithErrors - updates form fields with classes to show error states.
   * NOTE: The appearance of error messages is mostly found in the state-based.less rules
   */
  updateViewWithErrors: () => {
    const errorChecks = [ 'programType', 'programProgress', 'programLength',
      'programLevel', 'programRate', 'programHousing', 'programDependency' ];

    const searchBox = document.querySelector( '#search__school-input' );
    if ( getStateValue( 'schoolSelected' ) === false ) {
      searchBox.classList.add( 'a-text-input__warning' );
    } else {
      searchBox.classList.remove( 'a-text-input__warning' );
    }
  },

  _updateProgramList: () => {
    let level = 'undergrad';
    if ( getStateValue( 'programType' ) === 'graduate' ) {
      level = 'graduate';
    }

    const list = getProgramList( level );
    if ( list.length > 0 ) {
      updateState.byProperty( 'schoolHasPrograms', 'yes' );
    } else {
      updateState.byProperty( 'schoolHasPrograms', 'no' );
    }

    if ( list.length > 0 ) {
      let html = '<option selected="selected" value="null">Select...</option>';
      list.forEach( elem => {
        html += `
          <option data-program-salary="${ elem.salary }" value="${ elem.code }">
                ${ elem.level } - ${ elem.name }
          </option>`;
      } );
      html += '\n<option value="null">My program is not listed here/I am undecided.</option>';
      schoolView._programSelect.innerHTML = html;

      // If there's a program id in the state, select that program
      if ( getStateValue( 'pid' ) ) {
        document.querySelector( '#program-select' ).value = getStateValue( 'pid' );
      }
    }
  },

  _updateSchoolRadioButtons: () => {
    const buttons = [ 'programLength', 'programType', 'programHousing', 'programProgress',
      'programRate', 'programDependency' ];

    schoolView._searchResults.classList.remove( 'active' );
    schoolView._searchBox.value = getSchoolValue( 'school' );
    schoolView._schoolInfo.classList.add( 'active' );

    buttons.forEach( name => {
      const val = getStateValue( name );
      if ( typeof val !== 'undefined' ) {
        schoolView.clickRadioButton( name, val );
      }
    } );

  },

  clickRadioButton: ( name, value ) => {
    if ( name !== null && value !== false ) {
      const input = document.querySelector( 'INPUT[name="' + name + '"][value="' + value + '"]' );
      if ( input !== null ) {
        const label = closest( input, '.m-form-field__radio' ).querySelector( 'LABEL' );
        label.click();
      }
    }
  },

  init: body => {
    // Set up nodeLists
    schoolView._searchSection = body.querySelector( '#college-costs_school-search' );
    schoolView._searchBox = body.querySelector( '#search__school-input' );
    schoolView._searchResults = body.querySelector( '#search-results' );
    schoolView._programRadios = body.querySelectorAll( '.school-search_additional-info label' );
    schoolView._programSelect = body.querySelector( '#program-select' );
    schoolView._schoolInfo = body.querySelector( '.school-search_additional-info' );
    schoolView._schoolItems = document.querySelectorAll( '[data-school-item]' );
    schoolView._stateItems = document.querySelectorAll( '[data-state-item]' );

    // Initialize listeners
    _addListeners();
  }
};

/**
 * Add all event listeners for school search view
 */
function _addListeners() {
  schoolView._searchBox.addEventListener( 'keyup', _handleInputChange );
  schoolView._searchResults.addEventListener( 'click', _handleResultButtonClick );

  schoolView._programRadios.forEach( elem => {
    elem.addEventListener( 'click', _handleProgramRadioClick );
  } );

  schoolView._programSelect.addEventListener( 'change', _handleProgramSelectChange );
}

/**
 * Convert JSON string of school search results into markup.
 * @param {string} responseText - JSON string of school info.
 */
function _formatSearchResults( responseText ) {
  const obj = JSON.parse( responseText );
  let html = '<ul>';
  for ( const key in obj ) {
    const school = obj[key];
    html += '\n<li><button role="button" data-school_id="' + school.id + '"><strong>' + school.schoolname + '</strong>';
    html += '<p><em>' + school.city + ', ' + school.state + '</em></p></button></li>';
  }
  html += '</li>';
  schoolView._searchResults.innerHTML = html;
  schoolView._searchResults.classList.add( 'active' );
}

let _keyupDelay;

/**
 * Text has been entered in the school search input.
 * @param {KeyboardEvent} event - keyup event object.
 */
function _handleInputChange( event ) {
  clearTimeout( _keyupDelay );
  _keyupDelay = setTimeout( function() {
    const searchTerm = schoolView._searchBox.value.trim();
    // TODO - clean up searchbox text, remove non-alphanumeric characters
    if ( !searchTerm ) {
      schoolView._searchResults.classList.remove( 'active' );
    } else if ( searchTerm.length > 2 ) {
      schoolSearch( searchTerm )
        .then( resp => {
          _formatSearchResults( resp.responseText );
        }, error => {
          console.log( error );
        } );
    }
  }, 500 );
}

/**
 * Graduate program selection has changed.
 * @param {Event} event - change event object.
 */
function _handleProgramSelectChange( event ) {
  const target = event.target;
  const salary = target.options[target.selectedIndex].dataset.programSalary;
  let programName = target.options[target.selectedIndex].innerText;
  let pid = target.value;
  if ( pid === 'null' ) {
    pid = false;
    programName = '';
  }
  updateState.byProperty( 'pid', pid );
  updateState.byProperty( 'programName', programName );
  if ( salary ) {
    updateFinancial( 'salary_annual', salary );
  } else {
    updateFinancial( 'salary_annual', stringToNum( getSchoolValue( 'medianAnnualPay6Yr' ) ) );
  }
  refreshExpenses();
}

/**
 * An item in the search results box was clicked.
 * @param {MouseEvent} event - click event object.
 */
function _handleResultButtonClick( event ) {
  const target = event.target;
  let button;
  // Find the button in the clickable area
  if ( target.tagName === 'BUTTON' ) {
    button = target;
  } else {
    button = closest( target, 'BUTTON' );
  }

  // Clear pid from state
  updateState.byProperty( 'pid', false );

  // If there's a school_id, then proceed with schoolInfo
  if ( typeof button.dataset.school_id !== 'undefined' ) {
    const iped = button.dataset.school_id;

    // Add schoolData to schoolModel
    updateSchoolData( iped );
  }
}

/**
 * A school program selection radio button was clicked.
 * @param {MouseEvent} event - click event object.
 */
function _handleProgramRadioClick( event ) {
  const container = closest( event.target, '.m-form-field' );
  const input = container.querySelector( 'input' );
  const recalcProps = [ 'programProgress', 'programLength', 'programType',
    'programDependency' ];

  // Update the model with program info
  const prop = input.getAttribute( 'name' );
  const value = input.value;
  updateState.byProperty( prop, value );
  if ( prop === 'programType' ) {
    schoolView._updateProgramList();
  }

  if ( recalcProps.indexOf( prop ) !== -1 ) {
    recalculateFinancials();
    updateFinancialViewAndFinancialCharts();
  }
}

export {
  schoolView
};
