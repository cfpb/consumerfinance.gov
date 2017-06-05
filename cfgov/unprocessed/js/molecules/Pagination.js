'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var standardType = require( '../modules/util/standard-type' );
var EventObserver = require( '../modules/util/EventObserver' );
var assign = require( '../modules/util/assign' ).assign;

/**
 * Pagination
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Pagination} An instance.
 */
function Pagination( element, currentPage, pageCount ) {
  var BASE_CLASS = 'm-pagination';
  var HIDDEN_CLASS = 'hidden';
  var DISABLED_CLASS = 'btn__disabled';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _nextBtn = _dom.querySelector( '.m-pagination_btn-next' );
  var _prevBtn = _dom.querySelector( '.m-pagination_btn-prev' );
  var _formElement = _dom.querySelector( 'form' );
  var _pageCountElement = _formElement.querySelector( '.m-pagination_page-count' );
  var _currentPageInput = _formElement.querySelector( '.m-pagination_current-page' );

  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  var _instance;
  var _state = {
    currentPage: 0,
    pageCount: 0
  }

  /**
   * @returns {Pagination|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }
    _state.currentPage = parseInt( _currentPageInput.value ) || 1;
    _state.pageCount = parseInt( _pageCountElement.innerHTML ) || 1;

    _instance = this;
    _instance.addEventListener( 'updatePagination', _updateState );
    _nextBtn.addEventListener( 'click', _next );
    _prevBtn.addEventListener( 'click', _prev );
    _formElement.addEventListener( 'submit', _submit );
   
    return this;
  }
  
  function _next( e ) {
    e.preventDefault();
    _updatePage( _state.currentPage + 1 );
  }
  
  function _prev( e ) {
    e.preventDefault();
    _updatePage( _state.currentPage - 1 );
  }
  
  function _submit( e ) {
    e.preventDefault();
    _updatePage( _currentPageInput.value );
  }
  
  function _updatePage( page ) {
    if ( page > 0 && page <= _state.pageCount ) {
      _updateState( {currentPage: page} );
      _instance.dispatchEvent( 'updatePage', _state );
    }
  }
  
  function _updateState( obj ) {
    if (obj && typeof obj === 'object') {
      assign( _state, obj );
      _updateDOM();
    }
  }

  function _toggleClass( el, className, on ) {
  	if ( on ) {
  		el.classList.add( className );
  	} else {
  		el.classList.remove( className );
  	}
  }
  
  function _updateDOM() {
    if ( _state.pageCount < 2 ) {
    	_toggleClass( _dom, HIDDEN_CLASS, true );
    } else {
      _currentPageInput.value = _state.currentPage;
      _pageCountElement.innerHTML = _state.pageCount;
      _toggleClass( _nextBtn, DISABLED_CLASS, _state.currentPage >= _state.pageCount );
      _toggleClass( _prevBtn, DISABLED_CLASS, _state.currentPage <= 1 );
      _toggleClass( _dom, HIDDEN_CLASS, false );
    }
  }
  
  this.init = init;
  
  return this;
}

module.exports = Pagination;