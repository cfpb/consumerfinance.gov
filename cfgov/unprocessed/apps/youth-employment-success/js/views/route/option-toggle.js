import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

const CLASSES = Object.freeze( {
  BUTTON: 'm-yes-route-option'
} );

/**
 * RouteOptionToggleView
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @param {object} props Additional properties to be supplied to the view
 * @returns {Object} The view's public methods
 */
function routeOptionToggleView( element, { expandable, routeOptionForm } ) {
  const _dom = checkDom( element, CLASSES.BUTTON );

  /**
   * Show additional route option expandable, hiding the button
   * Initialize the new route option form
   */
  function _showRouteOption() {
    expandable.element.querySelector( '.o-expandable_target' ).click();
    expandable.element.classList.remove( 'u-hidden' );
    _dom.classList.add( 'u-hidden' );
    _dom.removeEventListener( 'click', _showRouteOption );
    routeOptionForm.init();
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.addEventListener( 'click', _showRouteOption );
      }
    }
  };
}

routeOptionToggleView.CLASSES = CLASSES;

export default routeOptionToggleView;
