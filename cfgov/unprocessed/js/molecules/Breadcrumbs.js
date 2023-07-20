import {
  checkDom,
  instantiateAll,
  setInitFlag,
} from '@cfpb/cfpb-atomic-component';

const BASE_CLASS = 'm-breadcrumbs';

/**
 * Breadcrumbs
 * @class
 * @classdesc Initializes a new Breadcrumbs molecule.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the molecule.
 * @returns {Breadcrumbs} An instance.
 */
function Breadcrumbs(element) {
  const _dom = checkDom(element, BASE_CLASS);
  let toggle;
  let crumbs;

  /**
   * @returns {Breadcrumbs} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    crumbs = _dom.querySelector(`.${BASE_CLASS}_crumbs`);
    _hideCrumbs(crumbs);

    toggle = _dom.querySelector(`.${BASE_CLASS}_toggle`);
    toggle.addEventListener('click', _toggleClicked);
  }

  function _hideCrumbs(crumbs) {
    _dom.classList.remove(`${BASE_CLASS}__expanded`);
    crumbs.setAttribute('aria-expanded', 'false');
  }

  function _showCrumbs(crumbs) {
    _dom.classList.add(`${BASE_CLASS}__expanded`);
    crumbs.setAttribute('aria-expanded', 'true');
  }

  function _toggleClicked() {
    _showCrumbs(crumbs);
    toggle.classList.add('u-hidden');
  }

  this.init = init;

  return this;
}

Breadcrumbs.BASE_CLASS = BASE_CLASS;
Breadcrumbs.init = (scope) =>
  instantiateAll(`.${Breadcrumbs.BASE_CLASS}`, Breadcrumbs, scope);

export { Breadcrumbs };
