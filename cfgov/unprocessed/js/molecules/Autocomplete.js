'use strict';
// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var throttle = require( '../modules/util/throttle' ).throttle;
var ajaxRequest = require( '../modules/util/ajax-request' ).ajaxRequest;
var bindEvent = require( '../modules/util/dom-events' ).bindEvent;
var standardType = require( '../modules/util/standard-type' );
var assign = require( '../modules/util/assign' ).assign;

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
  var BASE_CLASS = 'm-autocomplete';
  var HIDDEN_CLASS = 'u-hidden';
  var AUTOCOMPLETE_CLASS = 'm-autocomplete_results';
  var SELECTED_CLASS = 'm-autocomplete_selected';

  // Key constants
  var ENTER = 13;
  var UP = 38;
  var DOWN = 40;
  var ESCAPE = 27;

  // Internal variables
  var _autocomplete;
  var _data = [];
  var _suggestions;
  var _isVisible;
  var _selection;

  // Autocomplete elements
  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _input = _dom.querySelector( 'input' );

  // Settings
  var _settings = {
    minChars: 2,
    delay: 300,
    url: '',
    list: [],
    onSubmit: function( event, selected ) {
      return selected;
    },
    renderItem: function ( item ) {
      var li = document.createElement( 'li' );
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
  var _xhr;
  var _searchTerm = '';
  var _throttleFetch = throttle( function() {
    _fetchSuggestions();
  }, _settings.delay );

  assign( _settings, opts );

  /**
   * Set up and create the autocomplete.
   * @returns {Autocomplete|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
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
    var ul = document.createElement( 'ul' );
    ul.className = AUTOCOMPLETE_CLASS + ' ' + HIDDEN_CLASS;
    document.body.appendChild( ul );
    return ul;
  }

  /**
   * Updates dimensions and position of autocomplete container
   * relative to _input element.
   */
  function _positionContainer() {
    var inputCoords = _input.getBoundingClientRect();
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
    bindEvent( _input, {
      input: function() {
        _searchTerm = this.value;
        if ( _searchTerm.length >= _settings.minChars ) {
          if ( _settings.url ) {
            _throttleFetch();
          } else {
            _settings.filterList( _settings.list );
          }
        } else {
          _hide();
        }
      },
      blur: function() {
        setTimeout( function() {
          var active = document.activeElement;
          if ( active !== _autocomplete && !_autocomplete.contains( active ) ) {
            _hide();
          }
        }, 1 );
      },
      keydown: function( event ) {
        var key = event.keyCode;
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
      }
    } );

    bindEvent( window, {
      resize: function() {
        _positionContainer();
      }
    } );

    bindEvent( _autocomplete, {
      mousedown: function( event ) {
        event.preventDefault();
      }
    } );
  }

  /**
   * Replaces autocomplete content with suggestions
   * markup for each item in _data array.
   */
  function _updateSuggestions() {
    _reset();
    _data.forEach( function( item, index ) {
      var suggestion = _settings.renderItem( item );
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
    var length = _suggestions.length - 1;
    var index = _selection >= length ? 0 : _selection + 1;
    _updateSelection( index );
  }

  /**
   * Gets previous item in suggestions list and
   * uses it to update current selection.
   */
  function _prev() {
    var index = _selection > 0 ? _selection - 1 : _suggestions.length - 1;
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
    var item = _suggestions[index];

    _input.value = item.getAttribute( 'data-val' );
    item.classList.add( SELECTED_CLASS );
    _scrollSelectionIntoView();
  }

  /**
   * Scrolls autocomplete suggestions list so current
   * selection is visible.
   */
  function _scrollSelectionIntoView() {
    var _target = _suggestions[_selection];
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
    _xhr = ajaxRequest( 'GET', _settings.url + _settings.cleanQuery( _searchTerm ), {
      success: _success,
      fail: _fail
    } );
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

module.exports = Autocomplete;
