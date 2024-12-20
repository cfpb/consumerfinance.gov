// TODO: Note that this is an older copy of BaseTransition from the
// design-system to isolate TDP expandable customizations.

// Required modules.
import { EventObserver } from '@cfpb/cfpb-design-system';

/**
 * BaseTransition
 * @class
 * @classdesc Initializes new BaseTransition behavior.
 *   This shouldn't be used directly, but instead should be
 *   the base class used through composition by a specific transition.
 * @param {HTMLElement} element - DOM element to apply transition to.
 * @param {object} classes - The classes to apply to this transition.
 * @returns {BaseTransition} An instance.
 */
function BaseTransition(element, classes) {
  const _classes = classes;
  let _dom;

  let _lastClass;
  let _transitionEndEvent;
  let _transitionCompleteBinded;
  let _addEventListenerBinded;
  let _isAnimating = false;
  let _isFlushed = false;

  // Make sure required attributes are passed in.
  if (
    typeof _classes.CSS_PROPERTY === 'undefined' ||
    typeof _classes.BASE_CLASS === 'undefined'
  ) {
    throw new Error(
      'Transitions require CSS_PROPERTY and BASE_CLASS ' +
        'to be passed into BaseTransition.',
    );
  }

  /**
   * Add an event listener to the transition, or call the transition
   * complete handler immediately if transition not supported.
   */
  function _addEventListener() {
    _dom.classList.add(BaseTransition.ANIMATING_CLASS);
    _isAnimating = true;

    /*
      If transition is not supported, call handler directly (IE9/OperaMini).
      Also, if "transition-duration: 0s" is set, transitionEnd event will not
      fire, so we need to call the handler straight away.
    */
    if (
      _transitionEndEvent &&
      !_dom.classList.contains(BaseTransition.NO_ANIMATION_CLASS)
    ) {
      _dom.addEventListener(_transitionEndEvent, _transitionCompleteBinded);
      this.dispatchEvent(BaseTransition.BEGIN_EVENT, { target: this });
    } else {
      this.dispatchEvent(BaseTransition.BEGIN_EVENT, { target: this });
      _transitionCompleteBinded();
    }
  }

  /**
   * Remove an event listener to the transition.
   */
  function _removeEventListener() {
    _dom.removeEventListener(_transitionEndEvent, _transitionCompleteBinded);
  }

  /**
   * Handle the end of a transition.
   * @param {TransitionEvent} evt - Transition event object.
   * @returns {boolean} True if transition was cleaned up,
   *   false if an outside transitioning property triggered this event handler.
   */
  function _transitionComplete(evt) {
    if (evt && evt.propertyName !== _classes.CSS_PROPERTY) {
      return false;
    }

    _removeEventListener();
    _dom.classList.remove(BaseTransition.ANIMATING_CLASS);
    this.dispatchEvent(BaseTransition.END_EVENT, { target: this });
    _isAnimating = false;
    return true;
  }

  /**
   * Search for and remove initial BaseTransition classes that have
   * already been applied to this BaseTransition's target element.
   */
  function _flush() {
    let prop;
    for (prop in _classes) {
      if (
        {}.hasOwnProperty.call(_classes, prop) &&
        _classes[prop] !== _classes.BASE_CLASS &&
        _dom.classList.contains(_classes[prop])
      ) {
        _dom.classList.remove(_classes[prop]);
      }
    }
  }

  /**
   * Halt an in-progress animation and call the complete event immediately.
   */
  function halt() {
    if (!_isAnimating) {
      return;
    }
    _dom.style.webkitTransitionDuration = '0';
    _dom.style.mozTransitionDuration = '0';
    _dom.style.oTransitionDuration = '0';
    _dom.style.transitionDuration = '0';
    _dom.removeEventListener(_transitionEndEvent, _transitionCompleteBinded);
    _transitionCompleteBinded();
    _dom.style.webkitTransitionDuration = '';
    _dom.style.mozTransitionDuration = '';
    _dom.style.oTransitionDuration = '';
    _dom.style.transitionDuration = '';
  }

  /**
   * Remove all transition classes, if transition is initialized.
   * @returns {boolean}
   *   True, if the element's CSS classes were touched, false otherwise.
   */
  function remove() {
    if (_dom) {
      halt();
      _dom.classList.remove(_classes.BASE_CLASS);
      _flush();
      return true;
    }

    return false;
  }

  /**
   * Add a "transition-duration: 0s" utility CSS class.
   * @returns {BaseTransition} An instance.
   */
  function animateOn() {
    if (!_dom) {
      return this;
    }
    _dom.classList.remove(BaseTransition.NO_ANIMATION_CLASS);

    return this;
  }

  /**
   * Remove a "transition-duration: 0s" utility CSS class.
   * @returns {BaseTransition} An instance.
   */
  function animateOff() {
    if (!_dom) {
      return this;
    }
    _dom.classList.add(BaseTransition.NO_ANIMATION_CLASS);

    return this;
  }

  /**
   * @param {HTMLElement} elem - The element to check
   *   for support of transition end event.
   * @returns {string} The browser-prefixed transition end event.
   */
  function _getTransitionEndEvent(elem) {
    if (!elem) {
      const msg = 'Element does not have TransitionEnd event. It may be null!';
      throw new Error(msg);
    }

    let transition;
    const transitions = {
      WebkitTransition: 'webkitTransitionEnd',
      MozTransition: 'transitionend',
      OTransition: 'oTransitionEnd otransitionend',
      transition: 'transitionend',
    };

    let transitionEvent;
    for (transitionEvent in transitions) {
      if (
        {}.hasOwnProperty.call(transitions, transitionEvent) &&
        typeof elem.style[transitionEvent] !== 'undefined'
      ) {
        transition = transitions[transitionEvent];
        break;
      }
    }
    return transition;
  }

  /**
   * Set the HTML element target of this transition.
   * @param {HTMLElement} targetElement - The target of the transition.
   */
  function setElement(targetElement) {
    /*
      If the element has already been set,
      clear the transition classes from the old element.
    */
    if (_dom) {
      remove();
      animateOn();
    }
    _dom = targetElement;
    _dom.classList.add(_classes.BASE_CLASS);
    _transitionEndEvent = _getTransitionEndEvent(_dom);
  }

  /**
   * @returns {BaseTransition} An instance.
   */
  function init() {
    _transitionCompleteBinded = _transitionComplete.bind(this);
    _addEventListenerBinded = _addEventListener.bind(this);
    setElement(element);

    return this;
  }

  /**
   * @returns {boolean} Whether the transition has a duration or not.
   *   Returns false if this transition has not been initialized.
   */
  function isAnimated() {
    if (!_dom) {
      return false;
    }
    return !_dom.classList.contains(BaseTransition.NO_ANIMATION_CLASS);
  }

  /**
   * @param {string} className - A CSS class.
   * @returns {boolean} False if the class is already applied
   *   or the transition is not initialized,
   *   otherwise true if the class was applied.
   */
  function applyClass(className) {
    if (!_dom) {
      return false;
    }
    if (!_isFlushed) {
      _flush();
      _isFlushed = true;
    }

    if (_dom.classList.contains(className)) {
      return false;
    }

    _removeEventListener();
    _dom.classList.remove(_lastClass);
    _lastClass = className;
    _addEventListenerBinded();
    _dom.classList.add(_lastClass);

    return true;
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
