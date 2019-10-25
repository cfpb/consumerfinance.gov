import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import { toArray } from '../../util';

const CLASSES = {
  BUTTON: 'yes-print-button',
  NO_PRINT: 'js-no-print',
  HIDE: 'u-hide-on-print'
};

/**
 * PrintButton
 * @class
 *
 * @classdesc Simple view for calling the system print dialog when the
 * user wants to print their final plan. Toggles visibility of elements
 * that should not be printed.
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} The view's public methods
 */
function printButton( element ) {
  const _dom = checkDom( element, CLASSES.BUTTON );

  /**
   * When printing has finished, show all the hidden elements
   */
  function _onAfterPrint() {
    toArray(
      document.querySelectorAll( `.${ CLASSES.NO_PRINT }.${ CLASSES.HIDE }` )
    )
      .forEach( el => el.classList.remove( `${ CLASSES.HIDE }` ) );

    window.removeEventListener( 'focus', _onAfterPrint );
  }

  /**
   * Calls the system print dialog
   */
  function _print() {
    /* I believe we need to query each time as elements may have been
       added to the DOM during the tool's lifecycle on the page */
    toArray(
      document.querySelectorAll( `.${ CLASSES.NO_PRINT }` )
    )
      .forEach( el => el.classList.add( `${ CLASSES.HIDE }` ) );

    window.addEventListener( 'focus', _onAfterPrint );
    window.print();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.addEventListener( 'click', _print );
      }
    }
  };
}

printButton.CLASSES = CLASSES;

export default printButton;
