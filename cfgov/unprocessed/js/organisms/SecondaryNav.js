/* ==========================================================================
   SecondaryNav Organism
   ========================================================================== */

import {
  add as addDataHook,
  checkDom,
  setInitFlag,
  instantiateAll,
  MaxHeightTransition,
  EventObserver,
  FlyoutMenu,
} from '@cfpb/cfpb-atomic-component';

const BASE_CLASS = 'o-secondary-nav';

/**
 * SecondaryNav
 * @class
 * @classdesc Initializes a new SecondaryNav molecule.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the molecule.
 * @returns {SecondaryNav} An instance.
 */
function SecondaryNav(element) {
  // Internal vars.
  const _dom = checkDom(element, BASE_CLASS);
  let _targetDom;
  let _contentDom;

  // Animation vars.
  let _transition;
  let _flyout;

  /**
   * Set up and create the multiselect.
   * @returns {SecondaryNav} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    _targetDom = _dom.querySelector(`.${BASE_CLASS}_header`);
    _contentDom = _dom.querySelector(`.${BASE_CLASS}_content`);

    // Add behavior hooks.
    addDataHook(_dom, 'behavior_flyout-menu');
    addDataHook(_targetDom, 'behavior_flyout-menu_trigger');
    addDataHook(_contentDom, 'behavior_flyout-menu_content');

    const initialClass = MaxHeightTransition.CLASSES.MH_ZERO;
    _transition = new MaxHeightTransition(_contentDom).init(initialClass);

    // Create root menu.
    _flyout = new FlyoutMenu(_dom);

    _flyout.setTransition(
      _transition,
      _transition.maxHeightZero,
      _transition.maxHeightDefault
    );

    _flyout.init();

    return this;
  }

  // Attach public events.
  this.init = init;
  this.collapse = () => _flyout.collapse();

  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  return this;
}

SecondaryNav.BASE_CLASS = BASE_CLASS;
SecondaryNav.init = (scope) =>
  instantiateAll(`.${SecondaryNav.BASE_CLASS}`, SecondaryNav, scope);

export { SecondaryNav };
