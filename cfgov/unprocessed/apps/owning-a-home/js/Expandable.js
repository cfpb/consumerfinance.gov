import { checkDom, destroyInitFlag, setInitFlag }
  from '../../../js/modules/util/atomic-helpers';
import DT from './dom-tools';
import EventObserver from '../../../js/modules/util/EventObserver';


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

  const BASE_CLASS = 'o-expandable';
  let UNDEFINED;

  // Bitwise flags for the state of this Expandable.
  const COLLAPSED = 0;
  const COLLAPSING = 1;
  const EXPANDING = 2;
  const EXPANDED = 3;

  /* The Expandable element will directly be the Expandable
     when used in an ExpandableGroup, otherwise it can be the parent container. */
  const _dom = checkDom( element, BASE_CLASS );
  const _target = _dom.querySelector( '.' + BASE_CLASS + '_target' );
  const _content = _dom.querySelector( '.' + BASE_CLASS + '_content' );
  const _link = _dom.querySelector( '.' + BASE_CLASS + '_link' );

  let _state = COLLAPSED;
  const _transitionEndEvent = _getTransitionEndEvent( _content );
  const _transitionPrefix = _getTransitionPrefix( _transitionEndEvent );
  let _contentHeight;

  // TODO: Replace function of _that with Function.prototype.bind.
  const _that = this;
  const _collapseBinded = collapse.bind( this );
  const _expandBinded = expand.bind( this );

  /**
   * @param {number} state
   *   Allows passing of EXPANDED flag to set expanded state.
   * @returns {Expandable|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init( state ) {
    if ( !setInitFlag( _dom ) ) {
      return UNDEFINED;
    }
    // Even if expanded is set, don't expand if in mobile window size.
    if ( state === EXPANDED ||
         _dom.getAttribute( 'data-state' ) === 'expanded' ) {

      /* If expanded by default, we need to set the height inline so the
         inline transition to collapse the Expandable works.
         TODO: Handle issue of height calculating before
         web fonts have loaded and changed height. */
      _setMaxHeight();
      _setExpandedState();
    } else {
      _setCollapsedState();
    }

    // Show the show/hide links, which otherwise are hidden if JS is off.
    DT.removeClass( _link, 'u-hidden' );

    _target.addEventListener( 'click', _handleClick );

    return this;
  }

  /**
   * Reverse a call to init() to teardown an instance initialization.
   * @returns {Expandable} An instance.
   */
  function destroy() {
    if ( destroyInitFlag( _dom ) ) {
      _target.removeEventListener( 'click', _handleClick );
    }

    return this;
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

    DT.nextFrame( () => {
      _setExpandingState( );
      _content.style[_transitionPrefix] = '';
      _calcHeight();
      duration = duration || _calculateExpandDuration( _contentHeight );
      this.dispatchEvent( 'expandBegin', { target: _that } );
      DT.nextFrame( () =>
        _transitionHeight(
          _expandComplete,
          duration,
          'cubic-bezier(0.190, 1.000, 0.220, 1.000)'
        )
      );

      /* on the next frame (as soon as the previous style change has taken effect),
         have the element transition to it's maximum height. */
      DT.nextFrame( _setMaxHeight );
    } );

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
    } else if ( _isExpanding() ) {
      DT.removeClass( _dom, BASE_CLASS + '__expanding' );
      _content.removeEventListener( _transitionEndEvent, _expandComplete );
    }

    DT.nextFrame( () => {
      _setCollapsingState( );
      _content.style[_transitionPrefix] = '';
      _calcHeight();
      _setMaxHeight();
      duration = duration || _calculateCollapseDuration( _contentHeight );
      this.dispatchEvent( 'collapseBegin', { target: _that } );
      DT.nextFrame( () =>
        _transitionHeight( _collapseComplete, duration, 'ease-in' )
      );

      /* on the next frame (as soon as the previous style change has taken effect),
         have the element transition to height: 0 */
      DT.nextFrame( _setMinHeight );
    } );

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
   * @param {string} transition - Type of transition timing.
   */
  function _transitionHeight( callback, duration, transition ) {
    const isVisible = window.getComputedStyle( _dom, null )
      .getPropertyValue( 'display' ) !== 'none';

    if ( _transitionEndEvent && isVisible ) {
      _content.addEventListener( _transitionEndEvent, callback );
      _content.style[_transitionPrefix] = 'height ' + duration + 's ' + transition;
    } else {
      // TODO: Remove callback-return ESLint ignore
      callback(); // eslint-disable-line callback-return, inline-comments, max-len
    }
  }

  /**
   * Configure the expanded state appearance.
   */
  function _setExpandingState() {
    _setStateTo( EXPANDING );
    DT.removeClass( _dom, BASE_CLASS + '__collapsed' );
    DT.addClass( _dom, BASE_CLASS + '__expanding' );
  }

  /**
   * Configure the expanded state appearance.
   */
  function _setExpandedState() {
    _setStateTo( EXPANDED );
    DT.removeClass( _dom, BASE_CLASS + '__expanding' );
    DT.addClass( _dom, BASE_CLASS + '__expanded' );
    _content.setAttribute( 'aria-expanded', 'true' );
    _target.setAttribute( 'aria-pressed', 'true' );
  }

  /**
   * Configure the collapsed state appearance.
   */
  function _setCollapsedState() {
    _setStateTo( COLLAPSED );
    DT.removeClass( _dom, BASE_CLASS + '__collapsing' );
    DT.addClass( _dom, BASE_CLASS + '__collapsed' );
    _content.setAttribute( 'aria-expanded', 'false' );
    _target.setAttribute( 'aria-pressed', 'false' );
  }

  /**
   * Configure the expanded state appearance.
   */
  function _setCollapsingState() {
    _setStateTo( COLLAPSING );
    DT.removeClass( _dom, BASE_CLASS + '__expanded' );
    DT.addClass( _dom, BASE_CLASS + '__collapsing' );
  }

  /**
   * Expand animation has completed.
   */
  function _expandComplete() {
    _content.style.height = '';
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
    _contentHeight = _content.scrollHeight;
  }

  /**
   * Calculate and set the height based on the contents' height.
   */
  function _setMaxHeight() {
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
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.toggle = toggle;
  this.expand = expand;
  this.refreshHeight = refreshHeight;
  this.collapse = collapse;
  this.destroy = destroy;

  /* Export constants so initialization signature can support, e.g.
     var item = new Expandable( '.item' );
     item.init( item.EXPANDED );
     TODO: Move these to Expandable.COLLAPSED and Expandable.EXPANDED.
     So that they are set on the constructor, not an instance. */
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
  let transition;
  const transitions = {
    WebkitTransition: 'webkitTransitionEnd',
    MozTransition:    'transitionend',
    OTransition:      'oTransitionEnd otransitionend',
    transition:       'transitionend'
  };

  for ( const t in transitions ) {
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
  const TRANSITION_PREFIXES = {
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
  return _constrainValue( 300, 600, height * 4 ) / 1000;
}

/**
 * @param {number} height The height of the expandable content area in pixels.
 * @returns {number} The amount of time over which to expand in seconds.
 */
function _calculateCollapseDuration( height ) {
  return _constrainValue( 250, 500, height * 2 ) / 1000;
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

export default Expandable;
