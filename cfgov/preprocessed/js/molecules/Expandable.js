'use strict';

// Required polyfills for <IE9.
require( '../modules/polyfill/query-selector' );
require( '../modules/polyfill/event-listener' );
require( '../modules/polyfill/class-list' );

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );
var $ = require( 'jquery' );

/**
 * Expandable
 * @class
 *
 * @classdesc Initializes a new Expandable molecule.
 *
 * @param {Object} context
 *   The DOM element within which to search for the molecule.
 * @returns {Object} An Expandable instance.
 */
function Expandable( context ) { // eslint-disable-line max-statements, inline-comments, max-len

  // TODO: Remove this when difference between atomic Expandable
  //       and cf-expandables is resolved.
  // ==========================================================================
  // Unsets global expandables logic.
  if ( $.fn.expandable ) {
    var html = context.innerHTML;
    context.innerHTML = html;

    var $this = $( context );
    var $cueOpen = $this.find( '.expandable_cue-open' ).not( $this.find( '.expandable .expandable_cue-open' ) );
    var $cueClose = $this.find( '.expandable_cue-close' ).not( $this.find( '.expandable .expandable_cue-close' ) );
    var $content = $this.find( '.expandable_content' ).not( $this.find( '.expandable .expandable_content' ) );

    $cueOpen.attr( 'style', '' );
    $cueClose.attr( 'style', '' );
    $content.attr( 'style', '' );

  }
  // ==========================================================================


  // The Expandable context will directly be the Expandable when used in an ExpandableGroup.
  var _dom = context.classList.contains( 'expandable' ) ?
             context : context.querySelector( '.expandable' );
  var _target = _dom.querySelector( '.expandable_target' );
  var _content = _dom.querySelector( '.expandable_content' );
  var _link = _dom.querySelector( '.expandable_link' );
  var _cueOpen = _link.querySelector( '.expandable_cue-open' );
  var _cueClose = _link.querySelector( '.expandable_cue-close' );
  var _isAnimating = false;
  var _clickQueue = 0;
  var _isExpanded;
  var _that = this;
  var _contentHeight = $( _content ).height();

  /**
   * @returns {Object} The Expandable instance.
   */
  function init() {
    _isExpanded = _dom.classList.contains( 'expandable__expanded' );
    if ( _isExpanded ) {
      _setExpandedState();
    } else {
      _content.style.display = 'none';
      _setCollapsedState();
    }
    _link.classList.remove( 'u-hide' );

    _target.addEventListener( 'click', _handleClick );
    return this;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function toggle( duration ) {
    if ( !_isExpanded ) {
      this.expand( duration );
    } else {
      this.collapse( duration );
    }
    return this;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function expand( duration ) {
    duration = duration || _calculateExpandDuration( _contentHeight );

    this.dispatchEvent( 'beginExpand', { target: _that } );
    _isAnimating = true;
    $( _content ).slideDown( {
      duration: duration,
      easing: 'easeOutExpo',
      complete: _expandComplete
    } );

    return this;
  }

  /**
   * @param {number} duration
   *   The duration of the sliding animation in milliseconds.
   * @returns {Object} The Expandable instance.
   */
  function collapse( duration ) {
    duration = duration || _calculateCollapseDuration( _contentHeight );

    this.dispatchEvent( 'beginCollapse', { target: _that } );
    _isAnimating = true;
    $( _content ).slideUp( {
      duration: duration,
      easing: 'easeOutExpo',
      complete: _collapseComplete
    } );

    return this;
  }

  /**
   * Configure the expanded state appearance.
   */
  function _setExpandedState() {
    _showCollapseCue();
    _dom.classList.add( 'expandable__expanded' );
    _content.setAttribute( 'aria-expanded', 'true' );
    _target.setAttribute( 'aria-pressed', 'true' );
    _isExpanded = true;
  }

  /**
   * Configure the collapsed state appearance.
   */
  function _setCollapsedState() {
    _showExpandCue();
    _dom.classList.remove( 'expandable__expanded' );
    _content.setAttribute( 'aria-expanded', 'false' );
    _target.setAttribute( 'aria-pressed', 'false' );
    _isExpanded = false;
  }

  /**
   * Expand animation has completed.
   */
  function _expandComplete() {
    _setExpandedState();
    _animationComplete();
    _that.dispatchEvent( 'endExpand', { target: _that } );
  }

  /**
   * Collapse animation has completed.
   */
  function _collapseComplete() {
    _setCollapsedState();
    _animationComplete();
    _that.dispatchEvent( 'endCollapse', { target: _that } );
  }

  /**
   * Animation for content has completed.
   */
  function _animationComplete() {
    _isAnimating = false;
    if ( _clickQueue === 1 ) {
      _handleClick();
      _clickQueue = 0;
    }
  }

  /**
   * Handle click of the Expandable target.
   */
  function _handleClick() {
    if ( !_isAnimating ) {
      _that.toggle();
    } else {
      _clickQueue = 1;
    }
  }

  /**
   * Show the expand cue and hide the collapse cue.
   */
  function _showExpandCue() {
    _cueOpen.classList.remove( 'u-hide' );
    _cueClose.classList.add( 'u-hide' );
  }

  /**
   * Show the collapse cue and hide the expand cue.
   */
  function _showCollapseCue() {
    _cueOpen.classList.add( 'u-hide' );
    _cueClose.classList.remove( 'u-hide' );
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
  return this;
}

/**
 * @param {number} height The height of the expandable content area in pixels.
 * @returns {number} The amount of time over which to expand in milliseconds.
 */
function _calculateExpandDuration( height ) {
  return _constrainValue( 450, 900, height * 4 );
}

/**
 * @param {number} height The height of the expandable content area in pixels.
 * @returns {number} The amount of time over which to expand in milliseconds.
 */
function _calculateCollapseDuration( height ) {
  return _constrainValue( 350, 900, height * 2 );
}

/**
 * @param {number} min The minimum height in pixels.
 * @param {number} max The maximum height in pixels.
 * @param {number} duration The amount of time over which to expand in milliseconds.
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
