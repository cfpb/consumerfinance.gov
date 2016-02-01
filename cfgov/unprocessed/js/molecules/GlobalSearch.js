'use strict';

// Required polyfills for <IE9.
require( '../modules/polyfill/query-selector' );
require( '../modules/polyfill/event-listener' );
require( '../modules/polyfill/class-list' );

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var breakpointState = require( '../modules/util/breakpoint-state' );

/**
 * GlobalSearch
 * @class
 *
 * @classdesc Initializes a new GlobalSearch molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Object} An GlobalSearch instance.
 */
function GlobalSearch( element ) {

  var BASE_CLASS = 'm-global-search';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'GlobalSearch' );
  var _triggerDom = _dom.querySelector( '.' + BASE_CLASS + '_trigger' );
  var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  var _searchInputDom;
  var _clearBtnDom;

  var _isExpanded = false;
  var _tabPressed = false;

  var KEY_TAB = 9;

  /**
   * @returns {Object} The GlobalSearch instance.
   */
  function init() {
    var inputSelector = '.' + BASE_CLASS + '_content-form input';
    var clearBtnSelector =
      '.' + BASE_CLASS + ' .input-contains-label_after__clear';
    var searchIconSelector =
      '.' + BASE_CLASS + ' .input-contains-label_before__search';
    var searchBtnSelector = '.' + BASE_CLASS + ' .input-with-btn_btn button';

    _searchInputDom = _contentDom.querySelector( inputSelector );
    var searchIconDom = _contentDom.querySelector( searchIconSelector );
    var searchBtnDom = _contentDom.querySelector( searchBtnSelector );
    _clearBtnDom = _contentDom.querySelector( clearBtnSelector );

    _triggerDom.addEventListener( 'click', _triggerClicked );
    _clearBtnDom.addEventListener( 'mousedown', _clearClicked );
    _searchInputDom.addEventListener( 'keyup', _inputTyped );
    _searchInputDom.addEventListener( 'blur', _searchBlurred );
    searchBtnDom.addEventListener( 'mousedown', _searchBtnClicked );
    searchIconDom.addEventListener( 'click', _searchIconClicked );

    _contentDom.addEventListener( 'keydown', _handleTabPress );

    _setClearBtnState( _searchInputDom.value );

    return this;
  }

  /**
   * Event handler for when the keyboard is pressed on the HTML document body.
   * If the tab key was pressed, record the press so that when
   * getting to the search input, the input won't collapse when
   * tabbing between the input and the search button.
   * @param {KeyboardEvent} event The event object for the keyboard key press.
   */
  function _handleTabPress( event ) {
    if ( event.keyCode === KEY_TAB ) {
      _tabPressed = true;
    }
  }

  /**
   * Event handler for when the search icon is clicked in the
   * expanded state at desktop sizes. Closes the search box.
   */
  function _searchIconClicked() {
    _collapseIfDesktop();
  }

  /**
   * Force a click on the search button after it has been clicked.
   * This is necessary to handle the button before the search input blurs.
   * @param {MouseEvent} event The event object for mousedown event.
   */
  function _searchBtnClicked( event ) {
    event.target.click();
  }

  /**
   * Event handler for when the search input loses focus.
   * Closes the search input if the tab key was not pressed.
   */
  function _searchBlurred() {
    if ( !_tabPressed ) {
      _collapseIfDesktop();
    } else {
      _tabPressed = false;
    }
  }

  /**
   * Collapse the search box if screen is at desktop sizes.
   */
  function _collapseIfDesktop() {
    var currentBreakpoint = breakpointState.get();
    if ( ( currentBreakpoint.isBpMED ||
         currentBreakpoint.isBpLG ||
         currentBreakpoint.isBpXL ) ) {
      collapse();
    }
  }

  /**
   * Event handler for when the search input trigger is clicked,
   * which opens/closes the search input.
   */
  function _triggerClicked() {
    if ( _isExpanded ) {
      collapse();
    } else {
      expand();
    }
  }

  /**
   * Open the search box.
   * @returns {Object} An GlobalSearch instance.
   */
  function expand() {
    if ( !_isExpanded ) {
      _isExpanded = true;
      _triggerDom.setAttribute( 'aria-expanded', 'true' );
      _contentDom.setAttribute( 'aria-expanded', 'true' );
      _searchInputDom.select();
    }

    return this;
  }

  /**
   * Close the search box.
   * @returns {Object} An GlobalSearch instance.
   */
  function collapse() {
    if ( _isExpanded ) {
      _isExpanded = false;
      _triggerDom.setAttribute( 'aria-expanded', 'false' );
      _contentDom.setAttribute( 'aria-expanded', 'false' );
    }

    return this;
  }

  /**
   * Event handler for when the clear input label was clicked.
   * @param {MouseEvent} event The event object for the mousedown event.
   */
  function _clearClicked( event ) {
    _searchInputDom.value = _setClearBtnState( '' );
    _searchInputDom.focus();

    // Prevent event bubbling up to the input,
    // which would blur and trigger a collapse otherwise.
    event.preventDefault();
  }

  /**
   * Event handler for when the user typed in the input.
   */
  function _inputTyped() {
    _setClearBtnState( _searchInputDom.value );
  }

  /**
   * @param {string} value - The input value in the search box.
   * @returns {string} The input value in the search box.
   */
  function _setClearBtnState( value ) {
    if ( value !== '' ) {
      _showClearBtn();
    } else {
      _hideClearBtn();
    }

    return value;
  }

  /**
   * Add a hidden class to the input search label.
   * Used when there is no text input.
   */
  function _hideClearBtn() {
    _clearBtnDom.classList.add( 'u-hidden' );
  }

  /**
   * Remove a hidden class from the input search label.
   * Used when there is text input.
   */
  function _showClearBtn() {
    _clearBtnDom.classList.remove( 'u-hidden' );
  }

  this.init = init;
  this.expand = expand;
  this.collapse = collapse;
  return this;
}

module.exports = GlobalSearch;
