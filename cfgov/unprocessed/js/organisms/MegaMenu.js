'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var breakpointState = require( '../modules/util/breakpoint-state' );
var dataHook = require( '../modules/util/data-hook' );
var EventObserver = require( '../modules/util/EventObserver' );
var FlyoutMenu = require( '../modules/FlyoutMenu' );
var MegaMenuDesktop = require( '../organisms/MegaMenuDesktop' );
var MegaMenuMobile = require( '../organisms/MegaMenuMobile' );
var MoveTransition = require( '../modules/transition/MoveTransition' );
var Tree = require( '../modules/Tree' );

/**
 * MegaMenu
 * @class
 *
 * @classdesc Initializes a new MegaMenu organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {MegaMenu} An instance.
 */
function MegaMenu( element ) {
  var BASE_CLASS = 'o-mega-menu';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS, 'MegaMenu' );

  // Tree data model.
  var _menus;

  // Screen-size specific behaviors.
  var _desktopNav;
  var _mobileNav;

  // TODO: Move tab trigger to its own class.
  var _tabTriggerDom = _dom.querySelector( '.' + BASE_CLASS + '_tab-trigger' );

  var KEY_TAB = 9;

  /**
   * @returns {MegaMenu} An instance.
   */
  function init() {
    // DOM selectors.
    var rootMenuDom = _dom;
    var rootContentDom = rootMenuDom.querySelector( FlyoutMenu.CONTENT_SEL );

    // Create model.
    _menus = new Tree();

    // Create root menu.
    var transition = new MoveTransition( rootContentDom ).init();
    var rootMenu = new FlyoutMenu( rootMenuDom ).init();
    // Set initial position.
    rootMenu.setExpandTransition( transition, transition.moveToOrigin );
    rootMenu.setCollapseTransition( transition, transition.moveLeft );
    _addEvents( rootMenu );

    // Populate tree model with menus.
    var rootNode = _menus.init( rootMenu ).getRoot();
    rootMenu.setData( rootNode );
    _populateTreeFromDom( rootMenuDom, rootNode, _addMenu );

    // Initialize screen-size specific behaviors.
    _desktopNav = new MegaMenuDesktop( _menus ).init();
    _mobileNav = new MegaMenuMobile( _menus ).init();
    _mobileNav.addEventListener( 'rootExpandBegin',
                                 _handleRootExpandBegin.bind( this ) );
    _mobileNav.addEventListener( 'rootCollapseEnd',
                                 _handleRootCollapseEnd.bind( this ) );

    window.addEventListener( 'resize', _resizeHandler );

    if ( _isInDesktop() ) {
      _desktopNav.resume();
    } else {
      _mobileNav.resume();
    }

    _dom.classList.remove( 'u-hidden' );

    _tabTriggerDom.addEventListener( 'keyup', _handleTabPress );

    return this;
  }

  /**
   * Perform a recursive depth-first search of the DOM
   * and call a function for each node.
   * @param {HTMLNode} dom - A DOM element to search from.
   * @param {TreeNode} parentNode
   *   Node in a tree from which to attach new nodes.
   * @param {Function} callback - Function to call on each node.
   *   Must return a TreeNode.
   */
  function _populateTreeFromDom( dom, parentNode, callback ) {
    var children = dom.children;
    var child;
    for ( var i = 0, len = children.length; i < len; i++ ) {
      var newParentNode = parentNode;
      child = children[i];
      newParentNode = callback.call( this, child, newParentNode );
      _populateTreeFromDom( child, newParentNode, callback );
    }
  }

  /**
   * Create a new FlyoutMenu and attach it to a new tree node.
   * @param {HTMLNode} dom
   *   A DOM element to check for a js data-* attribute hook.
   * @param {TreeNode} parentNode
   *   The parent node in a tree on which to attach a new menu.
   * @returns {TreeNode} Return the processed tree node.
   */
  function _addMenu( dom, parentNode ) {
    var newParentNode = parentNode;
    var transition;
    if ( dataHook.contains( dom, FlyoutMenu.BASE_CLASS ) ) {
      var menu = new FlyoutMenu( dom ).init();
      transition = new MoveTransition( menu.getDom().content ).init();
      menu.setExpandTransition( transition, transition.moveToOrigin );
      menu.setCollapseTransition( transition, transition.moveLeft );
      _addEvents( menu );
      newParentNode = newParentNode.tree.add( menu, newParentNode );
      menu.setData( newParentNode );
    }

    return newParentNode;
  }

  /**
   * @param {FlyoutMenu} menu - a menu on which to attach events.
   */
  function _addEvents( menu ) {
    menu.addEventListener( 'triggerOver', _handleEvent );
    menu.addEventListener( 'triggerClick', _handleEvent );
    menu.addEventListener( 'expandBegin', _handleEvent );
    menu.addEventListener( 'expandEnd', _handleEvent );
    menu.addEventListener( 'collapseBegin', _handleEvent );
    menu.addEventListener( 'collapseEnd', _handleEvent );
  }

  /**
   * Handle events coming from menu,
   * and pass it to the desktop or mobile behaviors.
   * @param {Object} event - A FlyoutMenu event object.
   */
  function _handleEvent( event ) {
    var activeNav = _isInDesktop() ? _desktopNav : _mobileNav;
    activeNav.handleEvent( event );
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if ( _isInDesktop() ) {
      _mobileNav.suspend();
      _desktopNav.resume();
    } else {
      _desktopNav.suspend();
      _mobileNav.resume();
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
   * Close the mega menu.
   * @returns {MegaMenu} An instance.
   */
  function collapse() {
    if ( !_isInDesktop() ) {
      _mobileNav.collapse();
    }

    return this;
  }

  /**
   * Event handler for when root menu expand transition begins.
   */
  function _handleRootExpandBegin() {
    this.dispatchEvent( 'rootExpandBegin', { target: this } );
  }

  /**
   * Event handler for when root menu collapse transition ends.
   */
  function _handleRootCollapseEnd() {
    this.dispatchEvent( 'rootCollapseEnd', { target: this } );
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.collapse = collapse;

  return this;
}

module.exports = MegaMenu;
