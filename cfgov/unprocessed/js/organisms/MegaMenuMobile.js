// Required modules.
import * as treeTraversal from '../modules/util/tree-traversal.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import MoveTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/MoveTransition.js';

/**
 * MegaMenuMobile
 * @class
 *
 * @classdesc Behavior for the mega menu at desktop sizes.
 *
 * @param {Tree} menus - Tree of FlyoutMenus.
 * @returns {MegaMenuMobile} An instance.
 */
function MegaMenuMobile( menus ) {

  // DOM references.
  const _bodyDom = document.body;

  // Binded functions.
  const _handleTriggerClickBinded = _handleTriggerClick.bind( this );
  const _handleExpandBeginBinded = _handleExpandBegin.bind( this );
  const _handleExpandEndBinded = _handleExpandEnd.bind( this );
  const _handleCollapseBeginBinded = _handleCollapseBegin.bind( this );
  const _handleCollapseEndBinded = _handleCollapseEnd.bind( this );
  const _suspendBinded = suspend.bind( this );

  // Tree model.
  const _menus = menus;

  let _rootMenu;
  let _rootMenuContentDom;

  //  Currently showing menu picked from the tree.
  let _activeMenu = null;
  let _activeMenuDom;

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
    _activeMenuDom = _rootMenuContentDom;

    // Make root level links disabled to tab and voiceover navigation on init.
    _rootLinksDom = _rootMenuContentDom.querySelectorAll( 'a:not(.o-mega-menu_content-2 a)' );

    return this;
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event The event object for the click event.
   */
  function _handleBodyClick( event ) {
    const target = event.target;
    if ( _activeMenu.getDom().trigger[0] === target ) {
      return;
    }

    if ( !_rootMenu.getDom().container.contains( target ) ) {
      _rootMenu.getDom().trigger[0].click();
    }
  }

  /**
   * Pass an event bubbled up from the menus to the appropriate handler.
   * @param {Event} event - A FlyoutMenu event.
   */
  function handleEvent( event ) {
    if ( _suspended ) { return; }
    const eventMap = {
      triggerClick:  _handleTriggerClickBinded,
      expandBegin:   _handleExpandBeginBinded,
      expandEnd:     _handleExpandEndBinded,
      collapseBegin: _handleCollapseBeginBinded,
      collapseEnd:   _handleCollapseEndBinded
    };

    const currHandler = eventMap[event.type];
    if ( currHandler ) { currHandler( event ); }
  }

  /**
   * Event handler for when FlyoutMenu trigger is clicked.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerClick( event ) {
    this.dispatchEvent( 'triggerClick', { target: this } );
    const menu = event.target;
    const rootMenu = _menus.getRoot().data;
    const menuNode = menu.getData();
    let level = menuNode.level;
    const transition = rootMenu.getTransition();

    // Halt any active transitions.
    if ( _activeMenu ) {
      _activeMenu.getTransition().halt();
    }

    // Scroll to top of page so menu is always at the top.
    document.body.scrollTop = document.documentElement.scrollTop = 0;

    if ( menu === rootMenu ) {
      // Root menu clicked.
      _enableRootMenuContent();

      // Root menu is closing.
      if ( menu.isExpanded() ) {
        level = _activeMenu.getData().level;
        menu.setCollapseTransition(
          transition,
          transition.moveLeft,
          [ level + 1 ]
        );
        _disableRootMenuContent();
      }
    } else {
      // Submenu clicked.
      menuNode.data.setExpandTransition(
        transition,
        transition.moveLeft,
        [ level ]
      );

      // Back button on the 2nd level menu clicked.
      if ( event.trigger.classList.contains( 'o-mega-menu_content-2-alt-trigger' ) ) {
        _enableRootMenuContent();
      } else {
        _disableRootMenuContent();
      }

      if ( level === 1 ) {
        menuNode.data.setCollapseTransition(
          transition,
          transition.moveToOrigin
        );
      } else {
        // This is only used if we re-add a 3rd level menu.
        menuNode.data.setCollapseTransition(
          transition,
          transition.moveLeft
        );
      }

      /* TODO: Investigate helper functions to mask these crazy long lookups!
         Do we really want to remove the overflow here? We're also adding it
         in the collapse end. */
      menuNode.parent.data.getDom()
        .content.classList.remove( 'u-hidden-overflow' );
    }
    _activeMenu = menu;
  }

  /**
   * Event handler for when the search input flyout is toggled,
   * which opens/closes the search input.
   * @param {FlyoutMenu} target - menu that is expanding or collapsing.
   */
  function _handleToggle( target ) {
    if ( target === _rootMenu &&
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
    const menu = event.target;
    const menuDom = menu.getDom();

    _handleToggle( menu );

    if ( menu === _rootMenu ) {
      this.dispatchEvent( 'rootExpandBegin', { target: this } );
      _bodyDom.addEventListener( 'click', _handleBodyClick );
    }

    menuDom.content.classList.add( 'u-is-animating' );
  }

  /**
   * Event handler for when FlyoutMenu expand transition ends.
   * Use this to perform post-expandEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleExpandEnd( event ) {
    const menu = event.target;
    const menuNode = menu.getData();
    const menuDom = menu.getDom();
    const level = menuNode.level;

    if ( level >= 1 ) {
      menuDom.trigger[1].focus();
    }

    menuDom.content.classList.remove( 'u-is-animating' );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has begun.
   * Use this to perform post-collapseBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseBegin( event ) {
    const menu = event.target;
    const menuDom = menu.getDom();

    _handleToggle( menu );
    if ( menu === _rootMenu ) {
      _bodyDom.removeEventListener( 'click', _handleBodyClick );
    }

    menuDom.content.classList.add( 'u-is-animating' );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd( event ) {
    const menu = event.target;
    const menuNode = menu.getData();
    const menuDom = menu.getDom();
    const level = menuNode.level;

    if ( menu === _rootMenu ) {
      _suspendBinded();
      resume();
    } else {

      /* When clicking the back button and sliding to the right,
         hide the overflow after animation has completed. */
      const parentNode = menu.getData().parent;
      parentNode.data.getDom().content.classList.add( 'u-hidden-overflow' );
    }

    if ( level >= 1 ) {
      menuDom.trigger[0].focus();
    }

    menuDom.content.classList.remove( 'u-is-animating' );
  }

  /**
   * Hide the root menu content.
   * This is to prevent tabbing to off-screen content.
   */
  function _disableRootMenuContent() {
    for ( let i = 0, len = _rootLinksDom.length; i < len; i++ ) {
      _rootLinksDom[i].setAttribute( 'tabindex', '-1' );
      _rootLinksDom[i].setAttribute( 'aria-hidden', 'true' );
    }
  }

  /**
   * Show the root menu content.
   */
  function _enableRootMenuContent() {
    for ( let i = 0, len = _rootLinksDom.length; i < len; i++ ) {
      _rootLinksDom[i].removeAttribute( 'tabindex' );
      _rootLinksDom[i].removeAttribute( 'aria-hidden' );
    }
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenuMobile} A instance.
   */
  function collapse() {
    if ( _rootMenu.isExpanded() ) {
      _rootMenu.getDom().trigger[0].click();
    }

    return this;
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function resume() {
    if ( _suspended ) {
      const transition = new MoveTransition( _rootMenuContentDom ).init();
      _rootMenu.setExpandTransition( transition, transition.moveToOrigin );
      _rootMenu.setCollapseTransition( transition, transition.moveLeft );
      _rootMenu.getTransition().moveLeft();
      _rootMenuContentDom.classList.add( 'u-hidden-overflow' );

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
    if ( !_suspended ) {
      _suspended = true;

      treeTraversal.bfs( _menus.getRoot(), _handleSuspendTraversal );
      _rootMenuContentDom.classList.remove( 'u-invisible' );
      _rootMenuContentDom.classList.remove( 'u-hidden-overflow' );

      _enableRootMenuContent();

      /* TODO: Investigate updating this to close the menus directly
         so `_handleCollapseEnd` is fired. */
      this.dispatchEvent( 'rootCollapseEnd', { target: this } );
      _bodyDom.removeEventListener( 'click', _handleBodyClick );
    }

    return _suspended;
  }

  /**
   * Iterate over the sub menus and handle setting the suspended state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleSuspendTraversal( node ) {
    const menu = node.data;
    menu.clearTransitions();

    /* TODO: Investigate whether deferred collapse has another solution.
       This check is necessary since a call to an already collapsed
       menu will set a deferred collapse that will be called
       on expandEnd next time the flyout is expanded.
       The deferred collapse is used in cases where the
       user clicks the flyout menu while it is animating open,
       so that it appears like they can collapse it, even when
       clicking during the expand animation. */
    if ( menu.isExpanded() ) {
      menu.collapse();
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

export default MegaMenuMobile;
