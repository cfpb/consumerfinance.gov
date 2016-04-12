'use strict';

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );
var MoveTransition = require( '../modules/transition/MoveTransition' );
var treeTraversal = require( '../modules/util/tree-traversal' );

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
  var _bodyDom = document.body;

  // Binded functions.
  var _handleTriggerClickBinded = _handleTriggerClick.bind( this );
  var _handleTriggerOverBinded = _handleTriggerOver.bind( this );
  var _handleExpandBeginBinded = _handleExpandBegin.bind( this );
  var _handleCollapseEndBinded = _handleCollapseEnd.bind( this );

  // Tree model.
  var _menus = menus;

  //  Currently showing menu picked from the tree.
  var _activeMenu = null;

  // Whether this instance's behaviors are suspended or not.
  var _suspended = true;

  /**
   * @returns {MegaMenuDesktop} An instance.
   */
  function init() {

    return this;
  }

  /**
   * Pass an event bubbled up from the menus to the appropriate handler.
   * @param {Event} event - A FlyoutMenu event.
   */
  function handleEvent( event ) {
    if ( _suspended ) return;
    var eventMap = {
      triggerClick: _handleTriggerClickBinded,
      triggerOver:  _handleTriggerOverBinded,
      expandBegin:  _handleExpandBeginBinded,
      collapseEnd:  _handleCollapseEndBinded
    };

    var currHandler = eventMap[event.type];
    if ( currHandler ) currHandler( event );
  }

  /**
   * Event handler for when FlyoutMenu trigger is clicked.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerClick( event ) {
    this.dispatchEvent( 'triggerClick', { target: this } );
    var menu = event.target;
    if ( !menu.isAnimating() ) {
      if ( _activeMenu === null ) {
        // A menu is opened.
        _activeMenu = menu;
        _activeMenu.getTransition().animateOn();
        // TODO: Investigate whether mouseout event may be able to be used
        //       instead of mousemove.
        _bodyDom.addEventListener( 'mousemove', _handleMove );
        _bodyDom.addEventListener( 'mouseleave', _handleMove );
      } else if ( _activeMenu === menu ) {
        // A menu is closed.
        _activeMenu.getTransition().animateOn();
        _activeMenu = null;
        _bodyDom.removeEventListener( 'mousemove', _handleMove );
        _bodyDom.removeEventListener( 'mouseleave', _handleMove );
      } else {
        // An open menu has switched to another menu.
        _activeMenu.getTransition().animateOff();
        _activeMenu.collapse();
        _activeMenu = event.target;
        _activeMenu.getTransition().animateOff();
      }
    }
  }

  /**
   * Event handler for when FlyoutMenu expand transition begins.
   * Use this to perform post-expandBegin actions.
   */
  function _handleExpandBegin() {
    this.dispatchEvent( 'expandBegin', { target: this } );

    // Set keyboard focus on first menu item link.
    var activeMenuDom = _activeMenu.getDom().content;
    activeMenuDom.classList.remove( 'u-invisible' );
    // TODO: Remove or uncomment when keyboard navigation is in.
    // var firstMenuLink = activeMenuDom.querySelector( 'a' );
    // firstMenuLink.focus();
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
   * Event handler for when FlyoutMenu trigger is hovered over.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleTriggerOver( event ) {
    this.dispatchEvent( 'triggerOver', { target: this } );
    var menu = event.target;
    var level = menu.getData().level;

    // Only trigger a click when rolling over the level one
    // menu items when in the desktop view.
    if ( level === 1 && _activeMenu !== menu ) {
      menu.getDom().trigger.click();
    }
  }

  /**
   * Event handler for when mouse is hovering.
   * @param {MouseEvent} event - The hovering event.
   */
  function _handleMove( event ) {
    var menu = event.target;

    if ( !_activeMenu.getDom().container.parentNode.contains( menu ) ) {
      _activeMenu.getDom().trigger.click();
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
      _suspended = true;
    }

    return _suspended;
  }

  /**
   * Iterate over the sub menus and handle setting the resumed state.
   * @param {TreeNode} node - The data source for the current menu.
   */
  function _handleResumeTraversal( node ) {
    var nLevel = node.level;
    var menu = node.data;

    if ( nLevel === 1 ) {
      var wrapperSel = '.o-mega-menu_content-2-wrapper';
      var contentDom = menu.getDom().content;
      var wrapperDom = contentDom.querySelector( wrapperSel );
      var transition = menu.getTransition();

      // This checks if the transition has been removed by MegaMenuMobile.
      transition = _setTransitionElement( wrapperDom, transition );
      transition.moveUp();

      // TODO: The only reason hiding is necessary is that the
      //       drop-shadow of the menu extends below its border,
      //       so it's still visible when the menu slides -100% out of view.
      //       Investigate whether it would be better to have a u-move-up-1_1x
      //       or similar class to move up -110%. Or whether the drop-shadow
      //       could be included within the bounds of the menu.
      menu.getDom().content.classList.add( 'u-invisible' );
      menu.setExpandTransition( transition, transition.moveToOrigin );
      menu.setCollapseTransition( transition, transition.moveUp );

      // TODO: Investigate whether deferred collapse has another solution.
      //       This check is necessary since a call to an already collapsed
      //       menu will set a deferred collapse that will be called
      //       on expandEnd next time the flyout is expanded.
      //       The deferred collapse is used in cases where the
      //       user clicks the flyout menu while it is animating open,
      //       so that it appears like they can collapse it, even when
      //       clicking during the expand animation.
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
    var nLevel = node.level;
    var menu = node.data;

    if ( nLevel === 1 ) {
      var transition = menu.getTransition();
      transition.remove();
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
    var transition = setTransition;
    if ( transition ) {
      transition.setElement( element );
    } else {
      transition = new MoveTransition( element ).init();
    }

    return transition;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.handleEvent = handleEvent;
  this.init = init;
  this.resume = resume;
  this.suspend = suspend;

  return this;
}

module.exports = MegaMenuDesktop;
