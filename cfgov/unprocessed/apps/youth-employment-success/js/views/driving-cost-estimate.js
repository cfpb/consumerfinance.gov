import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';
import { TRANSPORTATION } from '../data/transportation-map';

const CLASSES = {
  CONTAINER: 'js-driving-estimate',
  COST_PER_MILE: 'js-cost-per-mile'
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
  const _costPerMileEl = _dom.querySelector( `.${ CLASSES.COST_PER_MILE }` );

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.classList.add( 'u-hidden' );
      }
    },
    render( route ) {
      if ( route.transportation === TRANSPORTATION.DRIVE ) {
        _dom.classList.remove( 'u-hidden' );
        // Magic number for now, until we get an actual average cost
        _costPerMileEl.textContent = '$1.80';
      } else {
        _dom.classList.add( 'u-hidden' );
        _costPerMileEl.textContent = '';
      }
    }
  };
}

drivingCostEstimate.CLASSES = CLASSES;

export default drivingCostEstimate;
