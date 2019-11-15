/* schoolView specifically covers the school search and associated fields, such as
   program length and living situation. */
import { closest } from '../../../../js/modules/util/dom-traverse';
import { schoolSearch } from '../dispatchers/get-api-values';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const schoolView = {
  _searchSection: null,
  _searchBox: null,
  _searchResults: null,
  _keyupDelay: null,
  _programRadios: null,
  _schoolInfo: null,

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
    this._keyupDelay = setTimeout( function() {
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
      schoolView._searchResults.classList.remove( 'active' );
      schoolView._searchBox.value = button.querySelector( 'strong' ).innerText;
      schoolView._schoolInfo.classList.add( 'active' );

    }
  },

  _handleProgramRadioClick: function( event ) {
    const container = closest( event.target, '.m-form-field' );
    const input = container.querySelector( 'input' );
    input.setAttribute( 'checked', true );

    const checkedCount = schoolView._schoolInfo
      .querySelectorAll( 'input[checked="true"]' ).length;
    const questionCount = schoolView._schoolInfo
      .querySelectorAll( '.program-question' ).length;
    if ( checkedCount === questionCount ) {
      schoolView._searchSection.querySelector( 'button[data-button-target]' )
        .removeAttribute( 'disabled' );
    }
  },

  _addListeners: function() {
    const searchEvents = {
      keyup: this._handleInputChange
    };
    bindEvent( this._searchBox, searchEvents );

    const searchResultsEvent = {
      click: this._handleResultButtonClick
    };
    bindEvent( this._searchResults, searchResultsEvent );

    const radioEvents = {
      click: this._handleProgramRadioClick
    };
    this._programRadios.forEach( elem => {
      bindEvent( elem, radioEvents );
    } );
  },

  init: function( body ) {
    // Set up nodeLists
    this._searchSection = body.querySelector( '#college-costs_school-search' );
    this._searchBox = body.querySelector( '#search__school-input' );
    this._searchResults = body.querySelector( '#search__results' );
    this._programRadios = body.querySelectorAll( '.school-search_additional-info label' );
    this._schoolInfo = body.querySelector( '.school-search_additional-info' );

    // Initialize listeners
    this._addListeners();
  }

};

export {
  schoolView
};
