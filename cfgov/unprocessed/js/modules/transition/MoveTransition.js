'use strict';

// Required modules.
var EventObserver = require( '../../modules/util/EventObserver' );
var BaseTransition = require( './BaseTransition' );

// Exported constants.
var CLASSES = Object.seal( {
  BASE_CLASS:     'u-move-transition',
  MOVE_TO_ORIGIN: 'u-move-to-origin',
  MOVE_LEFT:      'u-move-left',
  MOVE_LEFT_2X:   'u-move-left-2x',
  MOVE_LEFT_3X:   'u-move-left-3x',
  MOVE_RIGHT:     'u-move-right',
  MOVE_UP:        'u-move-up'
} );

/**
 * MoveTransition
 * @class
 *
 * @classdesc Initializes new MoveTransition behavior.
 *
 * @param {HTMLNode} element
 *   DOM element to apply move transition to.
 * @returns {MoveTransition} An instance.
 */
function MoveTransition( element ) { // eslint-disable-line max-statements, no-inline-comments, max-len

  var _baseTransition = new BaseTransition( element, CLASSES ).init();
  var _transitionCompleteBinded = _transitionComplete.bind( this );
  _baseTransition.addEventListener( BaseTransition.END_EVENT,
                                    _transitionCompleteBinded );

  /**
   * @returns {MoveTransition} An instance.
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
   * Move to the element's original coordinates.
   * @returns {MoveTransition} An instance.
   */
  function moveToOrigin() {
    _baseTransition.applyClass( CLASSES.MOVE_TO_ORIGIN );

    return this;
  }

  /**
   * Move to the left by applying a utility move class.
   * @param {Number} count
   *   How many times to move left as a multiplication of the element's width.
   * @returns {MoveTransition} An instance.
   */
  function moveLeft( count ) {
    count = count || 1;
    var moveClasses = [
      CLASSES.MOVE_LEFT,
      CLASSES.MOVE_LEFT_2X,
      CLASSES.MOVE_LEFT_3X
    ];

    if ( count < 1 || count > moveClasses.length ) {
      throw new Error( 'MoveTransition: moveLeft count is out of range!' );
    }

    _baseTransition.applyClass( moveClasses[count - 1] );

    return this;
  }

  /**
   * Move to the right by applying a utility move class.
   * @returns {MoveTransition} An instance.
   */
  function moveRight() {
    _baseTransition.applyClass( CLASSES.MOVE_RIGHT );

    return this;
  }

  /**
   * Move up by applying a utility move class.
   * @returns {MoveTransition} An instance.
   */
  function moveUp() {
    _baseTransition.applyClass( CLASSES.MOVE_UP );

    return this;
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;
  this.removeEventListener = eventObserver.removeEventListener;

  this.animateOff = animateOff;
  this.animateOn = animateOn;
  this.init = init;
  this.isAnimated = isAnimated;
  this.moveToOrigin = moveToOrigin;
  this.moveLeft = moveLeft;
  this.moveRight = moveRight;
  this.moveUp = moveUp;
  this.setElement = setElement;
  this.remove = remove;

  return this;
}

// Public static properties.
MoveTransition.CLASSES = CLASSES;

module.exports = MoveTransition;
