import {
  contains,
  checkDom,
  setInitFlag,
  EventObserver,
  FlyoutMenu,
  MoveTransition,
} from '@cfpb/cfpb-design-system';
import { MegaMenuDesktop } from '../organisms/MegaMenuDesktop.js';
import { MegaMenuMobile } from '../organisms/MegaMenuMobile.js';
import { TabTrigger } from '../modules/TabTrigger.js';
import { Tree } from '../modules/Tree.js';
import {
  DESKTOP,
  MOBILE,
  viewportIsIn,
} from '../modules/util/breakpoint-state.js';

const BASE_CLASS = 'o-mega-menu';

/**
 * MegaMenu
 * @class
 * @classdesc Initializes a new MegaMenu organism.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the organism.
 * @returns {MegaMenu} An instance.
 */
function MegaMenu(element) {
  const _dom = checkDom(element, BASE_CLASS);

  // Tree data model.
  let _menus;

  // Screen-size specific behaviors.
  let _activeNav;
  let _desktopNav;
  let _mobileNav;

  /* The tab trigger adds an element to the end of the element that handles
     cleanup after tabbing out of the element. */
  const _tabTrigger = new TabTrigger(_dom);

  /**
   * @returns {MegaMenu|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    // DOM selectors.
    const rootMenuDom = _dom;
    const rootContentDom = rootMenuDom.querySelector(`.${BASE_CLASS}__content`);

    // Create model.
    _menus = new Tree();

    // Whether initial state is desktop or mobile.
    const isInDesktop = viewportIsIn(DESKTOP);

    // Create root menu.
    const rootMenu = new FlyoutMenu(rootMenuDom, false).init();

    // Set initial transition for root menu on mobile. It's hidden on desktop.
    if (!isInDesktop) {
      const transition = new MoveTransition(rootContentDom).init(
        MoveTransition.CLASSES.MOVE_LEFT,
      );
      rootMenu.setTransition(
        transition,
        transition.moveLeft,
        transition.moveToOrigin,
      );
    }

    // Populate tree model with menus.
    const rootNode = _menus.init(rootMenu).getRoot();
    rootMenu.setData(rootNode);
    _populateTreeFromDom(rootMenuDom, rootNode, _addMenu);

    // Initialize screen-size specific behaviors.
    _desktopNav = new MegaMenuDesktop(BASE_CLASS, _menus).init();
    _mobileNav = new MegaMenuMobile(_menus).init();

    // Add events and listeners to root menu.
    _addEvents(rootMenu);
    _mobileNav.addEventListener('rootexpandbegin', () =>
      this.dispatchEvent('rootexpandbegin', { target: this }),
    );
    _mobileNav.addEventListener('rootcollapseend', () =>
      this.dispatchEvent('rootcollapseend', { target: this }),
    );

    window.addEventListener('resize', _resizeHandler);
    // Pipe window resize handler into orientation change on supported devices.
    if ('onorientationchange' in window) {
      window.addEventListener('orientationchange', _resizeHandler);
    }

    // Force initial state.
    _resizeHandler();

    _tabTrigger.init();
    _tabTrigger.addEventListener('tabpressed', () => collapse());

    // All set! Show the menu.
    _dom.classList.remove('u-hidden');

    return this;
  }

  /**
   * Perform a recursive depth-first search of the DOM
   * and call a function for each node.
   * @param {HTMLElement} dom - A DOM element to search from.
   * @param {TreeNode} parentNode - Node in a tree from which
   *   to attach new nodes.
   * @param {Function} callback - Function to call on each node.
   *   Must return a TreeNode.
   */
  function _populateTreeFromDom(dom, parentNode, callback) {
    const children = dom.children;
    if (!children) {
      return;
    }

    let child;
    for (let i = 0, len = children.length; i < len; i++) {
      let newParentNode = parentNode;
      child = children[i];
      newParentNode = callback.call(this, child, newParentNode);
      _populateTreeFromDom(child, newParentNode, callback);
    }
  }

  /**
   * Create a new FlyoutMenu and attach it to a new tree node.
   * @param {HTMLElement} dom - A DOM element to check for a js
   *   data-* attribute hook.
   * @param {TreeNode} parentNode - The parent node in a tree on which
   *   to attach a new menu.
   * @returns {TreeNode} Return the processed tree node.
   */
  function _addMenu(dom, parentNode) {
    let newParentNode = parentNode;
    if (contains(dom, FlyoutMenu.BASE_CLASS)) {
      const menu = new FlyoutMenu(dom, false).init();
      _addEvents(menu);
      newParentNode = newParentNode.tree.add(menu, newParentNode);
      menu.setData(newParentNode);
    }

    return newParentNode;
  }

  /**
   * @param {FlyoutMenu} menu - a menu on which to attach events.
   */
  function _addEvents(menu) {
    menu.addEventListener('triggerclick', _handleEvent);
    menu.addEventListener('expandbegin', _handleEvent);
    menu.addEventListener('expandend', _handleEvent);
    menu.addEventListener('collapsebegin', _handleEvent);
    menu.addEventListener('collapseend', _handleEvent);
  }

  /**
   * Handle events coming from menu,
   * and pass it to the desktop or mobile behaviors.
   * @param {object} event - A FlyoutMenu event object.
   */
  function _handleEvent(event) {
    const activeNav = _activeNav === DESKTOP ? _desktopNav : _mobileNav;
    activeNav.handleEvent(event);
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if (viewportIsIn(DESKTOP)) {
      _mobileNav.suspend();
      _desktopNav.resume();
      _activeNav = DESKTOP;
    } else {
      _desktopNav.suspend();
      _mobileNav.resume();
      _activeNav = MOBILE;
    }
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenu} An instance.
   */
  function collapse() {
    if (viewportIsIn(DESKTOP)) {
      _desktopNav.collapse();
    } else {
      _mobileNav.collapse();
    }

    return this;
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

export { MegaMenu };
