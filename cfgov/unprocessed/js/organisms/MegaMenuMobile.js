import { bfs } from '../modules/util/tree-traversal.js';
import { EventObserver, MoveTransition } from '@cfpb/cfpb-design-system';

/**
 * MegaMenuMobile
 * @class
 * @classdesc Behavior for the mega menu at desktop sizes.
 * @param {Tree} menus - Tree of FlyoutMenus.
 * @returns {MegaMenuMobile} An instance.
 */
function MegaMenuMobile(menus) {
  // DOM references.
  const _bodyDom = document.body;

  // Binded functions.
  const _handleTriggerClickBinded = _handleTriggerClick.bind(this);
  const _handleExpandBeginBinded = _handleExpandBegin.bind(this);
  const _handleExpandEndBinded = _handleExpandEnd.bind(this);
  const _handleCollapseBeginBinded = _handleCollapseBegin.bind(this);
  const _handleCollapseEndBinded = _handleCollapseEnd.bind(this);

  // Tree model.
  const _menus = menus;

  let _rootMenu;
  let _rootMenuContentDom;

  //  Currently showing menu picked from the tree.
  let _activeMenu = null;

  /* Active menu DOM is unused, but is left commented out in case access
     to the DOM is needed in the future. */
  // let _activeMenuDom;

  let _rootLinksDom;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  /**
   * @returns {MegaMenuMobile} An instance.
   */
  function init() {
    const rootNode = _menus.getRoot();
    _rootMenu = rootNode.data;
    _rootMenuContentDom = _rootMenu.getDom().content;
    _activeMenu = _rootMenu;
    // _activeMenuDom = _rootMenuContentDom;

    // Make root level links disabled to tab and voiceover navigation on init.
    _rootLinksDom = _rootMenuContentDom.querySelectorAll(
      'a.o-mega-menu__content-1-link,.m-global-eyebrow a',
    );

    return this;
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event - The event object for the click event.
   */
  function _handleBodyClick(event) {
    const target = event.target;
    if (_activeMenu.getDom().trigger[0] === target) {
      return;
    }

    if (!_rootMenu.getDom().container.contains(target)) {
      _rootMenu.getDom().trigger[0].click();
    }
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
      expandend: _handleExpandEndBinded,
      collapsebegin: _handleCollapseBeginBinded,
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
    const transition = _rootMenu.getTransition();

    // Halt any active transitions.
    if (_activeMenu) {
      _activeMenu.getTransition()?.halt();
    }

    // Scroll to top of page so menu is always at the top.
    document.body.scrollTop = document.documentElement.scrollTop = 0;

    if (menu === _rootMenu) {
      // Root menu is closing.
      if (_rootMenu.isExpanded()) {
        _disableRootMenuContent();
        const currLevel = _activeMenu.getData().level + 1;
        let transitionCollapseMethod = 'moveLeft';
        transitionCollapseMethod += currLevel === 1 ? '' : currLevel;
        _rootMenu.setTransition(
          transition,
          transition[transitionCollapseMethod],
        );
      } else {
        // The transition animation is turned off when resuming to avoid a
        // flash of the menu being opened, so we re-animate on the click.
        _rootMenu.getTransition().animateOn();

        // Root menu is opening.
        _enableRootMenuContent();
      }
      _activeMenu = _rootMenu;
    } else {
      // Submenu clicked.

      // Back button on the 2nd level menu clicked.
      if (
        event.trigger.classList.contains('o-mega-menu__content-2-alt-trigger')
      ) {
        _enableRootMenuContent();
        _activeMenu = _rootMenu;
      } else {
        _disableRootMenuContent();
        menu.setTransition(
          transition,
          transition.moveToOrigin,
          transition.moveLeft,
        );
        _rootMenu.getDom().content.classList.remove('u-hidden-overflow');
        _activeMenu = menu;
      }
    }
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandbegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleExpandBegin(event) {
    const menu = event.target;
    const menuDom = menu.getDom();

    if (menu === _rootMenu) {
      this.dispatchEvent('rootexpandbegin', { target: this });
      _bodyDom.addEventListener('click', _handleBodyClick);
    }

    menuDom.content.classList.add('u-is-animating');
  }

  /**
   * Event handler for when FlyoutMenu expand transition ends.
   * Use this to perform post-expandEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleExpandEnd(event) {
    const menu = event.target;
    const menuDom = menu.getDom();
    const level = menu.getData().level;

    if (level >= 1) {
      menuDom.trigger[1].focus();
    }

    menuDom.content.classList.remove('u-is-animating');
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has begun.
   * Use this to perform post-collapseBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseBegin(event) {
    const menu = event.target;
    const menuDom = menu.getDom();

    if (menu === _rootMenu) {
      _bodyDom.removeEventListener('click', _handleBodyClick);
    }

    menuDom.content.classList.add('u-is-animating');
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd(event) {
    const menu = event.target;
    const menuDom = menu.getDom();
    const level = menu.getData().level;

    if (menu === _rootMenu) {
      bfs(_menus.getRoot(), (node) => {
        const menu = node.data;
        if (menu.isExpanded() && node.level > 0) {
          const transition = _rootMenu.getTransition();
          transition.animateOff();
          menu.setTransition(transition, transition.moveLeft);
          menu.collapse();
        }
      });
      this.dispatchEvent('rootcollapseend', { target: this });
    }

    if (level >= 1) {
      menuDom.trigger[0].focus();
      _rootMenu.getDom().content.classList.add('u-hidden-overflow');
    }

    menuDom.content.classList.remove('u-is-animating');
  }

  /**
   * Hide the root menu content.
   * This is to prevent tabbing to off-screen content.
   */
  function _disableRootMenuContent() {
    for (let i = 0, len = _rootLinksDom.length; i < len; i++) {
      _rootLinksDom[i].setAttribute('tabindex', '-1');
      _rootLinksDom[i].setAttribute('aria-hidden', 'true');
    }
  }

  /**
   * Show the root menu content.
   */
  function _enableRootMenuContent() {
    for (let i = 0, len = _rootLinksDom.length; i < len; i++) {
      _rootLinksDom[i].removeAttribute('tabindex');
      _rootLinksDom[i].removeAttribute('aria-hidden');
    }
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenuMobile} A instance.
   */
  function collapse() {
    if (_rootMenu.isExpanded()) {
      _rootMenu.getDom().trigger[0].click();
    }

    return this;
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function resume() {
    if (_suspended) {
      _rootMenuContentDom.classList.add('u-hidden-overflow');
      const transition = new MoveTransition(_rootMenuContentDom).init(
        MoveTransition.CLASSES.MOVE_LEFT,
      );
      transition.animateOff();
      _rootMenu.setTransition(
        transition,
        transition.moveLeft,
        transition.moveToOrigin,
      );

      _activeMenu = _rootMenu;

      _disableRootMenuContent();

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
      bfs(_menus.getRoot(), (node) => {
        const menu = node.data;
        if (menu.isExpanded()) {
          menu.getTransition().animateOff();
          menu.collapse();
        }
        menu.clearTransition();
      });
      _rootMenuContentDom.classList.remove('u-invisible');
      _rootMenuContentDom.classList.remove('u-hidden-overflow');

      _enableRootMenuContent();

      _bodyDom.removeEventListener('click', _handleBodyClick);

      _suspended = true;
    }

    return _suspended;
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

export { MegaMenuMobile };
