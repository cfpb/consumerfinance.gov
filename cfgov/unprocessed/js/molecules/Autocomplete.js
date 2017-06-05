'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var throttle = require( '../modules/util/email-popup-helpers' ).throttle;
var ajaxRequest = require( '../modules/util/ajax-request' ).ajaxRequest;
var assign = require( '../modules/util/assign' ).assign;
var EventObserver = require( '../modules/util/EventObserver' );

/**
 * Autocomplete
 * @class
 *
 * @classdesc Initializes the molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @param {string} baseClass class of molecule
 * @param {Object} opts optional params, including

 * @returns {Autocomplete} An instance.
 */

function Autocomplete( element, opts ) {
  opts || ( opts = {} );

  var _minChars = 2;

  var BASE_CLASS = 'm-autocomplete';
  var HIDDEN_CLASS = 'u-hidden';
  var AUTOCOMPLETE_CLASS = 'm-autocomplete_results';
  var SELECTED_CLASS = 'm-autocomplete_selected';

  var ENTER = 13;
  var UP = 38;
  var DOWN = 40;
  var ESCAPE = 27;

  var _source = [];

  var _xhr;
  var _autocomplete;
  var _items;
  var _isVisible;
  var _selection;
  var _searchTerm = '';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _input = _dom.querySelector( 'input' );

  var _throttleFetch = throttle( function( event ) {
    _fetch();
  }, 400 );


  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    _autocomplete = _addContainer();
    _positionContainer();
    _input.setAttribute('autocomplete', 'off');
    _input.setAttribute('aria-autocomplete', 'list');

    _input.addEventListener( 'keydown', _keydownHandler );
    _input.addEventListener( 'input', _inputHandler );
    _input.addEventListener( 'blur', _hide );
    window.addEventListener( 'resize', _positionContainer );
  }

  function _addContainer() {
    var ul = document.createElement( 'ul' );
    ul.className = AUTOCOMPLETE_CLASS;
    ul.classList.add( HIDDEN_CLASS );
    document.body.appendChild( ul );
    return ul;
  }

  function _positionContainer() {
    var inputCoords = _input.getBoundingClientRect();
    _autocomplete.style.left = Math.round( inputCoords.left + window.pageXOffset ) + 'px';
    _autocomplete.style.top = Math.round( inputCoords.bottom + window.pageYOffset ) + 'px';
    _autocomplete.style.width = Math.round( inputCoords.right - inputCoords.left ) + 'px';
  }

  function _update() {
    _reset();
    _source.forEach(function( res, index ) {
        var item = _renderItem( res, index );
        _items.push( item );
        _autocomplete.appendChild( item );
    });
    if ( _items.length ) {
        _show();
    } else {
        _hide();
    }
  }

  function _reset() {
    _selection = -1;
    _items = [];
    _autocomplete.innerHTML = '';
  }

  function _renderItem( item, index ) {
    var li = document.createElement( 'li' );
    li.setAttribute( 'data-val', item.value );
    li.setAttribute( 'role', 'option' );
    li.setAttribute( 'id', 'autocomplete-' + index );

    var link = document.createElement( 'a' );
    link.setAttribute( 'href', item.url );
    link.innerText = item.value;
    li.appendChild( link );
    return li;
  }

  function _fetch() {
    if ( _xhr ) {
        _xhr.abort()
    }
    _xhr = ajaxRequest( 'GET', opts.url + _cleanQuery( _searchTerm ), {
        success: _success,
        fail: _fail
    } );
  }

  function _success() {
    try {
        _source = JSON.parse( _xhr.responseText );
        _update();
    } catch ( err ) {
        _fail();
    }
    _xhr = null;
  }

  function _fail() {
    _source = [];
    _reset();
    _hide();
  }

  function _hide() {
    _isVisible = false;
    _autocomplete.classList.add( HIDDEN_CLASS );
  }

  function _show() {
    _isVisible = true;
    _autocomplete.classList.remove( HIDDEN_CLASS );
  }

  function _keydownHandler(event) {
    var key = event.keyCode;
    if ( _isVisible ) {
        if ( key === UP ) {
            _prev( event );
        } else if ( key === DOWN ) {
            _next( event );
        } else if ( key === ENTER && _selection > -1 ) {
            event.preventDefault(); 
            _submit( event );
        } else if ( key === ESCAPE ) {
            event.preventDefault();
            _hide();
        }
    }
  }
  function _inputHandler(event) {
    _searchTerm = _input.value;

    if ( _searchTerm.length >= _minChars ) {
        if ( opts.url ) {
            _throttleFetch();
        }
    } else {
        _hide();
    }
  }

  function _next() {
    var length = _items.length - 1;
    var index = _selection >= length ? 0 : _selection + 1;
    _select( index );
  }

  function _prev() {
    var index = _selection > 0 ? _selection - 1 : _items.length - 1 ;
    _select( index );
  }

  function _select( index ) {
    if ( _selection > -1 ) {
        _items[_selection].classList.remove( SELECTED_CLASS );
    }
    _selection = index;
    var item = _items[index];

    _input.value = item.getAttribute( 'data-val' );
    item.classList.add( SELECTED_CLASS );
    _scroll();
  }

  function _scroll() {
    var _target = _items[_selection];
    _autocomplete.scrollTop = _target.offsetTop - _autocomplete.clientHeight + _target.clientHeight;
  }

  function _submit(e) {
    var item = _items[_selection];
    var link = item.querySelector( 'a' );
    document.location = link.pathname;
  }

  function destroy() {
    _inputContainer.removeChild( _autocomplete );
    _input.removeAttribute( 'autocomplete' );
    _input.removeAttribute( 'aria-autocomplete' );
    _input.removeEventListener( 'keydown', _keydownHandler );
    _input.removeEventListener( 'input', _inputHandler );
    _input.removeEventListener( 'blur', _hide );
    window.removeEventListener( 'resize', _positionContainer );
  }

  function _cleanQuery(query) {
    query = query.replace(/[\u0080-\uffff]/g, '');
    query = query.replace(/[“”‘’]/g,'');
    return query;
  }

  this.init = init;
  this.destroy = destroy;
    
  return this;
}

module.exports = Autocomplete;