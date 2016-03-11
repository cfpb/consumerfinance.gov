'use strict';

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );
var MoveTransition = require( '../modules/transition/MoveTransition' );
var treeTraversal = require( '../modules/util/tree-traversal' );

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
  var _bodyDom = document.body;

  // Binded functions.
  var _handleExpandBeginBinded = _handleExpandBegin.bind( this );
  var _handleCollapseBeginBinded = _handleCollapseBegin.bind( this );
  var _handleCollapseEndBinded = _handleCollapseEnd.bind( this );

  // Tree model.
  var _menus = menus;

  var _rootMenu;

  //  Currently showing menu picked from the tree.
  var _activeMenu = null;
  var _activeMenuDom;

  // Whether this instance's behaviors are suspended or not.
  var _suspended = true;

  /**
   * @returns {MegaMenuMobile} An instance.
   */
  function init() {

    var rootNode = _menus.getRoot();
    _rootMenu = rootNode.data;
    _activeMenu = _rootMenu;
    _activeMenuDom = _rootMenu.getDom().content;

    return this;
  }

  function _setTransition( node ) {
    var menu = node.data;
    var transition = new MoveTransition( menu.getDom().content ).init();
    menu.setExpandTransition( transition, transition.moveToOrigin );
    menu.setCollapseTransition( transition, transition.moveLeft );
    menu.collapse();
    transition.moveLeft();
  }

  /**
   * Event handler for when there's a click on the page's body.
   * Used to close the global search, if needed.
   * @param {MouseEvent} event The event object for the mousedown event.
   */
  function _handleBodyClick( event ) {
    var target = event.target;
    if ( _activeMenu.getDom().trigger === target ) {
      return;
    }

    if ( !_rootMenu.getDom().container.contains( target ) ) {
      _rootMenu.collapse();
      _activeMenu.collapse();
    }
  }

  /**
   * Pass an event bubbled up from the menus to the appropriate handler.
   * @param {Event} event - A FlyoutMenu event.
   */
  function handleEvent( event ) {
    if ( !_suspended ) {
      if ( event.type === 'expandBegin' ) {
        _handleExpandBeginBinded( event );
      } else if ( event.type === 'collapseBegin' ) {
        _handleCollapseBeginBinded( event );
      } else if ( event.type === 'collapseEnd' ) {
        _handleCollapseEndBinded( event );
      }
    }
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
    var menu = event.target;
    _handleToggle( menu );
    if ( menu === _rootMenu ) {
      this.dispatchEvent( 'rootExpandBegin', { target: this } );
    }
    // If on a submenu, focus the back button, otherwise focus the first link.
    var firstMenuLink;
    if ( _activeMenu === _rootMenu ) {
      firstMenuLink = _activeMenuDom.querySelector( 'a' );
    } else {
      firstMenuLink = _activeMenuDom.querySelector( 'button' );
    }

    firstMenuLink.focus();
    document.body.addEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has begun.
   * Use this to perform post-collapseBegin actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseBegin( event ) {
    _handleToggle( event.target );
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Event handler for when FlyoutMenu collapse transition has ended.
   * Use this to perform post-collapseEnd actions.
   * @param {Event} event - A FlyoutMenu event.
   */
  function _handleCollapseEnd( event ) {
    if ( event.target === _rootMenu ) {
      this.dispatchEvent( 'rootCollapseEnd', { target: this } );
    }
    document.body.removeEventListener( 'mousedown', _handleBodyClick );
  }

  /**
   * Close the mega menu.
   * @returns {MegaMenuMobile} A instance.
   */
  function collapse() {

    // TODO: Combine with `resume` implementation.
    treeTraversal.bfs( _menus.getRoot(), function( node ) {
      var menu = node.data;
      menu.collapse();
    } );

    return this;
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function resume() {
    if ( _suspended ) {
      treeTraversal.bfs( _menus.getRoot(), _setTransition );
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
      _menus.getRoot().data.getTransition().remove();

      // TODO: Update this to close the menus directly
      //       so `_handleCollapseEnd` is fired.
      this.dispatchEvent( 'rootCollapseEnd', { target: this } );
      document.body.removeEventListener( 'mousedown', _handleBodyClick );

      _suspended = true;
    }

    return _suspended;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
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
