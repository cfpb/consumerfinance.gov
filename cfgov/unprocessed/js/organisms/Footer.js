import {
  checkDom,
  instantiateAll,
  setInitFlag,
} from '@cfpb/cfpb-design-system';
import { init as footerButtonInit } from '../modules/footer-button.js';

const BASE_CLASS = 'o-footer';

/**
 * Footer
 * @class
 * @classdesc Initializes the organism.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the organism.
 * @returns {Footer} An instance.
 */
function Footer(element) {
  const _dom = checkDom(element, BASE_CLASS);

  /**
   * @returns {Footer} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    footerButtonInit();

    return this;
  }

  this.init = init;

  return this;
}

Footer.BASE_CLASS = BASE_CLASS;
Footer.init = (scope) => instantiateAll(`.${Footer.BASE_CLASS}`, Footer, scope);

export { Footer };
