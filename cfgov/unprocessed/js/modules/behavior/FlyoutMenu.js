// Required modules.
import * as breakpointState from '../../modules/util/breakpoint-state';
import {
  BEHAVIOR_PREFIX,
  JS_HOOK,
  noopFunct
} from '../../modules/util/standard-type';
import BaseTransition from '../../modules/transition/BaseTransition';
import EventObserver from '../../modules/util/EventObserver';
import { checkBehaviorDom } from '../../modules/util/behavior';

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

  const BASE_CLASS = BEHAVIOR_PREFIX + 'flyout-menu';
  const SEL_PREFIX = '[' + JS_HOOK + '=' + BASE_CLASS;
  const BASE_SEL = SEL_PREFIX + ']';

  // Verify that the expected dom attributes are present.
  const _dom = checkBehaviorDom( element, BASE_CLASS );
  const _triggerDom = checkBehaviorDom( element, BASE_CLASS + '_trigger' );
  const _contentDom = checkBehaviorDom( element, BASE_CLASS + '_content' );

  let _altTriggerDom = _dom.querySelector( SEL_PREFIX + '_alt-trigger]' );

  let _isExpanded = false;
  let _isAnimating = false;

  let _expandTransition;
  let _expandTransitionMethod;
  let _expandTransitionMethodArgs = [];

  let _collapseTransition;
  let _collapseTransitionMethod;
  let _collapseTransitionMethodArgs = [];

  // Binded events.
  const _collapseBinded = collapse.bind( this );
  // Needed to add and remove events to transitions.
  const _collapseEndBinded = _collapseEnd.bind( this );
  const _expandEndBinded = _expandEnd.bind( this );

  /* If this menu appears in a data source,
     this can be used to store the source.
     Examples include the index in an Array,
     a key in an Hash, or a node in a Tree. */
  let _data;

  /* Set this function to a queued collapse function,
     which is called if collapse is called while
     expand is animating. */
  let _deferFunct = noopFunct;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  /* Event immediately preceeding mouseover is touchstart,
     if that event's present we'll want to ignore mouseover
     to avoid a mouseover and click immediately after each other. */
  let _touchTriggered = false;

  // TODO: Add param to set the FlyoutMenu open at initialization-time.
  /**
   * @returns {FlyoutMenu} An instance.
   */
  function init() {

    /* Ignore Google Analytics on the trigger if it is a link,
       since we're preventing the default link behavior. */
    if ( _triggerDom.tagName === 'A' && _isInMobile() ) {
      _triggerDom.setAttribute( 'data-gtm_ignore', 'true' );
    }

    const handleTriggerClickedBinded = _handleTriggerClicked.bind( this );
    const handleTriggerOverBinded = _handleTriggerOver.bind( this );
    const handleTriggerOutBinded = _handleTriggerOut.bind( this );

    // Set initial aria attributes to false.
    _setAriaAttr( 'expanded', _triggerDom, 'false' );

    _triggerDom.addEventListener( 'click', handleTriggerClickedBinded );
    _triggerDom.addEventListener( 'touchstart', _handleTouchStart );
    _triggerDom.addEventListener( 'mouseover', handleTriggerOverBinded );
    _triggerDom.addEventListener( 'mouseout', handleTriggerOutBinded );

    if ( _altTriggerDom ) {

      /* If menu contains a submenu but doesn't have
         its own alternative trigger (such as a Back button),
         then the altTriggerDom may be in the submenu and we
         need to remove the reference. */
      const subMenu = _dom.querySelector( BASE_SEL );
      if ( subMenu && subMenu.contains( _altTriggerDom ) ) {
        _altTriggerDom = null;
      } else {

        /* TODO: Investigate just having multiple triggers,
           instead of a primary and alternative.
           Ignore Google Analytics on the trigger if it is a link,
           since we're preventing the default link behavior. */
        if ( _altTriggerDom.tagName === 'A' && _isInMobile() ) {
          _altTriggerDom.setAttribute( 'data-gtm_ignore', 'true' );
        }

        // Set initial aria attributes to false.
        _setAriaAttr( 'expanded', _altTriggerDom, 'false' );

        /* TODO: alt trigger should probably listen
           for a mouseover/mouseout event too. */
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
    const strValue = String( value );
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
      this.dispatchEvent(
        'triggerOver',
        { target: this, type: 'triggerOver' }
      );
    }
    _touchTriggered = false;
  }

  /**
   * Event handler for when the trigger is hovered out.
   */
  function _handleTriggerOut() {
    if ( !_suspended ) {
      this.dispatchEvent(
        'triggerOut',
        { target: this, type: 'triggerOut' }
      );
    }
  }

  /**
   * Event handler for when the search input trigger is clicked,
   * which opens/closes the search input.
   * @param {MouseEvent} event - The flyout trigger was clicked.
   */
  function _handleTriggerClicked( event ) {
    if ( !_suspended ) {
      this.dispatchEvent(
        'triggerClick',
        { target: this, type: 'triggerClick' }
      );
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
    let isInMobile = false;
    const currentBreakpoint = breakpointState.get();
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
      _deferFunct = noopFunct;
      this.dispatchEvent(
        'expandBegin',
        { target: this, type: 'expandBegin' }
      );

      if ( _expandTransitionMethod ) {
        const hasTransition = _expandTransition &&
                              _expandTransition.isAnimated();
        if ( hasTransition ) {
          _expandTransition.addEventListener(
            BaseTransition.END_EVENT,
            _expandEndBinded
          );
        }
        _expandTransitionMethod.apply(
          _expandTransition,
          _expandTransitionMethodArgs
        );
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
      _deferFunct = noopFunct;
      _isAnimating = true;
      _isExpanded = false;
      this.dispatchEvent(
        'collapseBegin',
        { target: this, type: 'collapseBegin' }
      );
      if ( _collapseTransitionMethod ) {
        const hasTransition = _collapseTransition &&
                              _collapseTransition.isAnimated();
        if ( hasTransition ) {
          _collapseTransition.addEventListener(
            BaseTransition.END_EVENT,
            _collapseEndBinded
          );
        }
        _collapseTransitionMethod.apply(
          _collapseTransition,
          _collapseTransitionMethodArgs
        );
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
      _setAriaAttr( 'expanded', _contentDom, false );

      /* TODO: Remove or uncomment when keyboard navigation is in.
         _triggerDom.focus(); */
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
      _expandTransition.removeEventListener(
        BaseTransition.END_EVENT,
        _expandEndBinded
      );
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
      _collapseTransition.removeEventListener(
        BaseTransition.END_EVENT,
        _collapseEndBinded
      );
    }
    this.dispatchEvent( 'collapseEnd', { target: this, type: 'collapseEnd' } );
  }

  /**
   * @param {MoveTransition|AlphaTransition} transition
   *   A transition instance to watch for events on.
   * @param {Function} method
   *   The transition method to call on expand.
   * @param {Array} [args]
   *   List of arguments to apply to expand method.
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
    let transition = getTransition( FlyoutMenu.EXPAND_TYPE );
    if ( transition ) { transition.remove(); }
    transition = getTransition( FlyoutMenu.COLLAPSE_TYPE );
    if ( transition ) { transition.remove(); }

    let UNDEFINED;

    _expandTransition = UNDEFINED;
    _expandTransitionMethod = UNDEFINED;
    _expandTransitionMethodArgs = [];

    _collapseTransition = UNDEFINED;
    _collapseTransitionMethod = UNDEFINED;
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

  /* TODO: Use Object.defineProperty to create a getter/setter.
     See https://github.com/cfpb/cfgov-refresh/pull/1566/
     files#diff-7a844d22219d7d3db1fa7c1e70d7ba45R35 */
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
  const eventObserver = new EventObserver();
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

export default FlyoutMenu;
