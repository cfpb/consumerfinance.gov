import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { toArray } from '../../util';
import { isWaiting } from '../../reducers/choice-reducer';
import transportationMap from '../../data-types/transportation-map';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-yes-plans-review',
  CHOICE_HEADING: 'js-review-choice-heading',
  TRANSPORTATION_TYPE: 'js-transportation-option',
  DETAILS: 'yes-route-details',
  NOTIFICATION: 'js-route-notification'
} );

/**
 * ReviewDetailsView
 *
 * @class
 *
 * @classdesc View to display details of user's route selections in the
 * review section
 *
 * @param {HTMLElement} element The container node for this view
 * @param {Object} props The additional properties supplied to this view
 * @param {YesStore} props.store The public API exposed by the Store class
 * @param {Function} props.routeDetailsView The child view managed by this view,
 * duplicates the information shown in the details section of the route option
 * form
 * @returns {Object} This view's public API
 */
function reviewDetailsView( element, { store, routeDetailsView } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _detailsEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.DETAILS }` )
  );
  const _transportationTypeEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_TYPE }` )
  );
  const _reviewChoiceHeadingEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.CHOICE_HEADING }` )
  );
  const _notificationEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.NOTIFICATION }` )
  );

  const _detailsViews = [];

  /**
   * Event handler to update child views with current state
   * @param {Object} _ The previous state value from store (unused)
   * @param {Object} state The current application state
   */
  function _handleStateUpdate( _, state ) {
    const otherRoutes = state.routes.routes.slice();
    const preferredRoute = otherRoutes.splice( state.routeChoice, 1 );
    const finalRoutes = preferredRoute.concat( otherRoutes );

    _detailsViews.forEach( ( view, index ) => {
      const route = finalRoutes[index] || {};

      if ( Object.keys( route ).length ) {
        const transporationDesc = transportationMap[route.transportation];
        _transportationTypeEls[index].textContent = transporationDesc;

        view.render( {
          budget: state.budget,
          route
        } );
      }
    } );

    if ( isWaiting( state ) ) {
      _reviewChoiceHeadingEls.forEach( el => el.classList.add( 'u-hidden' ) );
    } else {
      _reviewChoiceHeadingEls.forEach( el => el.classList.remove( 'u-hidden' ) );
    }
  }

  /**
   * Initialize the child views this view manages.
   */
  function _initSubviews() {
    _detailsEls.reduce( ( memo, node, index ) => {
      const view = routeDetailsView( node, {
        alertTarget: _notificationEls[index],
        hasDefaultTodo: true
      } );

      memo.push( view );

      view.init();

      return memo;
    }, _detailsViews );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initSubviews();
        _handleStateUpdate( {}, store.getState() );
        store.subscribe( _handleStateUpdate );
      }
    }
  };
}

reviewDetailsView.CLASSES = CLASSES;

export default reviewDetailsView;
