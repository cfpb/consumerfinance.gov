import { assign, formatNegative, toArray, toPrecision } from '../../util';
import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import { ALERT_TYPES } from '../../data-types/notifications';
import { getPlanItem } from '../../data-types/todo-items';
import money from '../../money';
import notificationsView from '../notifications';
import transportationMap from '../../data-types/transportation-map';
import validate from '../../validators/route-option';

const CLASSES = Object.freeze( {
  CONTAINER: 'yes-route-details',
  TRANSPORTATION_TYPE: 'js-transportation-type',
  BUDGET: 'js-budget',
  DAYS_PER_WEEK: 'js-days-per-week',
  TOTAL_COST: 'js-total-cost',
  BUDGET_REMAINING: 'js-budget-left',
  TIME_HOURS: 'js-time-hours',
  TIME_MINUTES: 'js-time-minutes',
  TODO_LIST: 'js-todo-list',
  TODO_ITEMS: 'js-todo-items'
} );

/**
 * Generates a list of LI elements to be passed back to the DOM
 *
 * @param {array} todos A list of types of actions the user should take
 * when considering this route option
 * @returns {Node} An HTML documentFragment with a collection of LI elements
 */
function updateTodoList( todos = [] ) {
  const fragment = document.createDocumentFragment();

  todos.forEach( todo => {
    const realTodo = getPlanItem( todo );

    if ( realTodo ) {
      const li = document.createElement( 'li' );
      li.textContent = realTodo;

      fragment.appendChild( li );
    }
  } );

  return fragment;
}

const DEFAULT_COST_ESTIMATE = '0';

// Rough estimate to account for weeks that have more or less days
const WEEKLY_COST = 4.0;

// This number will be pulled from a data set, for now, its magic
const ESTIMATED_COST_PER_MILE = 1.8;

/**
 * Given a route configuration, determine what calculations need to be performed
 * to give the user an accurate (within the scope of the tool) estimate about
 * the average monthly cost of their chose transportation option.
 *
 * @param {object} route A route object from the route reducer.
 * @returns {Number} The average monthly cost the user can expect to pay for transportation
 */
function getCalculationFn( route ) {
  const {
    isMonthlyCost,
    transportation,
    averageCost,
    daysPerWeek,
    miles
  } = route;

  if ( transportation === 'Drive' ) {
    const realDailyCost = calculateDrivingDailyCost( miles );

    return calculatePerMonthCost( realDailyCost, daysPerWeek );
  } else if ( isMonthlyCost ) {
    return averageCost;
  }

  return calculatePerMonthCost( averageCost, daysPerWeek );
}

/**
 * Calculates the daily cost of driving
 * @param {string} numberOfMiles Number of miles user expects to drive each day
 * @returns {Number} The cost, in dollars, of driving each day
 */
function calculateDrivingDailyCost( numberOfMiles = 0 ) {
  return money.toDollars(
    parseFloat( numberOfMiles ) * ESTIMATED_COST_PER_MILE
  );
}

/**
 *
 * @param {number} dailyCost The daily cost of the user's chosen mode of transportation
 * @param {string} daysPerWeek The number of days per week the user expects to make the trip
 * @returns {String|Number} Retuns '-' if daysPerWeek is not supplied, otherwise returns the monthly cost
 */
function calculatePerMonthCost( dailyCost, daysPerWeek ) {
  if ( !daysPerWeek ) {
    return DEFAULT_COST_ESTIMATE;
  }

  const normalizedDays = Number( daysPerWeek ) > 7 ? 7 : daysPerWeek;

  return money.toDollars(
    money.toDollars( dailyCost ) *
    normalizedDays *
    WEEKLY_COST
  );
}

/**
 * Calculate the money remaining after transportation costs
 * @param {object} budget The monthly budget numbers the user specified, from the budget reducer
 * @param {string} transportationEstimate The estimated cost of transportation
 * @returns {Number} The user's remaining monthly money.
 */
function updateRemainingBudget( budget, transportationEstimate ) {
  return money.subtract(
    budget,
    transportationEstimate
  );
}

/**
 * Determine if a DOM node should update by seeing if the current value and the
 * next value are the same.
 * @param {*} lastValue Any value
 * @param {*} value Any value
 *
 * @returns {Boolean} Whether the node should update or not.
 */
function assertStateHasChanged( lastValue, value ) {
  if ( !lastValue && !value ) {
    return false;
  }

  return lastValue !== value;
}

/**
 * Updates a DOM node or collection of nodes
 * @param {HTMLElement|Array} node The node(s) to be updates
 * @param {*} nextValue The value with which to update the node(s)
 */
function updateDom( node, nextValue ) {
  if ( node ) {
    if ( 'length' in node ) {
      node.forEach( n => updateDomNode( n, nextValue ) );
    } else {
      updateDomNode( node, nextValue );
    }
  }
}

/**
 * 'Public' (to this class) function that handle node updates
 * @param {HTMLElement} node The node to be updates
 * @param {*} nextValue The value with which to update the node
 */
function updateDomNode( node, nextValue ) {
  const currentValue = node.textContent;

  if ( assertStateHasChanged( currentValue, nextValue ) ) {
    if ( nextValue instanceof HTMLElement || nextValue instanceof Node ) {
      node.innerHTML = '';
      node.appendChild( nextValue );
    } else {
      node.innerHTML = nextValue;
    }
  }
}

/**
 * RouteDetailsView
 * @class
 *
 * @classdesc View to handle updating the at-a-glance information
 * pertaining to the user's configured route
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} This view's public methods
 */
function routeDetailsView( element ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _transportationEl = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_TYPE }` )
  );
  const _budgetEl = _dom.querySelector( `.${ CLASSES.BUDGET }` );
  const _daysPerWeekEl = _dom.querySelector( `.${ CLASSES.DAYS_PER_WEEK }` );
  const _totalCostEl = _dom.querySelector( `.${ CLASSES.TOTAL_COST }` );
  const _budgetLeftEl = _dom.querySelector( `.${ CLASSES.BUDGET_REMAINING }` );
  const _timeHoursEl = _dom.querySelector( `.${ CLASSES.TIME_HOURS }` );
  const _timeMinutesEl = _dom.querySelector( `.${ CLASSES.TIME_MINUTES }` );
  const _todoListEl = _dom.querySelector( `.${ CLASSES.TODO_LIST }` );
  const _todoItemsEl = _dom.querySelector( `.${ CLASSES.TODO_ITEMS }` );

  let alertView;

  /**
   * Toggles the display of the todo list element and its children
   * @param {Array} todos The array of todos the user may have added
   */
  function _toggleTodoList( todos = [] ) {
    if ( todos.length ) {
      _todoListEl.classList.remove( 'u-hidden' );
    } else {
      _todoListEl.classList.add( 'u-hidden' );
    }

    updateDom( _todoItemsEl, updateTodoList( todos ) );
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        alertView = notificationsView(
          _dom.querySelector( `.${ notificationsView.CLASSES.CONTAINER }` )
        );
        alertView.init();
      }

      return this;
    },
    render( { budget, route } ) {
      const costEstimate = getCalculationFn( route );
      const remainingBudget = money.subtract( budget.earned, budget.spent );
      const nextRemainingBudget = updateRemainingBudget(
        remainingBudget,
        costEstimate
      );
      const dataToValidate = assign( {}, budget, route );
      const dataIsValid = validate( dataToValidate );
      const valuesForNotification = {
        [ALERT_TYPES.HAS_TODOS]: Boolean(
          route.transportation && route.actionPlanItems.length
        ),
        [ALERT_TYPES.INVALID]: Boolean( route.transportation && !dataIsValid ),
        [ALERT_TYPES.IN_BUDGET]: dataIsValid && nextRemainingBudget >= 0,
        [ALERT_TYPES.OUT_OF_BUDGET]: dataIsValid && nextRemainingBudget < 0
      };

      updateDom( _transportationEl, transportationMap[route.transportation] );
      updateDom( _budgetEl,
        formatNegative(
          toPrecision( remainingBudget, 2 )
        )
      );
      updateDom( _daysPerWeekEl, route.daysPerWeek );
      updateDom( _totalCostEl, toPrecision( costEstimate, 2 ) );
      updateDom( _budgetLeftEl,
        formatNegative(
          toPrecision( nextRemainingBudget, 2 )
        )
      );
      updateDom( _timeHoursEl, route.transitTimeHours );
      updateDom( _timeMinutesEl, route.transitTimeMinutes );
      if ( _todoListEl ) {
        _toggleTodoList( route.actionPlanItems );
      }

      alertView.render( valuesForNotification );
    }
  };
}

routeDetailsView.CLASSES = CLASSES;

export default routeDetailsView;
