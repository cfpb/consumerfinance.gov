// Required modules.
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const breakpointState = require( '../modules/util/breakpoint-state' );
const dataHook = require( '../modules/util/data-hook' );
const EventObserver = require( '../modules/util/EventObserver' );
const FlyoutMenu = require( '../modules/behavior/FlyoutMenu' );
const MegaMenuDesktop = require( '../organisms/MegaMenuDesktop' );
const MegaMenuMobile = require( '../organisms/MegaMenuMobile' );
const MoveTransition = require( '../modules/transition/MoveTransition' );
const TabTrigger = require( '../modules/TabTrigger' );
const TreeDomModel = require( '../modules/TreeDomModel' );
const standardType = require( '../modules/util/standard-type' );

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
  const BASE_CLASS = 'o-mega-menu';

  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  // Tree data model.
  let _model;

  // Screen-size specific behaviors.
  let _desktopNav;
  let _mobileNav;

  /* The tab trigger adds an element to the end of the element that handles
     cleanup after tabbing out of the element. */
  const _tabTrigger = new TabTrigger( _dom );

  /**
   * @returns {MegaMenu|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // DOM selectors.
    const rootMenuDom = _dom;
    const rootContentDom = rootMenuDom.querySelector( '.' + BASE_CLASS + '_content' );

    // Create root menu.
    const transition = new MoveTransition( rootContentDom ).init();
    const rootMenu = new FlyoutMenu( rootMenuDom ).init();
    // Set initial position.
    rootMenu.setExpandTransition( transition, transition.moveToOrigin );
    rootMenu.setCollapseTransition( transition, transition.moveLeft );
    _addEvents( rootMenu );

    // Create a tree-dom model and populate with menus.
    const model = new TreeDomModel();
    const selector = `[${ standardType.JS_HOOK }=${ FlyoutMenu.BASE_CLASS }]`;
    model.init( _dom, rootMenu, selector, _addMenu );
    const menusTree = model.getTree();
    rootMenu.setData( menusTree.getRoot() );

    // Initialize screen-size specific behaviors.
    _desktopNav = new MegaMenuDesktop( menusTree ).init();
    _mobileNav = new MegaMenuMobile( menusTree ).init();
    _mobileNav.addEventListener(
      'rootExpandBegin',
      _handleRootExpandBegin.bind( this )
    );
    _mobileNav.addEventListener(
      'rootCollapseEnd',
      _handleRootCollapseEnd.bind( this )
    );

    window.addEventListener( 'resize', _resizeHandler );
    // Pipe window resize handler into orientation change on supported devices.
    if ( 'onorientationchange' in window ) {
      window.addEventListener( 'orientationchange', _resizeHandler );
    }

    if ( breakpointState.isInDesktop() ) {
      _desktopNav.resume();
    } else {
      _mobileNav.resume();
    }

    _dom.classList.remove( 'u-hide-on-mobile' );

    _tabTrigger.init();
    _tabTrigger.addEventListener( 'tabPressed', _handleTabPress );

    return this;
  }

  /**
   * Create a new FlyoutMenu and attach it to a new tree node.
   * @param {HTMLNode} dom
   *   The dom element on which to initialize the FlyoutMenu behavior.
   * @param {TreeNode} treeNode
   *   The node in a tree on which to attach a new menu.
   * @returns {TreeNode} Return the processed tree node.
   */
  function _addMenu( dom, treeNode ) {
    const menu = new FlyoutMenu( dom ).init();
    const transition = new MoveTransition( menu.getDom().content ).init();
    menu.setExpandTransition( transition, transition.moveToOrigin );
    menu.setCollapseTransition( transition, transition.moveLeft );
    _addEvents( menu );
    treeNode.data = menu;
    menu.setData( treeNode );

    return treeNode;
  }

  /**
   * @param {FlyoutMenu} menu - a menu on which to attach events.
   */
  function _addEvents( menu ) {
    menu.addEventListener( 'triggerClick', _handleEvent );
    menu.addEventListener( 'triggerOver', _handleEvent );
    menu.addEventListener( 'triggerOut', _handleEvent );
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
    const activeNav = breakpointState.isInDesktop() ? _desktopNav : _mobileNav;
    activeNav.handleEvent( event );
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if ( breakpointState.isInDesktop() ) {
      _mobileNav.suspend();
      _desktopNav.resume();
    } else {
      _desktopNav.suspend();
      _mobileNav.resume();
    }
  }

  /**
   * Event handler for when the tab key is pressed.
   */
  function _handleTabPress() {
    collapse();
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenu} An instance.
   */
  function collapse() {
    if ( !breakpointState.isInDesktop() ) {
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
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.collapse = collapse;

  return this;
}

module.exports = MegaMenu;
