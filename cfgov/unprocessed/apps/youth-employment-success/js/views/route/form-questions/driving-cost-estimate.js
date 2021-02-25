import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { TRANSPORTATION } from '../../../data-types/transportation-map';

const CLASSES = {
  CONTAINER: 'js-driving-estimate'
};

/**
 * DrivingCostEstimateView
 * @class
 *
 * @classdesc View to manage the read-only driving cost estimate field
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} This view's public methods
 */
function drivingCostEstimate( element ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.classList.add( 'u-hidden' );
      }
    },
    render( route ) {
      if ( route.transportation === TRANSPORTATION.DRIVE ) {
        _dom.classList.remove( 'u-hidden' );
      } else {
        _dom.classList.add( 'u-hidden' );
      }
    }
  };
}

drivingCostEstimate.CLASSES = CLASSES;

export default drivingCostEstimate;
