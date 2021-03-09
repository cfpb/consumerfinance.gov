import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import {
  routeSelector,
  updateTransportationAction
} from '../../reducers/route-option-reducer';
import TodoNotification from '../../views/todo-notification';
import inputView from '../input';
import { toArray } from '../../util';
import { TRANSPORTATION } from '../../data-types/transportation-map';

const CLASSES = Object.freeze( {
  FORM: 'o-yes-route-option',
  TRANSPORTATION_CHECKBOX: 'a-yes-route-mode',
  QUESTION_INPUT: 'a-yes-question',
  DISCOUNT: 'js-discount-tip'
} );

/**
 * RouteOptionFormView
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *  The root DOM element for this view
 * @returns {Object} The view's public methods
 */
function RouteOptionFormView( element, {
  store,
  routeIndex,
  routeDetailsView,
  averageCostView,
  daysPerWeekView,
  drivingCostEstimateView,
  milesView,
  transitTimeView
} ) {
  const _dom = checkDom( element, CLASSES.FORM );
  const _transportationOptionEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_CHECKBOX }` )
  );

  /**
   * Updates state from child input radio nodes
   * @param {object} updateObject object with DOM event and field name
   */
  function _setSelected( { event } ) {
    const { target: { value }} = event;

    store.dispatch( updateTransportationAction( {
      routeIndex,
      value } ) );
  }

  /**
   * Toggles visibility of transportation option tooltip
   * @param {String} transportationOption The type of transportation the user has indicated
   */
  function _updateToolTip( transportationOption ) {
    const tooltip = _dom.querySelector( `.${ CLASSES.DISCOUNT }` );

    if ( transportationOption === TRANSPORTATION.WALK ) {
      tooltip.classList.add( 'u-hidden' );
    } else {
      tooltip.classList.remove( 'u-hidden' );
    }
  }

  /**
   * Initialize checkbox nodes this form view manages
   */
  function _initRouteOptions() {
    _transportationOptionEls.forEach( node => inputView( node, {
      events: { click: _setSelected },
      type: 'radio'
    } )
      .init()
    );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initRouteOptions();
        const drivingEstimateView = drivingCostEstimateView(
          _dom.querySelector( `.${ drivingCostEstimateView.CLASSES.CONTAINER }` )
        );

        const detailsContainer = routeDetailsView.CLASSES.CONTAINER;
        const detailsEl = _dom.querySelector( `.${ detailsContainer }` );
        const detailsView = routeDetailsView(
          detailsEl,
          {
            alertTarget: detailsEl.querySelector( '.js-route-inline-notification' )
          }
        );

        transitTimeView(
          _dom.querySelector( `.${ transitTimeView.CLASSES.CONTAINER }` ),
          { store, routeIndex, todoNotification: new TodoNotification() }
        ).init();

        averageCostView(
          _dom.querySelector( `.${ averageCostView.CLASSES.CONTAINER }` ),
          { store, routeIndex, todoNotification: new TodoNotification() }
        ).init();

        daysPerWeekView(
          _dom.querySelector( `.${ daysPerWeekView.CLASSES.CONTAINER }` ),
          { store, routeIndex, todoNotification: new TodoNotification() }
        ).init();

        milesView( _dom.querySelector( `.${ milesView.CLASSES.CONTAINER }` ), {
          store, routeIndex, todoNotification: new TodoNotification()
        } ).init();

        detailsView.init();
        drivingEstimateView.init();

        store.subscribe( ( _, state ) => {
          const currentRouteState = routeSelector(
            state.routes,
            routeIndex
          );

          detailsView.render( {
            budget: state.budget,
            route: currentRouteState
          } );
          drivingEstimateView.render( currentRouteState );
          _updateToolTip( currentRouteState.transportation );
        } );
      }
    }
  };
}

RouteOptionFormView.CLASSES = CLASSES;

export default RouteOptionFormView;
