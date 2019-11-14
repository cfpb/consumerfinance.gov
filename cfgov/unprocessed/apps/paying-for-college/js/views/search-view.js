import { closest } from '../../../../js/modules/util/dom-traverse';
import { schoolSearch } from '../dispatchers/get-api-values';
import { bindEvent } from '../../../../js/modules/util/dom-events';

const searchView = {
  _searchSection: null,
  _searchBox: null,
  _searchResults: null,
  _keyupDelay: null,

  _formatSearchResults: function( responseText ) {
    const obj = JSON.parse( responseText );
    let html = '<ul>';
    for ( const key in obj ) {
      const school = obj[key];
      console.log( school );
      html += '\n<li><button data-school_id="' + school.id + '"><strong>' + school.schoolname + '</strong>';
      html += '<p><em>' + school.city  + ', ' + school.state + '</em></p></button></li>';
      
    }
    html += '</li>';
    this._searchResults.innerHTML = html;
    this._searchResults.classList.add( 'active' );
  },

  _handleInputChange: function( event ) {
    clearTimeout( this._keyupDelay );
    this._keyupDelay = setTimeout( function() {
      const searchTerm = searchView._searchBox.value;
      // TODO - clean up searchbox text, remove non-alphanumeric characters
      console.log( searchTerm );
      schoolSearch( searchTerm )
        .then( resp => {
          searchView._formatSearchResults( resp.responseText );
        } );
    }, 500 );
  },

  _handleResultButtonClick: function( event ) {
    const target = event.target;
    let button;
    if ( target.tagName === 'BUTTON' ) {
      button = target;
    } else {
      button = closest( target, 'BUTTON' );
    }
    console.log( button.dataset );
    if ( typeof button.dataset.school_id !== 'undefined' ) {
      console.log( button.dataset.school_id );
      searchView._searchResults.classList.remove( 'active' );
      console.log( button.innerText );
      searchView._searchBox.value = button.querySelector( 'strong' ).innerText;
    }
  },

  _addKeyListener: function() {
    const events = {
      keyup: this._handleInputChange,
      focusout: this._handleInputChange
    };
    bindEvent( this._searchBox, events );
  },

  _addResultButtonListener: function() {
    const events = {
      click: this._handleResultButtonClick
    };
    bindEvent( this._searchResults, events );
  },

  init: function( body ) {
    // Set up nodeLists
    this._searchSection = body.querySelector( '#college-costs__school-search' );
    this._searchBox = body.querySelector( '#search__school-input' );
    this._searchResults = body.querySelector( '#search__results' );

    // Initialize listeners
    this._addKeyListener();
    this._addResultButtonListener();
  }

};

export {
  searchView
};
