// Required modules.
import EventObserver from '../../modules/util/EventObserver';

// eslint-disable-next-line max-statements
/**
 * BaseTransition
 * @class
 *
 * @classdesc Initializes new BaseTransition behavior.
 *   This shouldn't be used directly, but instead should be
 *   the base class used through composition by a specific transition.
 *
 * @param {HTMLNode} element
 *   DOM element to apply transition to.
 * @param {Object} classes
 *   The classes to apply to this transition.
 * @returns {BaseTransition} An instance.
 */
function BaseTransition( element, classes ) {
  const _classes = classes;
  let _dom;

  let _lastClass;
  let _transitionEndEvent;
  let _transitionCompleteBinded;
  let _addEventListenerBinded;
  let _isAnimating = false;
  let _isFlushed = false;

  /**
   * @returns {BaseTransition} An instance.
   */
  function init() {
    _transitionCompleteBinded = _transitionComplete.bind( this );
    _addEventListenerBinded = _addEventListener.bind( this );
    setElement( element );

    return this;
  }

  /**
   * Set the HTML element target of this transition.
   * @param {HTMLNode} elem - The target of the transition.
   */
  function setElement( elem ) {

    /* If the element has already been set,
       clear the transition classes from the old element. */
    if ( _dom ) {
      remove();
      animateOn();
    }
    _dom = elem;
    _dom.classList.add( _classes.BASE_CLASS );
    _transitionEndEvent = _getTransitionEndEvent( _dom );
  }

  /**
   * Add a "transition-duration: 0s" utility CSS class.
   * @returns {BaseTransition} An instance.
   */
  function animateOn() {
    if ( !_dom ) { return this; }
    _dom.classList.remove( BaseTransition.NO_ANIMATION_CLASS );

    return this;
  }

  /**
   * Remove a "transition-duration: 0s" utility CSS class.
   * @returns {BaseTransition} An instance.
   */
  function animateOff() {
    if ( !_dom ) { return this; }
    _dom.classList.add( BaseTransition.NO_ANIMATION_CLASS );

    return this;
  }

  /**
   * @returns {boolean} Whether the transition has a duration or not.
   *   Returns false if this transition has not been initialized.
   */
  function isAnimated() {
    if ( !_dom ) { return false; }
    return !_dom.classList.contains( BaseTransition.NO_ANIMATION_CLASS );
  }

  /**
   * Halt an in-progress animation and call the complete event immediately.
   */
  function halt() {
    if ( !_isAnimating ) { return; }
    _dom.style.webkitTransitionDuration = '0';
    _dom.style.mozTransitionDuration = '0';
    _dom.style.oTransitionDuration = '0';
    _dom.style.transitionDuration = '0';
    _dom.removeEventListener(
      _transitionEndEvent,
      _transitionCompleteBinded
    );
    _transitionCompleteBinded();
    _dom.style.webkitTransitionDuration = '';
    _dom.style.mozTransitionDuration = '';
    _dom.style.oTransitionDuration = '';
    _dom.style.transitionDuration = '';
  }

  /**
   * Add an event listener to the transition, or call the transition
   * complete handler immediately if transition not supported.
   */
  function _addEventListener() {
    _dom.classList.add( BaseTransition.ANIMATING_CLASS );
    _isAnimating = true;
    // If transition is not supported, call handler directly (IE9/OperaMini).
    if ( _transitionEndEvent ) {
      _dom.addEventListener(
        _transitionEndEvent,
        _transitionCompleteBinded
      );
      this.dispatchEvent( BaseTransition.BEGIN_EVENT, { target: this } );
    } else {
      this.dispatchEvent( BaseTransition.BEGIN_EVENT, { target: this } );
      _transitionCompleteBinded();
    }
  }

  /**
   * Remove an event listener to the transition.
   */
  function _removeEventListener() {
    _dom.removeEventListener( _transitionEndEvent, _transitionCompleteBinded );
  }

  /**
   * Handle the end of a transition.
   */
  function _transitionComplete() {
    _removeEventListener();
    _dom.classList.remove( BaseTransition.ANIMATING_CLASS );
    this.dispatchEvent( BaseTransition.END_EVENT, { target: this } );
    _isAnimating = false;
  }

  /**
   * Search for and remove initial BaseTransition classes that have
   * already been applied to this BaseTransition's target element.
   */
  function _flush() {
    for ( const prop in _classes ) {
      if ( _classes.hasOwnProperty( prop ) &&
           _classes[prop] !== _classes.BASE_CLASS &&
           _dom.classList.contains( _classes[prop] ) ) {
        _dom.classList.remove( _classes[prop] );
      }
    }
  }

  /**
   * Remove all transition classes, if transition is initialized.
   * @returns {boolean}
   *   True, if the element's CSS classes were touched, false otherwise.
   */
  function remove() {
    if ( _dom ) {
      halt();
      _dom.classList.remove( _classes.BASE_CLASS );
      _flush();
      return true;
    }

    return false;
  }

  /**
   * @param {string} className - A CSS class.
   * @returns {boolean} False if the class is already applied
   *   or the transition is not initialized,
   *   otherwise true if the class was applied.
   */
  function applyClass( className ) {
    if ( !_dom ) { return false; }
    if ( !_isFlushed ) {
      _flush();
      _isFlushed = true;
    }

    if ( _dom.classList.contains( className ) ) {
      return false;
    }

    _removeEventListener();
    _dom.classList.remove( _lastClass );
    _lastClass = className;
    _addEventListenerBinded();
    _dom.classList.add( _lastClass );

    return true;
  }

  // TODO: Update Expandables to use a transition.
  /**
   * @param {HTMLNode} elem
   *   The element to check for support of transition end event.
   * @returns {string} The browser-prefixed transition end event.
   */
  function _getTransitionEndEvent( elem ) {
    if ( !elem ) {
      const msg = 'Element does not have TransitionEnd event. It may be null!';
      throw new Error( msg );
    }

    let transition;
    const transitions = {
      WebkitTransition: 'webkitTransitionEnd',
      MozTransition:    'transitionend',
      OTransition:      'oTransitionEnd otransitionend',
      transition:       'transitionend'
    };

    for ( const t in transitions ) {
      if ( transitions.hasOwnProperty( t ) &&
           typeof elem.style[t] !== 'undefined' ) {
        transition = transitions[t];
        break;
      }
    }
    return transition;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;
  this.removeEventListener = eventObserver.removeEventListener;

  this.animateOff = animateOff;
  this.animateOn = animateOn;
  this.applyClass = applyClass;
  this.halt = halt;
  this.init = init;
  this.isAnimated = isAnimated;
  this.remove = remove;
  this.setElement = setElement;

  return this;
}

// Public static constants.
BaseTransition.BEGIN_EVENT = 'transitionBegin';
BaseTransition.END_EVENT = 'transitionEnd';
BaseTransition.NO_ANIMATION_CLASS = 'u-no-animation';
BaseTransition.ANIMATING_CLASS = 'u-is-animating';

export default BaseTransition;
