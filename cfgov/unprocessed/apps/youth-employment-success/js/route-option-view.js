import { checkDom, setInitFlag } from '../../../js/modules/util/atomic-helpers';
import {
  routeSelector,
  updateDaysPerWeekAction,
  updateTransportationAction
} from './reducers/route-option-reducer';
import inputView from './input-view';
import { toArray } from './util';
import transitTimeView from './views/transit-time';

const CLASSES = Object.freeze( {
  FORM: 'o-yes-route-option',
  TRANSPORTATION_CHECKBOX: 'a-yes-route-mode',
  QUESTION_INPUT: 'a-yes-question'
} );

const actionMap = Object.freeze( {
  daysPerWeek: updateDaysPerWeekAction,
} );

/**
 * Map of the fields this form manages that are hidden or shown conditionally,
 * and the predicate functions that determine the field's state
 */
const toggleableFields = {
<<<<<<< HEAD
  miles: state => state.transportation === 'Drive'
=======
  daysPerWeek: state => state.transportation === 'Drive' || state.isCostPerDay
>>>>>>> Fills in miles combo view
};

/**
 * Hide an input and clear its value
 * @param {HTMLElement} node dom element to be toggled
 */
function hideToggleableField( node ) {
  if ( !node ) return;
  // need to add an action to update the store somewhere
  node.value = '';
  node.classList.add( 'u-hidden' );
}

/**
 ** Show an input
 * @param {HTMLElement} node dom element to be toggled
 */
function showToggleableField( node ) {
  node.classList.remove( 'u-hidden' );
}

/**
 *
 * @param {HTMLElement} node the node to be updated
 * @param {boolean} flag indicates if node is hidden or shown
 */
function updateNode( node, flag ) {
  if ( flag ) {
    showToggleableField( node );
  } else {
    hideToggleableField( node );
  }
}

/**
 * Determine if value in store has changed since last state update
 * @param {*} lastValue the old value of the state item
 * @param {*} currentValue the new value of the state item
 * @returns {boolean} Whether the value has changed
 */
function checkHasStateChanged( lastValue, currentValue ) {
  return lastValue !== currentValue || ( !lastValue && !currentValue );
}

/**
 * Updates togglebale inputs this view controls
 * @param {object} inputs node names with ref to dom node as value
 * @param {*} prevState previous state of the app
 * @param {*} state current state of the app
 */
function updateVisibleInputs( inputs, prevState, state ) {
  for ( const name in toggleableFields ) {
    if ( toggleableFields.hasOwnProperty( name ) ) {
      const predicate = toggleableFields[name];
      const stateHasChanged = checkHasStateChanged(
        prevState[name],
        state[name]
      );

      if ( stateHasChanged ) {
        updateNode( inputs[name], predicate( state ) );
      }
    }
  }
}

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
<<<<<<< HEAD
  daysPerWeekView
=======
  milesView
>>>>>>> Fills in miles combo view
} ) {
  const _dom = checkDom( element, CLASSES.FORM );
  const _transportationOptionEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_CHECKBOX }` )
  );
  const _textInputEls = toArray(
    _dom.querySelectorAll( `.${ CLASSES.QUESTION_INPUT }` )
  );
  const _inputMap = _textInputEls.reduce( ( memo, node ) => {
    const maybeNode = node.tagName === 'INPUT' ? node : node.querySelector( 'input' );

    if ( !maybeNode ) {
      return memo;
    }

    memo[maybeNode.getAttribute( 'data-js-name' )] = maybeNode;

    return memo;
  }, {} );

  /**
   * Updates form state from child input text nodes
   * @param {object} updateObject object with DOM event and field name
   */
  function _setQuestionResponse( { name, event } ) {
    const action = actionMap[name];
    const { target: { value }} = event;

    if ( action ) {
      store.dispatch( action( {
        routeIndex,
        value
      } ) );
    }
  }

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

  /**
   * Initialize input nodes this form view manages
   */
  function _initQuestions() {
    _textInputEls.forEach( node => inputView( node, {
      events: { input: _setQuestionResponse }
    } )
      .init()
    );
  }

  const boundUpdate = updateVisibleInputs.bind( null, _inputMap );

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _initRouteOptions();
        _initQuestions();
        transitTimeView(
          _dom.querySelector( `.${ transitTimeView.CLASSES.CONTAINER }` ),
          { store, routeIndex }
        ).init();

        averageCostView(
          _dom.querySelector( `.${ averageCostView.CLASSES.CONTAINER }` ),
          { store, routeIndex }
        ).init();

        daysPerWeekView(
          _dom.querySelector( `.${ daysPerWeekView.CLASSES.CONTAINER }` ),
          { store, routeIndex }
        ).init();

        milesView( _dom.querySelector( `.${ milesView.CLASSES.CONTAINER }` ), {
          store, routeIndex
        } ).init();

        detailsView.init();

        const currentState = routeSelector(
          store.getState().routes, routeIndex
        );

        boundUpdate( currentState, currentState );

        store.subscribe( ( prevState, nextState ) => {
          const currentRouteState = routeSelector(
            nextState.routes,
            routeIndex
          );

          boundUpdate(
            routeSelector( prevState.routes, routeIndex ),
            currentRouteState
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
