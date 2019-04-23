// Required modules.
import EventObserver from '../modules/util/EventObserver';
import MoveTransition from '../modules/transition/MoveTransition';
import * as treeTraversal from '../modules/util/tree-traversal';

/**
 * MegaMenuDesktop
 * @class
 *
 * @classdesc Behavior for the mega menu at desktop sizes.
 *
 * @param {Tree} menus - Tree of FlyoutMenus.
 * @returns {MegaMenuDesktop} An instance.
 */
function MegaMenuDesktop( menus ) {

  // DOM references.
  const _bodyDom = document.body;
  let _firstLevelDom;

  // Binded functions.
  const _handleTriggerClickBinded = _handleTriggerClick.bind( this );
  const _handleTriggerOverBinded = _handleTriggerOver.bind( this );
  const _handleTriggerOutBinded = _handleTriggerOut.bind( this );
  const _handleExpandBeginBinded = _handleExpandBegin.bind( this );
  const _handleCollapseEndBinded = _handleCollapseEnd.bind( this );

  // Tree model.
  const _menus = menus;

  //  Currently showing menu picked from the tree.
  let _activeMenu = null;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  // Timeout for delayed events.
  let _showDelay;

  /**
   * @returns {MegaMenuDesktop} An instance.
   */
  function init() {

    /* Get the immediate parent of the 1st level menu links.
       We'll use this later to check if we're still over the links,
       on mouse move. */
    const firstLevelMenus = _menus.getAllAtLevel( 1 );
    if ( firstLevelMenus.length > 0 ) {
      _firstLevelDom = firstLevelMenus[0].data.getDom().container.parentNode;
    }

    return this;
  }

  /**
   * Pass an event bubbled up from the menus to the appropriate handler.
   * @param {Event} event - A FlyoutMenu event.
   */
  function handleEvent( event ) {
    if ( _suspended ) { return; }
    const eventMap = {
      triggerClick: _handleTriggerClickBinded,
      triggerOver:  _handleTriggerOverBinded,
      triggerOut:   _handleTriggerOutBinded,
      expandBegin:  _handleExpandBeginBinded,
      collapseEnd:  _handleCollapseEndBinded
    };

    const currHandler = eventMap[event.type];
    if ( currHandler ) {
      const delay = _calcEventDelay( event.type );
      if ( delay > 0 ) {
        _delayedEvent( currHandler, event, delay );
      } else {
        currHandler( event );
      }
    }
  }

  /**
   * @param {string} type - The type of event to check.
   * @returns {number} The amount to delay in milliseconds,
   *   length is determined based on the event type and
   *   whether the menu is active or not.
   */
  function _calcEventDelay( type ) {
    let delay = 0;
    if ( type === 'triggerClick' ) {
      window.clearTimeout( _showDelay );
    } else if ( type === 'triggerOver' ) {
      if ( _activeMenu === null ) {
        delay = 150;
      } else {
        delay = 50;
      }
    }

    return delay;
  }

  /**
   * Delay the broadcasting of an event by supplied delay.
   * @param {Function} currHandler - Event handler.
   * @param {Event} event - A FlyoutMenu event.
   * @param {number} delay - Delay in milliseconds.
   */
  function _delayedEvent( currHandler, event, delay ) {
    window.clearTimeout( _showDelay );
    _showDelay = window.setTimeout( function() {
      currHandler( event );
    }, delay );
  }

  /**
   * Event handler for when FlyoutMenu trigger is clicked.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerClick( event ) {
    this.dispatchEvent( 'triggerClick', { target: this } );
    const menu = event.target;
    if ( menu.isAnimating() ) { return; }
    _updateMenuState( menu, event.type );
  }

  /**
   * Event handler for when FlyoutMenu trigger is hovered over.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerOver( event ) {
    this.dispatchEvent( 'triggerOver', { target: this } );
    _updateMenuState( event.target, event.type );
  }

  /**
   * Event handler for when FlyoutMenu trigger is hovered out.
   */
  function _handleTriggerOut() {
    this.dispatchEvent( 'triggerOut', { target: this } );
    // Clear any queued events to show the menu.
    window.clearTimeout( _showDelay );
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandBegin actions.
   */
  function _handleExpandBegin() {
    this.dispatchEvent( 'expandBegin', { target: this } );

    // Set keyboard focus on first menu item link.
    const activeMenuDom = _activeMenu.getDom().content;
    activeMenuDom.classList.remove( 'u-invisible' );

    /* TODO: Remove or uncomment when keyboard navigation is in.
       var firstMenuLink = activeMenuDom.querySelector( 'a' );
       firstMenuLink.focus(); */
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd( event ) {
    this.dispatchEvent( 'collapseEnd', { target: this } );
    event.target.getDom().content.classList.add( 'u-invisible' );
  }

  /**
   * Event handler for when mouse is hovering.
   * @param {MouseEvent} event - The hovering event.
   */
  function _handleMove( event ) {
    // If we've left the parent container of the current menu, close it.
    if ( !_firstLevelDom.contains( event.target ) ) {
      _updateMenuState( null, event.type );
    }
  }

  /**
   * Cleanup state and set the currently active menu.
   * @param {FlyoutMenu} menu - The menu currently being activated.
   * @param {string} type - The event type that is calling this method.
   */
  function _updateMenuState( menu, type ) {
    if ( menu === null || _activeMenu === menu ) {
      // A menu is closed.
      window.clearTimeout( _showDelay );
      _activeMenu.getTransition().animateOn();
      _activeMenu.collapse();
      _activeMenu = null;
      _bodyDom.removeEventListener( 'mousemove', _handleMove );
      _bodyDom.removeEventListener( 'mouseleave', _handleMove );
    } else if ( _activeMenu === null ) {
      // A menu is opened.
      _activeMenu = menu;
      _activeMenu.getTransition().animateOn();

      /* Mousemove needed in addition to mouseout of the trigger
         in order to check if user has moved off the menu <ul> and not
         just the <li> list items. */
      _bodyDom.addEventListener( 'mousemove', _handleMove );
      _bodyDom.addEventListener( 'mouseleave', _handleMove );
      _activeMenu.expand();
    } else {
      // An open menu has switched to another menu.
      _activeMenu.getTransition().animateOff();
      _activeMenu.collapse();
      _activeMenu = menu;
      if ( type === 'triggerOver' ) {
        _activeMenu.getTransition().animateOff();
        _activeMenu.expand();
      }
    }
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function resume() {
    if ( _suspended ) {
      treeTraversal.bfs( _menus.getRoot(), _handleResumeTraversal );
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
      treeTraversal.bfs( _menus.getRoot(), _handleSuspendTraversal );

      // Ensure body events were removed.
      _bodyDom.removeEventListener( 'mousemove', _handleMove );
      _bodyDom.removeEventListener( 'mouseleave', _handleMove );
      // Clear active menu.
      _activeMenu = null;
      _suspended = true;
    }

    return _suspended;
  }

  /**
   * Iterate over the sub menus and handle setting the resumed state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleResumeTraversal( node ) {
    const nLevel = node.level;
    const menu = node.data;

    if ( nLevel === 1 ) {
      const wrapperSel = '.o-mega-menu_content-2-wrapper';
      const contentDom = menu.getDom().content;
      const wrapperDom = contentDom.querySelector( wrapperSel );
      let transition = menu.getTransition();

      // This ensures the transition has been removed by MegaMenuMobile.
      transition = _setTransitionElement( wrapperDom, transition );
      transition.moveUp();

      /* TODO: The only reason hiding is necessary is that the
         drop-shadow of the menu extends below its border,
         so it's still visible when the menu slides -100% out of view.
         Investigate whether it would be better to have a u-move-up-1_1x
         or similar class to move up -110%. Or whether the drop-shadow
         could be included within the bounds of the menu. */
      menu.getDom().content.classList.add( 'u-invisible' );
      menu.setExpandTransition( transition, transition.moveToOrigin );
      menu.setCollapseTransition( transition, transition.moveUp );

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
    } else if ( nLevel === 2 ) {
      menu.suspend();
    }
  }

  /**
   * Iterate over the sub menus and handle setting the suspended state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleSuspendTraversal( node ) {
    const nLevel = node.level;
    const menu = node.data;

    if ( nLevel === 1 ) {
      menu.clearTransitions();
      menu.getDom().content.classList.remove( 'u-invisible' );

      if ( menu.isExpanded() ) {
        menu.collapse();
      }
    } else if ( nLevel === 2 ) {
      menu.resume();
    }
  }

  /**
   * Set an element on an existing transition or create a new transition.
   * @param {HTMLNode} element - Target of a transition.
   * @param {MoveTransition} [setTransition] - The transition to apply.
   * @returns {MoveTransition}
   *   The passed in transition or a new transition if none was supplied.
   */
  function _setTransitionElement( element, setTransition ) {
    let transition = setTransition;
    if ( transition ) {
      transition.setElement( element );
    } else {
      transition = new MoveTransition( element ).init();
    }

    return transition;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.handleEvent = handleEvent;
  this.init = init;
  this.resume = resume;
  this.suspend = suspend;

  return this;
}

export default MegaMenuDesktop;
