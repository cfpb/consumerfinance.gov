'use strict';

// Required modules.
var BaseTransition = require( '../../modules/transition/BaseTransition' );
var behavior = require( '../../modules/util/behavior' );
var breakpointState = require( '../../modules/util/breakpoint-state' );
var EventObserver = require( '../../modules/util/EventObserver' );
var fnBind = require( '../../modules/util/fn-bind' ).fnBind;
var standardType = require( '../../modules/util/standard-type' );

/**
 * FlyoutMenu
 * @class
 *
 * @classdesc Initializes new FlyoutMenu behavior.
 * Behaviors are functionality that can be shared between different pieces
 * of markup. They are not strictly atomic, though they likely are used
 * on atomic components.
 * As added JS behavior, this is added through HTML data-js-hook attributes.
 *
 * Structure is:
 * behavior_flyout-menu
 *   behavior_flyout-menu_trigger
 *   behavior_flyout-menu_content
 *     behavior_flyout-menu_alt-trigger
 *
 * The alt-trigger is for a back button, which may obscure the first trigger.
 * The flyout can be triggered three ways: through a click of the trigger or
 * through the click of an alt-trigger.
 *
 * @param {HTMLNode} element - The DOM element to attach FlyoutMenu behavior.
 * @returns {FlyoutMenu} An instance.
 */
function FlyoutMenu( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

  var BASE_CLASS = standardType.BEHAVIOR_PREFIX + 'flyout-menu';
  var SEL_PREFIX = '[' + standardType.JS_HOOK + '=' + BASE_CLASS;
  var BASE_SEL = SEL_PREFIX + ']';

  // Verify that the expected dom attributes are present.
  var _dom = behavior.checkBehaviorDom( element, BASE_CLASS );
  var _triggerDom = behavior.checkBehaviorDom( element, BASE_CLASS + '_trigger' );
  var _contentDom = behavior.checkBehaviorDom( element, BASE_CLASS + '_content' );

  var _altTriggerDom = _dom.querySelector( SEL_PREFIX + '_alt-trigger]' );

  var _isExpanded = false;
  var _isAnimating = false;

  var _expandTransition;
  var _expandTransitionMethod;
  var _expandTransitionMethodArgs = [];

  var _collapseTransition;
  var _collapseTransitionMethod;
  var _collapseTransitionMethodArgs = [];

  // Binded events.
  var _collapseBinded = fnBind( collapse, this );
  // Needed to add and remove events to transitions.
  var _collapseEndBinded = fnBind( _collapseEnd, this );
  var _expandEndBinded = fnBind( _expandEnd, this );

  // If this menu appears in a data source,
  // this can be used to store the source.
  // Examples include the index in an Array,
  // a key in an Hash, or a node in a Tree.
  var _data;

  // Set this function to a queued collapse function,
  // which is called if collapse is called while
  // expand is animating.
  var _deferFunct = standardType.noopFunct;

  // Whether this instance's behaviors are suspended or not.
  var _suspended = true;

  // Event immediately preceeding mouseover is touchstart,
  // if that event's present we'll want to ignore mouseover
  // to avoid a mouseover and click immediately after each other.
  var _touchTriggered = false;

  // TODO: Add param to set the FlyoutMenu open at initialization-time.
  /**
   * @returns {FlyoutMenu} An instance.
   */
  function init() {
    // Ignore Google Analytics on the trigger if it is a link,
    // since we're preventing the default link behavior.
    if ( _triggerDom.tagName === 'A' && _isInMobile() ) {
      _triggerDom.setAttribute( 'data-gtm_ignore', 'true' );
    }

    var handleTriggerClickedBinded = fnBind( _handleTriggerClicked, this );
    var handleTriggerOverBinded = fnBind( _handleTriggerOver, this );
    var handleTriggerOutBinded = fnBind( _handleTriggerOut, this );

    // Set initial aria attributes to false.
    _setAriaAttr( 'expanded', _triggerDom, 'false' );
    _setAriaAttr( 'pressed', _triggerDom, 'false' );

    _triggerDom.addEventListener( 'click', handleTriggerClickedBinded );
    _triggerDom.addEventListener( 'touchstart', _handleTouchStart );
    _triggerDom.addEventListener( 'mouseover', handleTriggerOverBinded );
    _triggerDom.addEventListener( 'mouseout', handleTriggerOutBinded );

    if ( _altTriggerDom ) {
      // If menu contains a submenu but doesn't have
      // its own alternative trigger (such as a Back button),
      // then the altTriggerDom may be in the submenu and we
      // need to remove the reference.
      var subMenu = _dom.querySelector( BASE_SEL );
      if ( subMenu && subMenu.contains( _altTriggerDom ) ) {
        _altTriggerDom = null;
      } else {
        // TODO: Investigate just having multiple triggers,
        //       instead of a primary and alternative.
        // Ignore Google Analytics on the trigger if it is a link,
        // since we're preventing the default link behavior.
        if ( _altTriggerDom.tagName === 'A' && _isInMobile() ) {
          _altTriggerDom.setAttribute( 'data-gtm_ignore', 'true' );
        }

        // Set initial aria attributes to false.
        _setAriaAttr( 'expanded', _altTriggerDom, 'false' );

        // TODO: alt trigger should probably listen
        //       for a mouseover/mouseout event too.
        _altTriggerDom.addEventListener( 'click', handleTriggerClickedBinded );
      }
    }

    resume();

    return this;
  }

  /**
   * Set an aria attribute on an HTML element.
   * @param {string} type - The aria attribute to set
   *   (without the aria- prefix).
   * @param {HTMLNode} elem - The element to set.
   * @param {boolean} value - The value to set on `aria-expanded`,
   *   casts to a string.
   * @returns {string} The cast value.
   */
  function _setAriaAttr( type, elem, value ) {
    var strValue = String( value );
    elem.setAttribute( 'aria-' + type, strValue );
    return strValue;
  }

  /**
   * Event handler for when the search input trigger is touched.
   */
  function _handleTouchStart() {
    _touchTriggered = true;
  }

  /**
   * Event handler for when the trigger is hovered over.
   */
  function _handleTriggerOver() {
    if ( !_touchTriggered && !_suspended ) {
      this.dispatchEvent( 'triggerOver',
                          { target: this, type: 'triggerOver' } );
    }
    _touchTriggered = false;
  }

  /**
   * Event handler for when the trigger is hovered out.
   */
  function _handleTriggerOut() {
    if ( !_suspended ) {
      this.dispatchEvent( 'triggerOut',
                          { target: this, type: 'triggerOut' } );
    }
  }

  /**
   * Event handler for when the search input trigger is clicked,
   * which opens/closes the search input.
   * @param {MouseEvent} event - The flyout trigger was clicked.
   */
  function _handleTriggerClicked( event ) {
    if ( !_suspended ) {
      this.dispatchEvent( 'triggerClick',
                          { target: this, type: 'triggerClick' } );
      event.preventDefault();
      if ( _isExpanded ) {
        this.collapse();
      } else {
        this.expand();
      }
    }
  }

  // TODO: Move this to breakpoint-state.js.
  /**
   * Whether currently in the desktop view.
   * @returns {boolean} True if in the desktop view, otherwise false.
   */
  function _isInMobile() {
    var isInMobile = false;
    var currentBreakpoint = breakpointState.get();
    if ( currentBreakpoint.isBpXS ) {
      isInMobile = true;
    }
    return isInMobile;
  }

  /**
   * Open the search box.
   * @returns {FlyoutMenu} An instance.
   */
  function expand() {
    if ( !_isExpanded && !_isAnimating ) {
      _isAnimating = true;
      _deferFunct = standardType.noopFunct;
      this.dispatchEvent( 'expandBegin',
                          { target: this, type: 'expandBegin' } );
      _setAriaAttr( 'pressed', _triggerDom, true );
      if ( _expandTransitionMethod ) {
        var hasTransition = _expandTransition &&
                            _expandTransition.isAnimated();
        if ( hasTransition ) {
          _expandTransition
            .addEventListener( BaseTransition.END_EVENT, _expandEndBinded );
        }
        _expandTransitionMethod
          .apply( _expandTransition, _expandTransitionMethodArgs );
        if ( !hasTransition ) {
          _expandEndBinded();
        }
      } else {
        _expandEndBinded();
      }
    }

    return this;
  }

  /**
   * Close the search box.
   * If collapse is called when expand animation is underway,
   * save a deferred call to collapse, which is called when
   * expand completes.
   * @returns {FlyoutMenu} An instance.
   */
  function collapse() {
    if ( _isExpanded && !_isAnimating ) {
      _deferFunct = standardType.noopFunct;
      _isAnimating = true;
      _isExpanded = false;
      this.dispatchEvent( 'collapseBegin',
                          { target: this, type: 'collapseBegin' } );
      if ( _collapseTransitionMethod ) {
        var hasTransition = _collapseTransition &&
                            _collapseTransition.isAnimated();
        if ( hasTransition ) {
          _collapseTransition
            .addEventListener( BaseTransition.END_EVENT, _collapseEndBinded );
        }
        _collapseTransitionMethod
          .apply( _collapseTransition, _collapseTransitionMethodArgs );
        if ( !hasTransition ) {
          _collapseEndBinded();
        }
      } else {
        _collapseEndBinded();
      }

      if ( _altTriggerDom ) {
        _setAriaAttr( 'expanded', _altTriggerDom, false );
      }

      _setAriaAttr( 'expanded', _triggerDom, false );
      _setAriaAttr( 'pressed', _triggerDom, false );
      _setAriaAttr( 'expanded', _contentDom, false );
      // TODO: Remove or uncomment when keyboard navigation is in.
      // _triggerDom.focus();
    } else {
      _deferFunct = _collapseBinded;
    }

    return this;
  }

  /**
   * Expand animation has completed.
   * Call deferred collapse function,
   * if set (otherwise it will call a noop function).
   */
  function _expandEnd() {
    _isAnimating = false;
    _isExpanded = true;
    if ( _expandTransition ) {
      _expandTransition
        .removeEventListener( BaseTransition.END_EVENT, _expandEndBinded );
    }
    this.dispatchEvent( 'expandEnd', { target: this, type: 'expandEnd' } );
    if ( _altTriggerDom ) {
      _setAriaAttr( 'expanded', _altTriggerDom, true );
    }
    _setAriaAttr( 'expanded', _triggerDom, true );
    _setAriaAttr( 'expanded', _contentDom, true );
    // Call collapse, if it was called while expand was animating.
    _deferFunct();
  }

  /**
   * Collapse animation has completed.
   */
  function _collapseEnd() {
    _isAnimating = false;
    if ( _collapseTransition ) {
      _collapseTransition
        .removeEventListener( BaseTransition.END_EVENT, _collapseEndBinded );
    }
    this.dispatchEvent( 'collapseEnd', { target: this, type: 'collapseEnd' } );
  }

  /**
   * @param {MoveTransition|AlphaTransition} transition
   *   A transition instance to watch for events on.
   * @param {Function} method
   *   The transition method to call on expand.
   * @param {Array} [args]
   *   List of arguments to apply to collapse method.
   */
  function setExpandTransition( transition, method, args ) {
    _expandTransition = transition;
    _expandTransitionMethod = method;
    _expandTransitionMethodArgs = args;
  }

  /**
   * @param {MoveTransition|AlphaTransition} transition
   *   A transition instance to watch for events on.
   * @param {Function} method
   *   The transition method to call on collapse.
   * @param {Array} [args]
   *   List of arguments to apply to collapse method.
   */
  function setCollapseTransition( transition, method, args ) {
    _collapseTransition = transition;
    _collapseTransitionMethod = method;
    _collapseTransitionMethodArgs = args;
  }

  /**
   * Clear the transitions attached to this FlyoutMenu instance.
   */
  function clearTransitions() {
    var transition = getTransition( FlyoutMenu.EXPAND_TYPE );
    if ( transition ) { transition.remove(); }
    transition = getTransition( FlyoutMenu.COLLAPSE_TYPE );
    if ( transition ) { transition.remove(); }

    _expandTransition = standardType.UNDEFINED;
    _expandTransitionMethod = standardType.UNDEFINED;
    _expandTransitionMethodArgs = [];

    _collapseTransition = standardType.UNDEFINED;
    _collapseTransitionMethod = standardType.UNDEFINED;
    _collapseTransitionMethodArgs = [];
  }

  /**
   * @param {string} [type]
   *   The type of transition to return.
   *   Accepts 'expand' or 'collapse'.
   *   `FlyoutMenu.EXPAND_TYPE` and `FlyoutMenu.COLLAPSE_TYPE` can be used
   *   as type-safe constants passed into this method.
   *   If neither or something else is supplied, expand type is returned.
   * @returns {MoveTransition|AlphaTransition|undefined}
   *   A transition instance set on this instance, or undefined if none is set.
   */
  function getTransition( type ) {
    if ( type === FlyoutMenu.COLLAPSE_TYPE ) {
      return _collapseTransition;
    }

    return _expandTransition;
  }

  /**
   * @returns {Object}
   *   Hash of trigger, alternative trigger, and content DOM references.
   */
  function getDom() {
    return {
      altTrigger: _altTriggerDom,
      container:  _dom,
      content:    _contentDom,
      trigger:    _triggerDom
    };
  }

  /**
   * Enable broadcasting of trigger events.
   * @returns {boolean} True if resumed, false otherwise.
   */
  function resume() {
    if ( _suspended ) {
      _suspended = false;
    }

    return !_suspended;
  }

  /**
   * Suspend broadcasting of trigger events.
   * @returns {boolean} True if suspended, false otherwise.
   */
  function suspend() {
    if ( !_suspended ) {
      _suspended = true;
    }

    return _suspended;
  }

  // TODO: Use Object.defineProperty to create a getter/setter.
  //       See https://github.com/cfpb/cfgov-refresh/pull/1566/
  //           files#diff-7a844d22219d7d3db1fa7c1e70d7ba45R35
  /**
   * @returns {number|string|Object} A data identifier such as an Array index,
   *   Hash key, or Tree node.
   */
  function getData() {
    return _data;
  }

  /**
   * @param {number|string|Object} data
   *   A data identifier such as an Array index, Hash key, or Tree node.
   * @returns {FlyoutMenu} An instance.
   */
  function setData( data ) {
    _data = data;

    return this;
  }

  /**
   * @returns {boolean} True if menu is animating, false otherwise.
   */
  function isAnimating() {
    return _isAnimating;
  }

  /**
   * @returns {boolean} True if menu is expanded, false otherwise.
   */
  function isExpanded() {
    return _isExpanded;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.expand = expand;
  this.collapse = collapse;
  this.setExpandTransition = setExpandTransition;
  this.setCollapseTransition = setCollapseTransition;
  this.clearTransitions = clearTransitions;
  this.getData = getData;
  this.getTransition = getTransition;
  this.getDom = getDom;
  this.isAnimating = isAnimating;
  this.isExpanded = isExpanded;
  this.resume = resume;
  this.setData = setData;
  this.suspend = suspend;

  // Public static properties.
  FlyoutMenu.EXPAND_TYPE = 'expand';
  FlyoutMenu.COLLAPSE_TYPE = 'collapse';
  FlyoutMenu.BASE_CLASS = BASE_CLASS;

  return this;
}

module.exports = FlyoutMenu;
