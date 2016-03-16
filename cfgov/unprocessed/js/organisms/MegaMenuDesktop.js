'use strict';

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );

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
    if ( !_suspended ) {
      if ( event.type === 'triggerClick' ) {
        _handleTriggerClickBinded( event );
      } else if ( event.type === 'triggerOver' ) {
        _handleTriggerOverBinded( event );
      } else if ( event.type === 'expandBegin' ) {
        _handleExpandBeginBinded( event );
      } else if ( event.type === 'collapseEnd' ) {
        _handleCollapseEndBinded( event );
      }
    }
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
      var level2 = _menus.getAllAtLevel( 1 );
      var menu;
      var contentDom;
      var wrapperDom;
      var transition;
      var wrapperSel = '.o-mega-menu_content-2-wrapper';
      for ( var i = 0, len = level2.length; i < len; i++ ) {
        menu = level2[i].data;
        contentDom = menu.getDom().content;
        wrapperDom = contentDom.querySelector( wrapperSel );
        transition = menu.getTransition();
        transition.setElement( wrapperDom );
        transition.moveUp();
        // TODO: The only reason hiding is necessary is that the
        //       drop-shadow of the menu extends below it border,
        //       so it's still visible when the menu slides -100% out of view.
        //       Investigate whether it would be better to have a u-move-up-1_1x
        //       or similar class to move up -110%. Or whether the drop-shadow
        //       could be included within the bounds of the menu.
        menu.getDom().content.classList.add( 'u-invisible' );
        menu.setExpandTransition( transition, transition.moveToOrigin );
        menu.setCollapseTransition( transition, transition.moveUp );
        menu.collapse();
      }

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
      var level2 = _menus.getAllAtLevel( 1 );
      var menu;
      var transition;
      for ( var i = 0, len = level2.length; i < len; i++ ) {
        menu = level2[i].data;
        transition = menu.getTransition();
        transition.remove();
        menu.getDom().content.classList.remove( 'u-invisible' );
      }

      _suspended = true;
    }

    return _suspended;
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
