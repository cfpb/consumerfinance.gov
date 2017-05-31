'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var breakpointState = require( '../modules/util/breakpoint-state' );
var EventObserver = require( '../modules/util/EventObserver' );
var fnBind = require( '../modules/util/fn-bind' ).fnBind;
var standardType = require( '../modules/util/standard-type' );

/**
 * Expandable
 * @class
 *
 * @classdesc Initializes a new Expandable molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Object} An Expandable instance.
 */
function Expandable( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  var BASE_CLASS = 'o-expandable';

  // Bitwise flags for the state of this Expandable.
  var COLLAPSED = 0;
  var COLLAPSING = 1;
  var EXPANDING = 2;
  var EXPANDED = 3;

  // The Expandable element will directly be the Expandable
  // when used in an ExpandableGroup, otherwise it can be the parent container.
  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
  var _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  var _contentAnimated =
    _content.querySelector( '.' + BASE_CLASS + '_content-animated' );
  var _link = _dom.querySelector( '.' + BASE_CLASS + '_link' );

  var _state = COLLAPSED;
  var _transitionEndEvent = _getTransitionEndEvent( _content );
  var _transitionPrefix = _getTransitionPrefix( _transitionEndEvent );
  var _contentHeight;

  // TODO: Replace function of _that with Function.prototype.bind.
  var _that = this;
  var _collapseBinded = fnBind( collapse, this );
  var _expandBinded = fnBind( expand, this );

  // Reference to MutationObserver for watching DOM changes within the content.
  // No-op Function for MutationObserver.disconnect() is set in case destroy()
  // is called on a DOM node that was copied with the atomic init flag set,
  // implying it had been initialized when it hadn't.
  var _observer = { disconnect: standardType.noopFunct };

  /**
   * @param {number} state
   *   Allows passing of EXPANDED flag to set expanded state.
   * @returns {Expandable|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init( state ) {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }
    _calcHeight();
    // Even if expanded is set, don't expand if in mobile window size.
    if ( !_isInMobile() &&
         ( state === EXPANDED ||
         _dom.getAttribute( 'data-state' ) === 'expanded' ) ) {
      // If expanded by default, we need to set the height inline so the
      // inline transition to collapse the Expandable works.
      // TODO: Handle issue of height calculating before
      //       web fonts have loaded and changed height.
      _setMaxHeight();
      _setExpandedState();
    } else {
      _setCollapsedState();
    }

    // Show the show/hide links, which otherwise are hidden if JS is off.
    _link.classList.remove( 'u-hidden' );

    _target.addEventListener( 'click', _handleClick );

    if ( !_dom.getAttribute( 'data-read-more' ) ) {
      window.addEventListener( 'resize', _resizeHandler );
    }

    _initObserver();

    return this;
  }

  /**
   * Reverse a call to init() to teardown an instance initialization.
   * @returns {Expandable} An instance.
   */
  function destroy() {
    if ( atomicHelpers.destroyInitFlag( _dom ) ) {
      _target.removeEventListener( 'click', _handleClick );
      window.removeEventListener( 'resize', _resizeHandler );
      _content.removeEventListener( 'DOMNodeInserted', refreshHeight, false );
      _content.removeEventListener( 'DOMNodeRemoved', refreshHeight, false );
      _observer.disconnect();
    }

    return this;
  }

  /**
   * Watch for the insertion/removal of DOM nodes.
   * @returns {Expandable} An instance.
   */
  function _initObserver() {
    var MutationObserver = window.MutationObserver ||
                           window.WebKitMutationObserver ||
                           window.MozMutationObserver;
    var addObserver;

    if ( MutationObserver ) {
      addObserver = _addMutationObserverEvents;
    } else {
      addObserver = _addMutationObserverEventsLegacy;
    }

    window.setTimeout( addObserver, 0 );

    return _that;
  }

  /**
   * Add mutation observer events.
   */
  function _addMutationObserverEvents() {
    _observer = new MutationObserver( function( mutations ) {
      mutations.forEach( refreshHeight );
    } );

    _observer.observe( _content, { childList: true, subtree: true } );
  }

  /**
   * Add mutation observer events for when MutationObserver is not supported.
   */
  function _addMutationObserverEventsLegacy() {
    _content.addEventListener( 'DOMNodeInserted', refreshHeight );
    _content.addEventListener( 'DOMNodeRemoved', refreshHeight );
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Expandable} An instance.
   */
  function toggle( duration ) {
    if ( _isExpanded() ) {
      _collapseBinded( duration );
    } else {
      _expandBinded( duration );
    }
    return _that;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Expandable} An instance.
   */
  function expand( duration ) {
    if ( _isExpanded() || _isExpanding() ) {
      return this;
    }

    duration = duration || _calculateExpandDuration( _contentHeight );

    _setStateTo( EXPANDING );
    this.dispatchEvent( 'expandBegin', { target: _that } );
    _setMaxHeight();
    _transitionHeight( _expandComplete, duration );
    return this;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Expandable} An instance.
   */
  function collapse( duration ) {
    if ( _isCollapsed() || _isCollapsing() ) {
      return this;
    }

    duration = duration || _calculateCollapseDuration( _contentHeight );

    _setStateTo( COLLAPSING );
    this.dispatchEvent( 'collapseBegin', { target: _that } );
    _setMinHeight();
    _transitionHeight( _collapseComplete, duration );
    return this;
  }

  /**
   * Reset the height of the Expandables, when e.g. resizing the window.
   */
  function refreshHeight() {
    if ( _isExpanded() ) {
      _setMaxHeight();
    } else {
      _setMinHeight();
    }
  }

  /**
   * Transition height property and call a callback function.
   * Call callback directly if CSS transitions aren't supported.
   * @param {Function} callback Callback function for completion of transition.
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   */
  function _transitionHeight( callback, duration ) {
    if ( _transitionEndEvent ) {
      _content.addEventListener( _transitionEndEvent, callback );
      _content.style[_transitionPrefix] = 'height ' + duration + 's ease-out';
    } else {
      // TODO: Remove callback-return ESLint ignore
      callback(); // eslint-disable-line callback-return, inline-comments, max-len
    }
  }

  /**
   * Configure the expanded state appearance.
   */
  function _setExpandedState() {
    _dom.classList.add( BASE_CLASS + '__expanded' );
    _content.setAttribute( 'aria-expanded', 'true' );
    _target.setAttribute( 'aria-pressed', 'true' );
    _setStateTo( EXPANDED );
  }

  /**
   * Configure the collapsed state appearance.
   */
  function _setCollapsedState() {
    _dom.classList.remove( BASE_CLASS + '__expanded' );
    _content.setAttribute( 'aria-expanded', 'false' );
    _target.setAttribute( 'aria-pressed', 'false' );
    _setStateTo( COLLAPSED );
  }

  /**
   * Expand animation has completed.
   */
  function _expandComplete() {
    _content.removeEventListener( _transitionEndEvent, _expandComplete );
    _setExpandedState();
    _that.dispatchEvent( 'expandEnd', { target: _that } );
  }

  /**
   * Collapse animation has completed.
   */
  function _collapseComplete() {
    _content.removeEventListener( _transitionEndEvent, _collapseComplete );
    _setCollapsedState();
    _that.dispatchEvent( 'collapseEnd', { target: _that } );
  }

  /**
   * Handle click of the Expandable target.
   */
  function _handleClick() {
    // Bubble click event outside of the Expandable.
    _that.dispatchEvent( 'click', { target: _that } );
    if ( _isCollapsed() || _isExpanded() ) {
      _that.toggle();
    }
  }

  /**
   * Refresh calculated height of content area.
   */
  function _calcHeight() {
    _contentHeight = _contentAnimated.offsetHeight;
  }

  /**
   * Handle a resize of the window.
   * TODO: Throttle this call per
   * https://developer.mozilla.org/en-US/docs/Web/Events/resize.
   */
  function _resizeHandler() {
    if ( _contentAnimated.offsetHeight !== _contentHeight ) {
      refreshHeight();
      if ( _isInMobile() ) {
        _collapseBinded();
      }
    }
  }

  /**
   * Calculate and set the height based on the contents' height.
   */
  function _setMaxHeight() {
    _calcHeight();
    _content.style.height = _contentHeight + 'px';
  }

  /**
   * Set the height to zero.
   */
  function _setMinHeight() {
    _content.style.height = '0';
  }

  /**
   * @returns {boolean} Whether Expandable is in a collapsed state.
   */
  function _isCollapsed() {
    return _state === COLLAPSED;
  }

  /**
   * @returns {boolean} Whether Expandable is collapsing.
   */
  function _isCollapsing() {
    return _state === COLLAPSING;
  }

  /**
   * @returns {boolean} Whether Expandable is expanding.
   */
  function _isExpanding() {
    return _state === EXPANDING;
  }

  /**
   * @returns {boolean} Whether Expandable is in a expanded state.
   */
  function _isExpanded() {
    return _state === EXPANDED;
  }

  /**
   * @param {number} state Set the hide/show state flag for the Expandable.
   * @returns {number} Whether Expandable is in a expanded state.
   */
  function _setStateTo( state ) {
    _state = state;
    return _state;
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

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.toggle = toggle;
  this.expand = expand;
  this.refreshHeight = refreshHeight;
  this.collapse = collapse;
  this.destroy = destroy;

  // Export constants so initialization signature can support, e.g.
  // var item = new Expandable( '.item' );
  // item.init( item.EXPANDED );
  // TODO: Move these to Expandable.COLLAPSED and Expandable.EXPANDED.
  //       So that they are set on the constructor, not an instance.
  this.COLLAPSED = COLLAPSED;
  this.EXPANDED = EXPANDED;

  return this;
}

// TODO: Use MoveTransition so this can be removed.
/**
 * @param {HTMLNode} elm
 *   The element to check for support of transition end event.
 * @returns {string} The browser-prefixed transition end event.
 */
function _getTransitionEndEvent( elm ) {
  var transition;
  var transitions = {
    WebkitTransition: 'webkitTransitionEnd',
    MozTransition:    'transitionend',
    OTransition:      'oTransitionEnd otransitionend',
    transition:       'transitionend'
  };

  for ( var t in transitions ) {
    if ( transitions.hasOwnProperty( t ) &&
         typeof elm.style[t] !== 'undefined' ) {
      transition = transitions[t];
      break;
    }
  }
  return transition;
}

/**
 * @param {string} transitionEnd The browser-prefixed transition end event.
 * @returns {string} The browser-prefixed transition event.
 */
function _getTransitionPrefix( transitionEnd ) {
  var TRANSITION_PREFIXES = {
    webkitTransitionEnd: '-webkit-transition',
    MozTransition:       '-moz-transition',
    OTransition:         '-o-transition',
    transitionend:       'transition'
  };

  return TRANSITION_PREFIXES[transitionEnd] ||
         TRANSITION_PREFIXES.transitionend;
}

/**
 * @param {number} height The height of the expandable content area in pixels.
 * @returns {number} The amount of time over which to expand in seconds.
 */
function _calculateExpandDuration( height ) {
  return _constrainValue( 225, 450, height ) / 1000;
}

/**
 * @param {number} height The height of the expandable content area in pixels.
 * @returns {number} The amount of time over which to expand in seconds.
 */
function _calculateCollapseDuration( height ) {
  return _constrainValue( 175, 450, height / 2 ) / 1000;
}

/**
 * @param {number} min The minimum height in pixels.
 * @param {number} max The maximum height in pixels.
 * @param {number} duration
 *   The amount of time over which to expand in milliseconds.
 * @returns {number} The amount of time over which to expand in milliseconds,
 *   constrained to within the min/max values.
 */
function _constrainValue( min, max, duration ) {
  if ( duration > max ) {
    return max;
  } else if ( duration < min ) {
    return min;
  }
  return duration;
}

module.exports = Expandable;
