// Required modules.
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import BaseTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/BaseTransition';

// Exported constants.
const CLASSES = {
  CSS_PROPERTY: 'max-height',
  BASE_CLASS:   'o-expandable-facets_content__transition',
  EXPANDED:     'o-expandable-facets_content__expanded',
  COLLAPSED:    'o-expandable-facets_content__collapsed',
  OPEN_DEFAULT: 'o-expandable-facets_content__onload-open'
};

/* eslint-disable max-lines-per-function */
/**
 * ExpandableFacetTransition
 * @class
 *
 * @classdesc Initializes new ExpandableFacetTransition behavior.
 *
 * @param {HTMLNode} element - DOM element to apply move transition to.
 * @returns {ExpandableFacetTransition} An instance.
 */
function ExpandableFacetTransition( element ) {
  const _baseTransition = new BaseTransition( element, CLASSES );
  let previousHeight;

  /**
   * @returns {ExpandableFacetTransition} An instance.
   */
  function init() {
    _baseTransition.init();
    _baseTransition.addEventListener(
      BaseTransition.END_EVENT,
      _transitionComplete.bind( this )
    );

    if ( element.classList.contains( CLASSES.OPEN_DEFAULT ) ) {
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
    if ( element.classList.contains( CLASSES.EXPANDED ) ) {
      this.dispatchEvent( 'expandEnd', { target: this } );

      if ( element.scrollHeight > previousHeight ) {
        element.style.maxHeight = element.scrollHeight + 'px';
      }
    } else if ( element.classList.contains( CLASSES.COLLAPSED ) ) {
      this.dispatchEvent( 'collapseEnd', { target: this } );
    }
  }

  /**
   * Toggle the expandable
   * @returns {ExpandableFacetTransition} An instance.
   */
  function toggleExpandable() {
    if ( element.classList.contains( CLASSES.COLLAPSED ) ) {
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
    this.dispatchEvent( 'collapseBegin', { target: this } );

    previousHeight = element.scrollHeight;
    element.style.maxHeight = '0';
    _baseTransition.applyClass( CLASSES.COLLAPSED );

    return this;
  }

  /**
   * Expands the expandable content
   * @returns {ExpandableFacetTransition} An instance.
   */
  function expand() {
    this.dispatchEvent( 'expandBegin', { target: this } );

    if ( !previousHeight || element.scrollHeight > previousHeight ) {
      previousHeight = element.scrollHeight;
    }

    element.style.maxHeight = previousHeight + 'px';
    _baseTransition.applyClass( CLASSES.EXPANDED );

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
/* eslint-enable max-lines-per-function */

// Public static properties.
ExpandableFacetTransition.CLASSES = CLASSES;

export default ExpandableFacetTransition;
