// Required modules.
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const breakpointState = require( '../modules/util/breakpoint-state' );
const ClearableInput = require( '../modules/ClearableInput' );
const EventObserver = require( '../modules/util/EventObserver' );
const FlyoutMenu = require( '../modules/behavior/FlyoutMenu' );
const fnBind = require( '../modules/util/fn-bind' ).fnBind;
const MoveTransition = require( '../modules/transition/MoveTransition' );
const standardType = require( '../modules/util/standard-type' );

/**
 * GlobalSearch
 * @class
 *
 * @classdesc Initializes a new GlobalSearch molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {GlobalSearch} An instance.
 */
function GlobalSearch( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

  const BASE_CLASS = 'm-global-search';
  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  const _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  const _flyoutMenu = new FlyoutMenu( _dom );
  let _searchInputDom;
  let _searchBtnDom;
  let _clearBtnDom;

  // TODO: Move tab trigger to its own class.
  const _tabTriggerDom =
    _contentDom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

  const KEY_TAB = 9;

  /**
   * @returns {GlobalSearch|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // Set initial appearance.
    const transition = new MoveTransition( _contentDom ).init();
    transition.moveRight();
    _flyoutMenu.setExpandTransition( transition, transition.moveToOrigin );
    _flyoutMenu.setCollapseTransition( transition, transition.moveRight );
    _flyoutMenu.init();

    _contentDom.classList.remove( 'u-hidden' );

    const clearBtnSel =
      '.' + BASE_CLASS + ' .input-contains-label_after__clear';
    const inputContainsLabelSel =
      '.' + BASE_CLASS + '_content-form .input-contains-label';
    const searchBtnSel =
      '.' + BASE_CLASS + ' .o-form__input-w-btn_btn-container button';

    _clearBtnDom = _contentDom.querySelector( clearBtnSel );
    const inputContainsLabel =
      _contentDom.querySelector( inputContainsLabelSel );
    _searchInputDom = inputContainsLabel.querySelector( 'input' );
    _searchBtnDom = _contentDom.querySelector( searchBtnSel );

    // Initialize new clearable input behavior on the input-contains-label.
    const clearableInput = new ClearableInput( inputContainsLabel );
    clearableInput.init();
    const handleExpandBeginBinded = fnBind( _handleExpandBegin, this );
    _flyoutMenu.addEventListener( 'expandBegin', handleExpandBeginBinded );
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
    const target = event.target;

    const isInDesktop = breakpointState.isInDesktop();
    if ( isInDesktop && !_isDesktopTarget( target ) ||
         !isInDesktop && !_isMobileTarget( target ) ) {
      collapse();
    }
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
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandBegin actions.
   */
  function _handleExpandBegin() {
    this.dispatchEvent( 'expandBegin', { target: this } );

    /* TODO: Remove when Android 4.0-4.4 support is dropped.
       Hack to fix reflow issues on legacy Android devices. */
    _contentDom.style.display = 'none';
    // eslint-disable-next-line no-unused-expressions
    _contentDom.offsetHeight;
    _contentDom.style.display = '';

    _contentDom.classList.remove( 'u-invisible' );

    _searchInputDom.select();

    document.body.addEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition begins.
   * Use this to perform post-collapseBegin actions.
   */
  function _handleCollapseBegin() {
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition ends.
   * Use this to perform post-collapseEnd actions.
   */
  function _handleCollapseEnd() {

    /* TODO: When tabbing is used to collapse the search flyout
       it will not animate with the below line.
       Investigate why this is the case for tab key
       but not with mouse clicks. */
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
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.expand = expand;
  this.collapse = collapse;

  return this;
}

module.exports = GlobalSearch;
