import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';

const CLASSES = Object.freeze( {
  BUTTON: 'm-yes-route-option'
} );

/**
 * AddRouteOptionView
 * @class
 *
 * @classdesc Adds event handling to add route option button
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {Object} props Additional properties to be supplied to the view
 * @param {Function} props.onAddExpandable Function called on click that should
 * handle instantiating an new Expandable and associated form components.
 * @returns {Object} The view's public methods
 */
function addRouteOptionView( element, { onAddExpandable } ) {
  const _dom = checkDom( element, CLASSES.BUTTON );

  if ( !onAddExpandable || typeof onAddExpandable !== 'function' ) {
    throw new TypeError( 'View must be called with `onAddExpandable` function prop.' );
  }

  /**
   * Call supplied handler function to dynamically create new route option
   * instances
   */
  function _showRouteOption() {
    onAddExpandable();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.addEventListener( 'click', _showRouteOption );
      }
    }
  };
}

addRouteOptionView.CLASSES = CLASSES;

export default addRouteOptionView;
