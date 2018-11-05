// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import * as footerButton from '../modules/footer-button';
import { UNDEFINED } from '../modules/util/standard-type';

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
   * @returns {Footer|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return UNDEFINED;
    }

    footerButton.init();

    return this;
  }

  this.init = init;

  return this;
}

export default Footer;
