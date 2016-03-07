'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var breakpointState = require( '../modules/util/breakpoint-state' );
var EventObserver = require( '../modules/util/EventObserver' );
var FlyoutMenu = require( '../modules/FlyoutMenu' );

/**
 * MegaMenu
 * @class
 *
 * @classdesc Initializes a new MegaMenu organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Object} An MegaMenu instance.
 */
function MegaMenu( element ) {
  var BASE_CLASS = 'o-mega-menu';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'MegaMenu' );
  var _flyoutMenu = new FlyoutMenu( _dom ).init();
  var _activeMenu = _flyoutMenu;
  var _activeMenuDom = _flyoutMenu.getDom().content;
  var _menuItems = _dom.querySelectorAll( '.' + BASE_CLASS + '_content-item' );
  var _subMenus = {};

  // TODO: Move tab trigger to its own class.
  var _tabTriggerDom = _dom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

  var KEY_TAB = 9;

  /**
   * @returns {Object} The MegaMenu instance.
   */
  function init() {
    var initEventsBinded = _initEvents.bind( this );
    var menuItem;
    var submenu;
    var childSel = '.' + BASE_CLASS + '_content-link__has-children';
    for ( var i = 1, len = _menuItems.length; i < len; i++ ) {
      menuItem = _menuItems[i];
      if ( menuItem.querySelector( '.u-link__disabled' ) === null &&
           menuItem.querySelector( childSel ) !== null ) {
        submenu =
          new FlyoutMenu( menuItem ).init();
        _subMenus[menuItem] = submenu;
        initEventsBinded( submenu );
      }
    }

    initEventsBinded( _flyoutMenu );
    _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

    return this;
  }

  /**
   * @param {FlyoutMenu} menu - The FlyoutMenu to add event listeners to.
   */
  function _initEvents( menu ) {
    menu.addEventListener( 'expandBegin', _handleExpandBegin.bind( this ) );
    menu.addEventListener( 'collapseBegin', _handleCollapseBegin );
    menu.addEventListener( 'collapseEnd', _handleCollapseEnd.bind( this ) );
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event The event object for the mousedown event.
   */
  function _handleBodyClick( event ) {
    var target = event.target;
    if ( _activeMenu.getDom().trigger === target ) {
      return;
    }

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
    return _activeMenuDom.contains( target );
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
   * Open the mega menu.
   * @returns {Object} A MegaMenu instance.
   */
  function expand() {
    _activeMenu.expand();

    return this;
  }

  /**
   * Close the mega menu.
   * @returns {Object} A MegaMenu instance.
   */
  function collapse() {
    _flyoutMenu.collapse();
    _activeMenu.collapse();

    return this;
  }

  /**
   * Event handler for when the search input flyout is toggled,
   * which opens/closes the search input.
   * @param {FlyoutMenu} target - menu that is expanding or collapsing.
   */
  function _handleToggle( target ) {
    if ( target === _flyoutMenu &&
         _activeMenu !== target ) {
      _activeMenu.collapse();
    }
    _activeMenu = target;
    _activeMenuDom = _activeMenu.getDom().content;
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleExpandBegin( event ) {
    var target = event.target;
    _handleToggle( target );
    if ( target === _flyoutMenu ) {
      this.dispatchEvent( 'rootExpandBegin', { target: this } );
    }
    // If on a submenu, focus the back button, otherwise focus the first link.
    var firstMenuLink;
    if ( _activeMenu === _flyoutMenu ) {
      firstMenuLink = _activeMenuDom.querySelector( 'a' );
    } else {
      firstMenuLink = _activeMenuDom.querySelector( 'button' );
    }

    firstMenuLink.focus();
    document.body.addEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition begins.
   * Use this to perform post-collapseBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseBegin( event ) {
    _handleToggle( event.target );
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition ends.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd( event ) {
    if ( event.target === _flyoutMenu ) {
      this.dispatchEvent( 'rootCollapseEnd', { target: this } );
    }
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
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

module.exports = MegaMenu;
