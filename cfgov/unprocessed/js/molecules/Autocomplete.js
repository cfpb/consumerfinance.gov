// Required modules.
import { assign } from '../modules/util/assign';
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { ajaxRequest } from '../modules/util/ajax-request';
import * as throttle from 'lodash.throttle';

/**
 * Autocomplete
 * @class
 *
 * @classdesc Initializes the molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @param {Object} opts optional params, including
 * url for suggestions endpoint or list of suggestions,
 * minChars, onSubmit, renderItem, and cleanQuery functions.
 * @returns {Autocomplete} An instance.
 */
function Autocomplete( element, opts ) {

  // Class constants
  const BASE_CLASS = 'm-autocomplete';
  const HIDDEN_CLASS = 'u-hidden';
  const AUTOCOMPLETE_CLASS = 'm-autocomplete_results';
  const SELECTED_CLASS = 'm-autocomplete_selected';

  // Key constants
  const ENTER = 13;
  const UP = 38;
  const DOWN = 40;
  const ESCAPE = 27;

  // Internal variables
  let _autocomplete;
  let _data = [];
  let _suggestions;
  let _isVisible;
  let _selection;

  // Autocomplete elements
  const _dom = checkDom( element, BASE_CLASS );
  const _input = _dom.querySelector( 'input' );

  // Settings
  const _settings = {
    minChars: 2,
    maxChars: 50, /* TODO Get this from the input's maxlength attribute */
    delay: 300,
    url: '',
    list: [],
    onSubmit: function( event, selected ) {
      return selected;
    },
    renderItem: function( item ) {
      const li = document.createElement( 'li' );
      li.setAttribute( 'data-val', item );
      li.innerText = item;
      return li;
    },
    cleanQuery: function( query ) {
      query = query.replace( /[\u0080-\uffff]/g, '' );
      query = query.replace( /[“”‘’]/g, '' );
      return query;
    },
    filterList: function( list ) {
      // TODO: add basic filtering
      _data = list;
    }
  };

  // Search variables
  let _xhr;
  let _searchTerm = '';
  const _throttleFetch = throttle( function() {
    _fetchSuggestions();
  }, _settings.delay );

  assign( _settings, opts );

  /**
   * Set up and create the autocomplete.
   * @returns {Autocomplete|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    _autocomplete = _addContainer();
    _input.setAttribute( 'autocomplete', 'off' );
    _input.setAttribute( 'aria-autocomplete', 'list' );

    _bindEvents();

    return this;
  }

  /**
   * Creates and injects markup for autocomplete.
   * @returns {HTMLNode} <ul> element for autocomplete suggestions.
   */
  function _addContainer() {
    const ul = document.createElement( 'ul' );
    ul.className = AUTOCOMPLETE_CLASS + ' ' + HIDDEN_CLASS;
    document.body.appendChild( ul );
    return ul;
  }

  /**
   * Updates dimensions and position of autocomplete container
   * relative to _input element.
   */
  function _positionContainer() {
    const inputCoords = _input.getBoundingClientRect();
    _autocomplete.style.left = Math.round( inputCoords.left +
      window.pageXOffset ) + 'px';
    _autocomplete.style.top = Math.round( inputCoords.bottom +
      window.pageYOffset ) + 'px';
    _autocomplete.style.width = Math.round( inputCoords.right -
      inputCoords.left ) + 'px';
  }

  /**
   * Binds input, blur, and keydown events on _input element and
   * resize event on window.
   */
  function _bindEvents() {
    _input.addEventListener( 'input', function() {
      _searchTerm = this.value;
      // TODO: Refactor the max length stuff
      if ( _searchTerm.length >= _settings.maxChars ) {
        _input.classList.add( 'a-text-input__error' );
        _input.blur();
        document.getElementById( 'o-search-bar-error_message' ).classList.remove( 'u-hidden' );
        document.querySelector( '.o-form__input-w-btn_btn-container button[type="submit"]' ).setAttribute( 'disabled', 'true' );
        return;
      } else if ( _searchTerm.length <= _settings.maxChars ) {
        _input.classList.remove( 'a-text-input__error' );
        document.getElementById( 'o-search-bar-error_message' ).classList.add( 'u-hidden' );
        document.querySelector( '.o-form__input-w-btn_btn-container button[type="submit"]' ).removeAttribute( 'disabled' );
      }
      if ( _searchTerm.length >= _settings.minChars ) {
        if ( _settings.url ) {
          _throttleFetch();
        } else {
          _settings.filterList( _settings.list );
        }
      } else {
        _hide();
      }
    } );
    _input.addEventListener( 'blur', function() {
      setTimeout( function() {
        const active = document.activeElement;
        if ( active !== _autocomplete && !_autocomplete.contains( active ) ) {
          _hide();
        }
      }, 1 );
    } );
    _input.addEventListener( 'keydown', function( event ) {
      const key = event.keyCode;
      if ( _isVisible ) {
        if ( key === UP ) {
          _prev( event );
        } else if ( key === DOWN ) {
          _next( event );
        } else if ( key === ENTER && _selection > -1 ) {
          event.preventDefault();
          _settings.onSubmit( event, _suggestions[_selection] );
        } else if ( key === ESCAPE ) {
          event.preventDefault();
          _hide();
        }
      }
    } );

    window.addEventListener( 'resize', function() {
      _positionContainer();
    } );

    _autocomplete.addEventListener( 'mousedown', function( event ) {
      event.preventDefault();
    } );
  }

  /**
   * Replaces autocomplete content with suggestions
   * markup for each item in _data array.
   */
  function _updateSuggestions() {
    _reset();
    _data.forEach( function( item, index ) {
      const suggestion = _settings.renderItem( item );
      suggestion.setAttribute( 'data-id', index );
      _suggestions.push( suggestion );
      _autocomplete.appendChild( suggestion );
    } );
    if ( _suggestions.length ) {
      _show();
    } else {
      _hide();
    }
  }

  /**
   * Gets next item in suggestions list and
   * uses it to update current selection.
   */
  function _next() {
    const length = _suggestions.length - 1;
    const index = _selection >= length ? 0 : _selection + 1;
    _updateSelection( index );
  }

  /**
   * Gets previous item in suggestions list and
   * uses it to update current selection.
   */
  function _prev() {
    const index = _selection > 0 ? _selection - 1 : _suggestions.length - 1;
    _updateSelection( index );
  }

  /**
   * Updates selected item in suggestions list and scrolls
   * it into view. Sets _input value to new selection.
   *
   * @param  {number} index Index of new selection
   */
  function _updateSelection( index ) {
    if ( _selection > -1 ) {
      _suggestions[_selection].classList.remove( SELECTED_CLASS );
    }
    _selection = index;
    const item = _suggestions[index];

    _input.value = item.getAttribute( 'data-val' );
    item.classList.add( SELECTED_CLASS );
    _scrollSelectionIntoView();
  }

  /**
   * Scrolls autocomplete suggestions list so current
   * selection is visible.
   */
  function _scrollSelectionIntoView() {
    const _target = _suggestions[_selection];
    _autocomplete.scrollTop = _target.offsetTop -
      _autocomplete.clientHeight + _target.clientHeight;
  }

  /**
   * Resets autocomplete suggestions and current selection.
   */
  function _reset() {
    _selection = -1;
    _suggestions = [];
    _autocomplete.innerHTML = '';
  }

  /**
   * Hides autocomplete suggestion list.
   */
  function _hide() {
    _isVisible = false;
    _autocomplete.classList.add( HIDDEN_CLASS );
  }

  /**
   * Shows autocomplete suggestion list.
   */
  function _show() {
    _isVisible = true;
    _positionContainer();
    _autocomplete.classList.remove( HIDDEN_CLASS );
  }

  /**
   * Initiates request for autocomplete suggestions
   * to endpoint specified in settings. Aborts any existing
   * request.
   */
  function _fetchSuggestions() {
    if ( _xhr ) {
      _xhr.abort();
    }
    _xhr = ajaxRequest(
      'GET',
      _settings.url + _settings.cleanQuery( _searchTerm ),
      {
        success: _success,
        fail: _fail
      }
    );
  }

  /**
   * On success, tries to parse xhr response
   * and use resulting data to populate autocomplete
   * suggestions list.
   */
  function _success() {
    try {
      _data = JSON.parse( _xhr.responseText );
      _updateSuggestions();
    } catch ( err ) {
      _fail();
    }
    _xhr = null;
  }

  /**
   * On xhr failure, clears data array and
   * resets and hides autocomplete.
   */
  function _fail() {
    _data = [];
    _reset();
    _hide();
  }

  this.init = init;

  return this;
}

export default Autocomplete;
