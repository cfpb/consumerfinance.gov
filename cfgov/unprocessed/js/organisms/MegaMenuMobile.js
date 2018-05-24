// Required modules.
const EventObserver = require( '../modules/util/EventObserver' );
const MoveTransition = require( '../modules/transition/MoveTransition' );
const treeTraversal = require( '../modules/util/tree-traversal' );

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

    return this;
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event The event object for the click event.
   */
  function _handleBodyClick( event ) {
    const target = event.target;
    if ( _activeMenu.getDom().trigger === target ) {
      return;
    }

    if ( !_rootMenu.getDom().container.contains( target ) ) {
      _rootMenu.getDom().trigger.click();
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

    if ( menu === rootMenu ) {
      // Root menu clicked.

      // Root menu is closing.
      if ( menu.isExpanded() ) {
        level = _activeMenu.getData().level;
        menu.setCollapseTransition(
          transition,
          transition.moveLeft,
          [ level + 1 ]
        );
      }
    } else {
      // Submenu clicked.

      // Scroll to top of page so menu is always at the top.
      document.body.scrollTop = document.documentElement.scrollTop = 0;

      const siblings = _menus.getAllAtLevel( level );
      let siblingMenu;
      for ( let i = 0, len = siblings.length; i < len; i++ ) {
        siblingMenu = siblings[i].data;
        siblingMenu.setExpandTransition(
          transition,
          transition.moveLeft,
          [ level ]
        );

        /* If on the 2nd level menu, set the back button to moveToOrigin,
           otherwise we're on the 3rd level menu, so moveLeft is needed. */
        if ( level === 1 ) {
          siblingMenu
            .setCollapseTransition( transition, transition.moveToOrigin );
        } else {
          siblingMenu.setCollapseTransition( transition, transition.moveLeft );
        }
        // If we're on the current menu, show it & hide all the other siblings.
        if ( siblings[i] === menuNode ) {
          siblingMenu.getDom().content.classList.remove( 'u-invisible' );
        } else {
          siblingMenu.getDom().content.classList.add( 'u-invisible' );
        }
      }

      // TODO: Investigate helper functions to mask these crazy long lookups!
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
    window.scrollTo( 0, 0 );
    const menu = event.target;
    _handleToggle( menu );
    if ( menu === _rootMenu ) {
      this.dispatchEvent( 'rootExpandBegin', { target: this } );
      _bodyDom.addEventListener( 'click', _handleBodyClick );
    }

    /* TODO: Enable or remove when keyboard navigation is in.
       If on a submenu, focus the back button, otherwise focus the first link.
       var firstMenuLink;
       if ( _activeMenu === _rootMenu ) {
       firstMenuLink = _activeMenuDom.querySelector( 'a' );
       } else {
       firstMenuLink = _activeMenuDom.querySelector( 'button' );
       }
       firstMenuLink.focus(); */
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has begun.
   * Use this to perform post-collapseBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseBegin( event ) {
    const menu = event.target;
    _handleToggle( menu );
    if ( menu === _rootMenu ) {
      _bodyDom.removeEventListener( 'click', _handleBodyClick );
    }
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd( event ) {
    const menu = event.target;
    if ( menu === _rootMenu ) {
      _suspendBinded();
      resume();
    } else {

      /* When clicking the back button and sliding to the right,
         hide the overflow after animation has completed. */
      const parentNode = menu.getData().parent;
      parentNode.data.getDom().content.classList.add( 'u-hidden-overflow' );
    }
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenuMobile} A instance.
   */
  function collapse() {
    if ( _rootMenu.isExpanded() ) {
      _rootMenu.getDom().trigger.click();
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

module.exports = MegaMenuMobile;
