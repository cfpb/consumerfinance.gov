// Required modules.
import BaseTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/BaseTransition.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';

// Exported constants.
const CLASSES = {
  CSS_PROPERTY: 'max-height',
  BASE_CLASS:   'u-max-height-transition',
  MH_DEFAULT:   'u-max-height-default',
  MH_SUMMARY:   'u-max-height-summary',
  MH_ZERO:      'u-max-height-zero'
};

/**
 * MoveTransition
 * @class
 *
 * @classdesc Initializes new MoveTransition behavior.
 *
 * @param {HTMLNode} element
 *   DOM element to apply transition to.
 * @returns {MaxHeightTransition} An instance.
 */
function MaxHeightTransition( element ) {
  const _baseTransition = new BaseTransition( element, CLASSES );
  let previousHeight;

  /**
   * @returns {MaxHeightTransition} An instance.
   */
  function init() {
    _baseTransition.init();

    element.style.maxHeight = element.scrollHeight + 'px';

    const _transitionCompleteBinded = _transitionComplete.bind( this );
    _baseTransition.addEventListener(
      BaseTransition.END_EVENT,
      _transitionCompleteBinded
    );

    return this;
  }

  /**
   * Handle the end of a transition.
   */
  function _transitionComplete() {
    this.dispatchEvent( BaseTransition.END_EVENT, { target: this } );

    if ( element.scrollHeight > previousHeight ) {
      element.style.maxHeight = element.scrollHeight + 'px';
    }
  }

  /**
   * Reset the max-height to the default size.
   * @returns {PostitionTransition} An instance.
   */
  function maxHeightDefault() {
    _baseTransition.applyClass( CLASSES.MH_DEFAULT );

    if ( !previousHeight || element.scrollHeight > previousHeight ) {
      previousHeight = element.scrollHeight;
    }

    return this;
  }

  /**
   * Collapses the max-height to just a summary height.
   * @returns {PostitionTransition} An instance.
   */
  function maxHeightSummary() {
    _baseTransition.applyClass( CLASSES.MH_SUMMARY );

    previousHeight = element.scrollHeight;

    return this;
  }

  /**
   * Collapses thte max-height completely.
   * @returns {PostitionTransition} An instance.
   */
  function maxHeightZero() {
    _baseTransition.applyClass( CLASSES.MH_ZERO );

    previousHeight = element.scrollHeight;

    return this;
  }

  /**
   * Remove style attribute.
   * Remove all transition classes, if transition is initialized.
   * @returns {boolean}
   *   True, if the element's CSS classes were touched, false otherwise.
   */
  function remove() {
    element.style.maxHeight = '';
    return _baseTransition.remove();
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;
  this.removeEventListener = eventObserver.removeEventListener;

  this.animateOff = _baseTransition.animateOff;
  this.animateOn = _baseTransition.animateOn;
  this.halt = _baseTransition.halt;
  this.isAnimated = _baseTransition.isAnimated;
  this.setElement = _baseTransition.setElement;
  this.remove = remove;

  this.init = init;
  this.maxHeightDefault = maxHeightDefault;
  this.maxHeightSummary = maxHeightSummary;
  this.maxHeightZero = maxHeightZero;

  return this;
}

// Public static properties.
MaxHeightTransition.CLASSES = CLASSES;

export default MaxHeightTransition;
