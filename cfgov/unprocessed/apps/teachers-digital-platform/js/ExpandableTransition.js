// Required modules.
import BaseTransition from './BaseTransition.js';
import { EventObserver } from '@cfpb/cfpb-design-system';

// Exported constants.
const CLASSES = {
  CSS_PROPERTY: 'max-height',
  BASE_CLASS: 'o-expandable__content--transition',
  EXPANDED: 'o-expandable__content--expanded',
  COLLAPSED: 'o-expandable__content--collapsed',
  OPEN_DEFAULT: 'o-expandable__content--onload-open',
};

/**
 * ExpandableTransition
 * @class
 * @classdesc Initializes new ExpandableTransition behavior.
 * @param {HTMLElement} element - DOM element to apply move transition to.
 * @returns {ExpandableTransition} An instance.
 */
function ExpandableTransition(element) {
  const _baseTransition = new BaseTransition(element, CLASSES);
  let previousHeight;

  /**
   * Handle the end of a transition.
   */
  function _transitionComplete() {
    if (element.classList.contains(CLASSES.EXPANDED)) {
      this.dispatchEvent('expandEnd', { target: this });

      if (element.scrollHeight > previousHeight) {
        element.style.maxHeight = element.scrollHeight + 'px';
      }
    } else if (element.classList.contains(CLASSES.COLLAPSED)) {
      this.dispatchEvent('collapseEnd', { target: this });
    }
  }

  /**
   * @returns {ExpandableTransition} An instance.
   */
  function init() {
    _baseTransition.init();
    _baseTransition.addEventListener(
      BaseTransition.END_EVENT,
      _transitionComplete.bind(this),
    );

    if (element.classList.contains(CLASSES.OPEN_DEFAULT)) {
      this.expand();
    } else {
      this.collapse();
    }

    return this;
  }

  /**
   * Toggle the expandable
   * @returns {ExpandableTransition} An instance.
   */
  function toggleExpandable() {
    if (element.classList.contains(CLASSES.COLLAPSED)) {
      this.expand();
    } else {
      this.collapse();
    }

    return this;
  }

  /**
   * Collapses the expandable content
   * @returns {ExpandableTransition} An instance.
   */
  function collapse() {
    this.dispatchEvent('collapseBegin', { target: this });

    previousHeight = element.scrollHeight;
    element.style.maxHeight = '0';
    _baseTransition.applyClass(CLASSES.COLLAPSED);

    return this;
  }

  /**
   * Expands the expandable content
   * @returns {ExpandableTransition} An instance.
   */
  function expand() {
    this.dispatchEvent('expandBegin', { target: this });

    if (!previousHeight || element.scrollHeight > previousHeight) {
      previousHeight = element.scrollHeight;
    }

    element.style.maxHeight = previousHeight + 'px';
    _baseTransition.applyClass(CLASSES.EXPANDED);

    return this;
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
  this.remove = _baseTransition.remove;

  this.init = init;
  this.toggleExpandable = toggleExpandable;
  this.collapse = collapse;
  this.expand = expand;

  return this;
}

// Public static properties.
ExpandableTransition.CLASSES = CLASSES;

export default ExpandableTransition;
