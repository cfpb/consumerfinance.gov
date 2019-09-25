import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';
import {
  routeSelector,
  updateTransportationAction
} from './reducers/route-option-reducer';
import inputView from './views/input';
import { toArray } from './util';
import TodoNotification from './todo-notification';

const CLASSES = Object.freeze( {
  FORM: 'o-yes-route-option',
  TRANSPORTATION_CHECKBOX: 'a-yes-route-mode',
  QUESTION_INPUT: 'a-yes-question'
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
  detailsView,
  averageCostView,
  daysPerWeekView,
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

        store.subscribe( ( _, nextState ) => {
          const currentRouteState = routeSelector(
            nextState.routes,
            routeIndex
          );

          detailsView.render( {
            budget: nextState.budget,
            route: currentRouteState
          } );
        } );
      }
    }
  };
}

RouteOptionFormView.CLASSES = CLASSES;

export default RouteOptionFormView;
