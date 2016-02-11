'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../modules/polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );
var atomicCheckers = require( '../modules/util/atomic-checkers' );

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

  var BASE_CLASS = 'm-expandable';

  // Bitwise flags for the state of this Expandable.
  var COLLAPSED = 0;
  var COLLAPSING = 1;
  var EXPANDING = 2;
  var EXPANDED = 3;

  // The Expandable element will directly be the Expandable
  // when used in an ExpandableGroup, otherwise it can be the parent container.
  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'Expandable' );
  var _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
  var _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  var _contentAnimated =
    _content.querySelector( '.' + BASE_CLASS + '_content-animated' );
  var _link = _dom.querySelector( '.' + BASE_CLASS + '_link' );

  var _state = COLLAPSED;
  var _transitionEndEvent = _getTransitionEndEvent( _content );
  var _contentHeight;

  // TODO: Replace function of _that with Function.prototype.bind.
  var _that = this;

  /**
   * @param {number} state
   *   Allows passing of EXPANDED flag to set expanded state.
   * @returns {Object} The Expandable instance.
   */
  function init( state ) {
    _calcHeight();
    if ( state === EXPANDED ||
         _dom.getAttribute( 'data-state' ) === 'expanded' ) {
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

    // TODO: Remove if statement if polyfill that
    //       adds addEventListener to window is used.
    if ( window.addEventListener ) {
      window.addEventListener( 'resize', _refreshHeight );
    }

    _initObserver();

    return this;
  }

  /**
   * Watch for the insertion/removal of DOM nodes.
   * @returns {Object} The Expandable instance.
   */
  function _initObserver() {
    var MutationObserver = window.MutationObserver ||
                           window.WebKitMutationObserver ||
                           window.MozMutationObserver;
    var observeDOM;

    if ( MutationObserver ) {
      observeDOM = function() {
        var observer = new MutationObserver( function( mutations ) {
          mutations.forEach( _refreshHeight );
        } );

        observer.observe( _content, { childList: true, subtree: true } );
      };
    } else {
      observeDOM = function() {
        _content.addEventListener( 'DOMNodeInserted', _refreshHeight, false );
        _content.addEventListener( 'DOMNodeRemoved', _refreshHeight, false );
      };
    }

    window.setTimeout( observeDOM, 0 );

    return _that;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function toggle( duration ) {
    if ( _isExpanded() ) {
      _that.collapse( duration );
    } else {
      _that.expand( duration );
    }
    return _that;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function expand( duration ) {
    if ( _isExpanded() || _isExpanding() ) {
      return this;
    }

    duration = duration || _calculateExpandDuration( _contentHeight );

    _setStateTo( EXPANDING );
    this.dispatchEvent( 'beginExpand', { target: _that } );
    _setMaxHeight();
    _transitionHeight( _expandComplete, duration );
    return this;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function collapse( duration ) {
    if ( _isCollapsed() || _isCollapsing() ) {
      return this;
    }

    duration = duration || _calculateCollapseDuration( _contentHeight );

    _setStateTo( COLLAPSING );
    this.dispatchEvent( 'beginCollapse', { target: _that } );
    _setMinHeight();
    _transitionHeight( _collapseComplete, duration );
    return this;
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
      _content.style.transition = 'height ' + duration + 's ease-out';
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
    _that.dispatchEvent( 'endExpand', { target: _that } );
  }

  /**
   * Collapse animation has completed.
   */
  function _collapseComplete() {
    _content.removeEventListener( _transitionEndEvent, _collapseComplete );
    _setCollapsedState();
    _that.dispatchEvent( 'endCollapse', { target: _that } );
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
   * Reset the height of the Expandables, when e.g. resizing the window.
   */
  function _refreshHeight() {
    if ( _isExpanded() ) {
      _setMaxHeight();
    } else {
      _setMinHeight();
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

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.toggle = toggle;
  this.expand = expand;
  this.collapse = collapse;

  // Export constants so initialization signature can support, e.g.
  // var item = new Expandable( '.item' );
  // item.init( item.EXPANDED );
  this.COLLAPSED = COLLAPSED;
  this.EXPANDED = EXPANDED;

  return this;
}

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
