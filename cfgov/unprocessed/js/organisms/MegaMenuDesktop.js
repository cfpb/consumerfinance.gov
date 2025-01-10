import { bfs } from '../modules/util/tree-traversal.js';
import { EventObserver, MoveTransition } from '@cfpb/cfpb-design-system';

/**
 * MegaMenuDesktop
 * @class
 * @classdesc Behavior for the mega menu at desktop sizes.
 * @param {string} baseClass - The base class of the parent mega menu.
 * @param {Tree} menus - Tree of FlyoutMenus.
 * @returns {MegaMenuDesktop} An instance.
 */
function MegaMenuDesktop(baseClass, menus) {
  // DOM references.
  const _bodyDom = document.body;
  let _firstLevelDom;

  // Binded functions.
  const _handleTriggerClickBinded = _handleTriggerClick.bind(this);
  const _handleExpandBeginBinded = _handleExpandBegin.bind(this);
  const _handleCollapseEndBinded = _handleCollapseEnd.bind(this);

  // Tree model.
  const _menus = menus;

  //  Currently showing menu picked from the tree.
  let _activeMenu = null;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  /**
   * @returns {MegaMenuDesktop} An instance.
   */
  function init() {
    /* Get the immediate parent of the 1st level menu links.
       We'll use this later to check if we're still over the links,
       when clicking to close the menu. */
    const firstLevelMenus = _menus.getAllAtLevel(1);
    if (firstLevelMenus.length > 0) {
      _firstLevelDom = firstLevelMenus[0].data.getDom().container.parentNode;
    }

    return this;
  }

  /**
   * Pass an event bubbled up from the menus to the appropriate handler.
   * @param {Event} event - A FlyoutMenu event.
   */
  function handleEvent(event) {
    if (_suspended) {
      return;
    }

    const eventMap = {
      triggerclick: _handleTriggerClickBinded,
      expandbegin: _handleExpandBeginBinded,
      collapseend: _handleCollapseEndBinded,
    };

    const currHandler = eventMap[event.type];
    if (currHandler) {
      currHandler(event);
    }
  }

  /**
   * Event handler for when FlyoutMenu trigger is clicked.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerClick(event) {
    const menu = event.target;
    _updateMenuState(menu);
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandbegin actions.
   */
  function _handleExpandBegin() {
    // Set keyboard focus on first menu item link.
    const activeMenuDom = _activeMenu.getDom().content;
    activeMenuDom.classList.remove('u-invisible');
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd(event) {
    event.target.getDom().content.classList.add('u-invisible');
  }

  /**
   * Event handler for when clicking on the body of the document.
   * @param {MouseEvent} event - The click event.
   */
  function _handleBodyClick(event) {
    // If we've clicked outside the parent of the current menu, close it.
    if (!_firstLevelDom.contains(event.target)) {
      _updateMenuState(null);
    }
  }

  /**
   * Cleanup state and set the currently active menu.
   * @param {FlyoutMenu} menu - The menu currently being activated.
   */
  function _updateMenuState(menu) {
    if (menu === null || _activeMenu === menu) {
      // A menu is closed or the menu is suspended.

      // If we've ever opened the menu, _activeMenu has to be cleared.
      if (_activeMenu) {
        _activeMenu.getTransition()?.animateOn();
        if (menu === null) _activeMenu.collapse();
        _activeMenu = null;
      }

      // Clean up listeners
      _bodyDom.removeEventListener('click', _handleBodyClick);
    } else if (_activeMenu === null) {
      // A menu is opened.
      _activeMenu = menu;
      _activeMenu.getTransition()?.animateOn();

      // Close the menu on click of the document body.
      _bodyDom.addEventListener('click', _handleBodyClick);
    } else {
      // An open menu has switched to another menu.
      _activeMenu.getTransition()?.animateOff();
      _activeMenu.collapse();
      _activeMenu = menu;
      _activeMenu.getTransition()?.animateOff();
    }
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenuDesktop} An instance.
   */
  function collapse() {
    // Close the menu.
    _updateMenuState(null);

    return this;
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function resume() {
    if (_suspended) {
      bfs(_menus.getRoot(), _handleResumeTraversal);
      _suspended = false;
    }

    return !_suspended;
  }

  /**
   * Remove events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been suspended or not.
   */
  function suspend() {
    if (!_suspended) {
      // Clear active menu.
      _updateMenuState(null);

      bfs(_menus.getRoot(), _handleSuspendTraversal);

      _suspended = true;
    }

    return _suspended;
  }

  /**
   * Iterate over the sub menus and handle setting the resumed state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleResumeTraversal(node) {
    const nLevel = node.level;
    const menu = node.data;

    if (nLevel === 1) {
      const wrapperSel = `.${baseClass}__content-2-wrapper`;
      const contentDom = menu.getDom().content;
      const wrapperDom = contentDom.querySelector(wrapperSel);

      // This ensures the transition has been removed by MegaMenuMobile.
      let transition = menu.getTransition();
      if (transition) transition.setElement(wrapperDom);
      else
        transition = new MoveTransition(wrapperDom).init(
          MoveTransition.CLASSES.MOVE_UP,
        );

      /* TODO: The only reason hiding is necessary is that the
         drop-shadow of the menu extends below its border,
         so it's still visible when the menu slides -100% out of view.
         Investigate whether it would be better to have a u-move-up-1_1x
         or similar class to move up -110%. Or whether the drop-shadow
         could be included within the bounds of the menu. */
      menu.getDom().content.classList.add('u-invisible');
      transition.animateOff();
      transition.moveUp();

      menu.setTransition(
        transition,
        transition.moveUp,
        transition.moveToOrigin,
      );
    } else if (nLevel === 2) {
      menu.suspend();
    }
  }

  /**
   * Iterate over the sub menus and handle setting the suspended state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleSuspendTraversal(node) {
    const nLevel = node.level;
    const menu = node.data;

    if (nLevel === 1) {
      menu.clearTransition();
      menu.getDom().content.classList.remove('u-invisible');

      if (menu.isExpanded()) {
        menu.collapse();
      }
    } else if (nLevel === 2) {
      menu.resume();
    }
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.collapse = collapse;
  this.handleEvent = handleEvent;
  this.init = init;
  this.resume = resume;
  this.suspend = suspend;

  return this;
}

export { MegaMenuDesktop };
