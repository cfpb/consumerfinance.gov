'use strict';

// Required modules.
var EventObserver = require( '../../modules/util/EventObserver' );
var BaseTransition = require( './BaseTransition' );

// Exported constants.
var CLASSES = Object.seal( {
  BASE_CLASS: 'u-alpha-transition',
  ALPHA_100:  'u-alpha-100',
  ALPHA_0:    'u-alpha-0'
} );

/**
 * AlphaTransition
 * @class
 *
 * @classdesc Initializes new AlphaTransition behavior.
 *
 * @param {HTMLNode} element
 *   DOM element to apply opacity transition to.
 * @returns {AlphaTransition} An instance.
 */
function AlphaTransition( element ) {

  var _baseTransition = new BaseTransition( element, CLASSES ).init();
  var _transitionCompleteBinded = _transitionComplete.bind( this );
  _baseTransition.addEventListener( BaseTransition.END_EVENT,
                                    _transitionCompleteBinded );

  /**
   * @returns {AlphaTransition} An instance.
   */
  function init() {
    return this;
  }

  /**
   * @param {HTMLNode} elem - Set HTML element target of the transition.
   */
  function setElement( elem ) {
    _baseTransition.setElement( elem );
  }

  /**
   * Remove all transition classes.
   */
  function remove() {
    _baseTransition.remove();
  }

  /**
   * Add a "transition-duration: 0" utility CSS class.
   */
  function animateOn() {
    _baseTransition.animateOn();
  }

  /**
   * Remove a "transition-duration: 0" utility CSS class.
   */
  function animateOff() {
    _baseTransition.animateOff();
  }

  /**
   * @returns {boolean} Whether the transition has a duration or not.
   */
  function isAnimated() {
    return _baseTransition.isAnimated();
  }

  /**
   * Handle the end of a transition.
   */
  function _transitionComplete() {
    this.dispatchEvent( BaseTransition.END_EVENT, { target: this } );
  }

  /**
   * Fade to 100% by applying a utility alpha class.
   * @returns {AlphaTransition} An instance.
   */
  function fadeTo100() {
    _baseTransition.applyClass( CLASSES.ALPHA_100 );

    return this;
  }

  /**
   * Fade to nothing by applying a utility alpha class.
   * @returns {AlphaTransition} An instance.
   */
  function fadeTo0() {
    _baseTransition.applyClass( CLASSES.ALPHA_0 );

    return this;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;
  this.removeEventListener = eventObserver.removeEventListener;

  this.animateOff = animateOff;
  this.animateOn = animateOn;
  this.fadeTo100 = fadeTo100;
  this.fadeTo0 = fadeTo0;
  this.init = init;
  this.isAnimated = isAnimated;
  this.setElement = setElement;
  this.remove = remove;

  return this;
}

// Public static properties.
AlphaTransition.CLASSES = CLASSES;

module.exports = AlphaTransition;
