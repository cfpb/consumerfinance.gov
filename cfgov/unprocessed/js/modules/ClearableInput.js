'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../modules/polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );

/**
 * ClearableInput
 * @class
 *
 * @classdesc Initializes a new ClearableInput molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Object} A ClearableInput instance.
 */
function ClearableInput( element ) {
  var BASE_CLASS = 'input-contains-label';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'ClearableInput' );
  var _inputDom = _dom.querySelector( 'input' );
  var _clearBtnDom = _dom.querySelector( '.' + BASE_CLASS + '_after__clear' );

  var _isClearShowing = true;

  /**
   * @returns {Object} The ClearableInput instance.
   */
  function init() {
    _clearBtnDom.addEventListener( 'mousedown', _clearClicked );
    _inputDom.addEventListener( 'keyup', _inputTyped );

    _setClearBtnState( _inputDom.value );

    return this;
  }

  /**
   * Event handler for when the clear input label was clicked.
   * @param {MouseEvent} event - The event object for the mousedown event.
   */
  function _clearClicked( event ) {
    _inputDom.value = _setClearBtnState( '' );
    _inputDom.focus();

    // Prevent event bubbling up to the input, which would blur otherwise.
    event.preventDefault();
  }

  /**
   * Event handler for when the user typed in the input.
   */
  function _inputTyped() {
    _setClearBtnState( _inputDom.value );
  }

  /**
   * @param {string} value - The input value in the search box.
   * @returns {string} The input value in the search box.
   */
  function _setClearBtnState( value ) {
    if ( _isClearShowing && value === '' ) {
      _hideClearBtn();
    } else if ( !_isClearShowing ) {
      _showClearBtn();
    }
    return value;
  }

  /**
   * Add a hidden class to the input search label.
   * Used when there is no text input.
   */
  function _hideClearBtn() {
    _clearBtnDom.classList.add( 'u-hidden' );
    _isClearShowing = false;
  }

  /**
   * Remove a hidden class from the input search label.
   * Used when there is text input.
   */
  function _showClearBtn() {
    _clearBtnDom.classList.remove( 'u-hidden' );
    _isClearShowing = true;
  }

  this.init = init;

  return this;
}

module.exports = ClearableInput;
