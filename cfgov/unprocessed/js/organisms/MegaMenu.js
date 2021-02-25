// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import FlyoutMenu from '../modules/behavior/FlyoutMenu.js';
import MegaMenuDesktop from '../organisms/MegaMenuDesktop.js';
import MegaMenuMobile from '../organisms/MegaMenuMobile.js';
import MoveTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/MoveTransition.js';
import TabTrigger from '../modules/TabTrigger.js';
import Tree from '../modules/Tree.js';
import { contains } from '@cfpb/cfpb-atomic-component/src/utilities/data-hook.js';
import { DESKTOP, viewportIsIn } from '../modules/util/breakpoint-state.js';

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

  const _dom = checkDom( element, BASE_CLASS );

  // Tree data model.
  let _menus;

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
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    // DOM selectors.
    const rootMenuDom = _dom;
    const rootContentDom = rootMenuDom.querySelector( '.' + BASE_CLASS + '_content' );

    // Create model.
    _menus = new Tree();

    // Create root menu.
    const transition = new MoveTransition( rootContentDom ).init();
    const rootMenu = new FlyoutMenu( rootMenuDom ).init();
    // Set initial position.
    rootMenu.setExpandTransition( transition, transition.moveToOrigin );
    rootMenu.setCollapseTransition( transition, transition.moveLeft );
    _addEvents( rootMenu );

    // Populate tree model with menus.
    const rootNode = _menus.init( rootMenu ).getRoot();
    rootMenu.setData( rootNode );
    _populateTreeFromDom( rootMenuDom, rootNode, _addMenu );

    // Initialize screen-size specific behaviors.
    _desktopNav = new MegaMenuDesktop( BASE_CLASS, _menus ).init();
    _mobileNav = new MegaMenuMobile( _menus ).init();
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

    if ( viewportIsIn( DESKTOP ) ) {
      _desktopNav.resume();
    } else {
      _mobileNav.resume();
    }

    _dom.classList.remove( 'u-hidden' );

    _tabTrigger.init();
    _tabTrigger.addEventListener( 'tabPressed', _handleTabPress );

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
    const children = dom.children;
    if ( !children ) {
      return;
    }
    let child;
    for ( let i = 0, len = children.length; i < len; i++ ) {
      let newParentNode = parentNode;
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
    let newParentNode = parentNode;
    let transition;
    if ( contains( dom, FlyoutMenu.BASE_CLASS ) ) {
      const menu = new FlyoutMenu( dom ).init();
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
    const activeNav = viewportIsIn( DESKTOP ) ? _desktopNav : _mobileNav;
    activeNav.handleEvent( event );
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if ( viewportIsIn( DESKTOP ) ) {
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
    if ( !viewportIsIn( DESKTOP ) ) {
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

export default MegaMenu;
