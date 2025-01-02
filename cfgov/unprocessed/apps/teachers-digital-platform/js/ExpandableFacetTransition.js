import BaseTransition from './BaseTransition.js';
import { EventObserver } from '@cfpb/cfpb-design-system';

// Exported constants.
const CLASSES = {
  CSS_PROPERTY: 'max-height',
  BASE_CLASS: 'o-expandable-facets__content--transition',
  EXPANDED: 'o-expandable-facets__content--expanded',
  COLLAPSED: 'o-expandable-facets__content--collapsed',
  OPEN_DEFAULT: 'o-expandable-facets__content--onload-open',
};

/**
 * ExpandableFacetTransition
 * @class
 * @classdesc Initializes new ExpandableFacetTransition behavior.
 * @param {HTMLElement} element - DOM element to apply move transition to.
 * @returns {ExpandableFacetTransition} An instance.
 */
function ExpandableFacetTransition(element) {
  const _baseTransition = new BaseTransition(element, CLASSES, this);
  let previousHeight;

  /**
   * @param {Function} initialClass - The initial state for this transition.
   * @returns {ExpandableFacetTransition} An instance.
   */
  function init(initialClass) {
    _baseTransition.init(initialClass);
    this.addEventListener(
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
   * Handle the end of a transition.
   */
  function _transitionComplete() {
    if (element.classList.contains(CLASSES.EXPANDED)) {
      this.dispatchEvent('expandend', { target: this });

      if (element.scrollHeight > previousHeight) {
        element.style.maxHeight = element.scrollHeight + 'px';
      }
    } else if (element.classList.contains(CLASSES.COLLAPSED)) {
      this.dispatchEvent('collapseend', { target: this });
    }
  }

  /**
   * Toggle the expandable
   * @returns {ExpandableFacetTransition} An instance.
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
   * @returns {ExpandableFacetTransition} An instance.
   */
  function collapse() {
    this.dispatchEvent('collapsebegin', { target: this });

    previousHeight = element.scrollHeight;
    element.style.maxHeight = '0';
    _baseTransition.applyClass(CLASSES.COLLAPSED);

    return this;
  }

  /**
   * Expands the expandable content
   * @returns {ExpandableFacetTransition} An instance.
   */
  function expand() {
    this.dispatchEvent('expandbegin', { target: this });

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
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

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
ExpandableFacetTransition.CLASSES = CLASSES;

export default ExpandableFacetTransition;
