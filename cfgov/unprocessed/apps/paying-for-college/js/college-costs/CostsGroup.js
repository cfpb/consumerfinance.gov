import {
  add as addDataHook,
  checkDom,
  instantiateAll,
  setInitFlag,
  FlyoutMenu,
  MaxHeightTransition,
  EventObserver,
} from '@cfpb/cfpb-design-system';

const BASE_CLASS = 'o-costs-group';

/**
 * CostsGroup
 * @class
 * @classdesc Initializes a new CostsGroup organism.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the organism.
 * @returns {CostsGroup} An instance.
 */
function CostsGroup(element) {
  const _dom = checkDom(element, BASE_CLASS);
  const _contentDom = _dom.querySelector(`.${BASE_CLASS}__content`);
  const _targetDom = _dom.querySelector(`.${BASE_CLASS}__header`);
  let _transition;
  let _flyout;

  /**
   * @returns {CostsGroup} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    // Add FlyoutMenu behavior data-js-hooks.
    addDataHook(_dom, 'behavior_flyout-menu');
    addDataHook(_contentDom, 'behavior_flyout-menu_content');
    addDataHook(_targetDom, 'behavior_flyout-menu_trigger');

    _configFlyout();

    return this;
  }

  /**
   * Configure the flyout.
   */
  function _configFlyout() {
    _flyout = new FlyoutMenu(_dom);
    _transition = new MaxHeightTransition(_contentDom);
    _transition.init(MaxHeightTransition.CLASSES.MH_ZERO);
    _flyout.setTransition(
      _transition,
      _transition.maxHeightZero,
      _transition.maxHeightDefault,
    );
    _flyout.init();

    _flyout.addEventListener('expandbegin', () => {
      _targetDom.classList.remove('o-costs-group__header--collapsed');
      _targetDom.classList.add('o-costs-group__header--expanded');
    });

    _flyout.addEventListener('collapsebegin', () => {
      _targetDom.classList.remove('o-costs-group__header--expanded');
      _targetDom.classList.add('o-costs-group__header--collapsed');
    });
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;

  return this;
}

CostsGroup.BASE_CLASS = BASE_CLASS;
CostsGroup.init = (scope) => {
  instantiateAll(`.${BASE_CLASS}`, CostsGroup, scope);
};

export { CostsGroup };
