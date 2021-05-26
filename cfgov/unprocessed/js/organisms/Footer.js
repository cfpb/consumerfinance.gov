// Required modules.
import * as footerButton from '../modules/footer-button';
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

/**
 * Footer
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Footer} An instance.
 */
function Footer( element ) {

  const BASE_CLASS = 'o-footer';

  const _dom = checkDom( element, BASE_CLASS );

  /**
   * @returns {Footer} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    footerButton.init();

    return this;
  }

  this.init = init;

  return this;
}

export default Footer;
