import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';

const CLASSES = {
  BUTTON: 'yes-print-button'
};

/**
 * PrintButton
 * @class
 *
 * @classdesc Simple view for calling the system print dialog
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} The view's public methods
 */
function printButton( element ) {
  const _dom = checkDom( element, CLASSES.BUTTON );

  /**
   * Calls the system print dialog
   */
  function _print() {
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
