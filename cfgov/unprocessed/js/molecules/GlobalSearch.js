'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../modules/polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var breakpointState = require( '../modules/util/breakpoint-state' );
var ClearableInput = require( '../modules/ClearableInput' );
var EventObserver = require( '../modules/util/EventObserver' );
var FlyoutMenu = require( '../modules/FlyoutMenu' );

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
function GlobalSearch( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

  var BASE_CLASS = 'm-global-search';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'GlobalSearch' );
  var _triggerSel = '.' + BASE_CLASS + '_trigger';
  var _triggerDom = _dom.querySelector( _triggerSel );
  var _flyoutMenu =
    new FlyoutMenu( _dom, _triggerSel, '.' + BASE_CLASS + '_content' ).init();
  var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  var _searchInputDom;
  var _searchBtnDom;
  var _clearBtnDom;

  // TODO: Move tab trigger to its own class.
  var _tabTriggerDom =
    _contentDom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

  var KEY_TAB = 9;

  /**
   * @returns {Object} The GlobalSearch instance.
   */
  function init() {
    var clearBtnSel = '.' + BASE_CLASS + ' .input-contains-label_after__clear';
    var inputContainsLabelSel =
      '.' + BASE_CLASS + '_content-form .input-contains-label';
    var searchBtnSel = '.' + BASE_CLASS + ' .input-with-btn_btn button';

    _clearBtnDom = _contentDom.querySelector( clearBtnSel );
    var inputContainsLabel = _contentDom.querySelector( inputContainsLabelSel );
    _searchInputDom = inputContainsLabel.querySelector( 'input' );
    _searchBtnDom = _contentDom.querySelector( searchBtnSel );

    // Initialize new clearable input behavior on the input-contains-label.
    var clearableInput = new ClearableInput( inputContainsLabel );
    clearableInput.init();

    _flyoutMenu.addEventListener( 'toggle',
                                  _handleToggle.bind( this ) );
    _flyoutMenu.addEventListener( 'expandBegin', _handleExpandBegin );
    _flyoutMenu.addEventListener( 'collapseBegin', _handleCollapseBegin );
    _flyoutMenu.addEventListener( 'collapseEnd', _handleCollapseEnd );

    _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

    // Set initial collapse state.
    _handleCollapseEnd();

    return this;
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event The event object for the mousedown event.
   */
  function _handleBodyClick( event ) {
    var target = event.target;

    var isInDesktop = _isInDesktop();
    if ( isInDesktop && !_isDesktopTarget( target ) ||
         !isInDesktop && !_isMobileTarget( target ) ) {
      collapse();
    }
  }

  // TODO: Move this to breakpoint-state.js.
  /**
   * Whether currently in the desktop view.
   * @returns {boolean} True if in the desktop view, otherwise false.
   */
  function _isInDesktop() {
    var isInDesktop = false;
    var currentBreakpoint = breakpointState.get();
    if ( currentBreakpoint.isBpMED ||
         currentBreakpoint.isBpLG ||
         currentBreakpoint.isBpXL ) {
      isInDesktop = true;
    }
    return isInDesktop;
  }

  /**
   * Whether a target is one of the ones that appear in the desktop view.
   * @param {HTMLNode} target - The target of a mouse event (most likely).
   * @returns {boolean} True if the passed target is in the desktop view.
   */
  function _isDesktopTarget( target ) {
    return target === _searchInputDom ||
           target === _searchBtnDom ||
           target === _clearBtnDom;
  }

  /**
   * Whether a target is one of the ones that appear in the mobile view.
   * @param {HTMLNode} target - The target of a mouse event (most likely).
   * @returns {boolean} True if the passed target is in the mobile view.
   */
  function _isMobileTarget( target ) {
    return _dom.contains( target );
  }

  /**
   * Event handler for when the tab key is pressed.
   * @param {KeyboardEvent} event
   *   The event object for the keyboard key press.
   */
  function _handleTabPress( event ) {
    if ( event.keyCode === KEY_TAB ) {
      collapse();
    }
  }

  /**
   * Event handler for when the search input flyout is toggled,
   * which opens/closes the search input.
   */
  function _handleToggle() {
    this.dispatchEvent( 'toggle', { target: this } );
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandBegin actions.
   */
  function _handleExpandBegin() {
    if ( _isInDesktop() ) { _triggerDom.classList.add( 'u-hidden' ); }
    _contentDom.classList.remove( 'u-invisible' );
    _searchInputDom.select();

    document.body.addEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition begins.
   * Use this to perform post-collapseBegin actions.
   */
  function _handleCollapseBegin() {
    _triggerDom.classList.remove( 'u-hidden' );
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition ends.
   * Use this to perform post-collapseEnd actions.
   */
  function _handleCollapseEnd() {
    // TODO: When tabbing is used to collapse the search flyout
    //       it will not animate with the below line.
    //       Investigate why this is the case for tab key
    //       but not with mouse clicks.
    _contentDom.classList.add( 'u-invisible' );
  }

  /**
   * Open the search box.
   * @returns {Object} An GlobalSearch instance.
   */
  function expand() {
    _flyoutMenu.expand();

    return this;
  }

  /**
   * Close the search box.
   * @returns {Object} An GlobalSearch instance.
   */
  function collapse() {
    _flyoutMenu.collapse();

    return this;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.expand = expand;
  this.collapse = collapse;

  return this;
}

module.exports = GlobalSearch;
