import { assign, formatNegative, isNumber, toArray, toPrecision } from '../../util';
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { ALERT_TYPES } from '../../data-types/notifications';
import { getPlanItem } from '../../data-types/todo-items';
import money from '../../money';
import notificationsView from '../notifications';
import transportationMap from '../../data-types/transportation-map';
import validate from '../../validators/route-option';

const CLASSES = Object.freeze( {
  AVERAGE_COST_HELPER: 'js-average-cost-helper',
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
 * @param {HTMLElement} todosEl Reference to the actual todo list ul element
 * @param {array} todos A list of types of actions the user should take
 * when considering this route option
 * @param {Boolean} hasDefault Whether or not this list has a default item
 * @returns {Node} An HTML documentFragment with a collection of LI elements
 */
function buildTodoListNodes( todosEl, todos = [], hasDefault ) {
  const fragment = document.createDocumentFragment();
  const defaultItem = hasDefault && todosEl.children && todosEl.children[0];

  if ( defaultItem ) {
    fragment.appendChild( defaultItem.cloneNode( true ) );
  }

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

const DEFAULT_COST_ESTIMATE = '—';
const WEEKLY_COST = 4.0;
const AAA_ESTIMATED_COST_PER_MILE = 0.80;

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

  const validDaysPerWeek = isMonthlyCost === null ? null : daysPerWeek;

  return calculatePerMonthCost( averageCost, validDaysPerWeek );
}

function useDefaultCostEstimate( value ) {
  if ( !isNumber( value ) && !value ) {
    return true;
  }

  if ( value === DEFAULT_COST_ESTIMATE ) {
    return true;
  }

  return false;
}

/**
 * Calculates the daily cost of driving
 * @param {string} numberOfMiles Number of miles user expects to drive each day
 * @returns {Number} The cost, in dollars, of driving each day
 */
function calculateDrivingDailyCost( numberOfMiles = 0 ) {
  if ( useDefaultCostEstimate( numberOfMiles ) ) {
    return DEFAULT_COST_ESTIMATE;
  }

  return money.toDollars(
    parseFloat( numberOfMiles ) * AAA_ESTIMATED_COST_PER_MILE
  );
}

/**
 *
 * @param {number} dailyCost The daily cost of the user's chosen mode of transportation
 * @param {string} daysPerWeek The number of days per week the user expects to make the trip
 * @returns {String|Number} Retuns '-' if daysPerWeek is not supplied, otherwise returns the monthly cost
 */
function calculatePerMonthCost( dailyCost, daysPerWeek ) {
  if ( useDefaultCostEstimate( daysPerWeek ) || useDefaultCostEstimate( dailyCost ) ) {
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
  if ( useDefaultCostEstimate( budget ) || useDefaultCostEstimate( transportationEstimate ) ) {
    return DEFAULT_COST_ESTIMATE;
  }

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
 * Toggle the visibility of a node
 * @param {HTMLElement} node The element to show or hide
 * @param {Boolean} visibility Whether to show or hide the element
 */
function updateNodeVisibility( node, visibility ) {
  const predicate = typeof visibility === 'function' ?
    visibility : () => visibility;

  if ( predicate() ) {
    node.classList.add( 'u-hidden' );
  } else {
    node.classList.remove( 'u-hidden' );
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
function routeDetailsView( element, { alertTarget, hasDefaultTodo = false } ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  const _transportationEl = toArray(
    _dom.querySelectorAll( `.${ CLASSES.TRANSPORTATION_TYPE }` )
  );
  const _averageCostHelperEl = _dom.querySelector( `.${ CLASSES.AVERAGE_COST_HELPER }` );
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
   * @param {DocumentFragment} fragment Collection of new li nodes representing
   * todos the user may have added
   */
  function updateTodoList( fragment ) {
    updateDom( _todoItemsEl, fragment, hasDefaultTodo );

    if ( _todoItemsEl.children.length ) {
      _todoListEl.classList.remove( 'u-hidden' );
    } else {
      _todoListEl.classList.add( 'u-hidden' );
    }
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        alertView = notificationsView(
          document.querySelector( `.${ notificationsView.CLASSES.CONTAINER }` )
        );
        alertView.init();
      }

      return this;
    },
    render( { budget, route } ) {
      const costEstimate = getCalculationFn( route );
      const remainingBudget = money.subtract( budget.earned, budget.spent );
      const nextRemainingBudget = updateRemainingBudget(
        String( remainingBudget ),
        costEstimate
      );
      const isFormValid = validate( assign( {}, budget, route ) );
      const valuesForNotification = {
        [ALERT_TYPES.HAS_TODOS]: Boolean(
          route.transportation && route.actionPlanItems.length
        ),
        [ALERT_TYPES.INVALID]: Boolean( route.transportation && !isFormValid ),
        [ALERT_TYPES.IN_BUDGET]: isFormValid && nextRemainingBudget >= 0,
        [ALERT_TYPES.OUT_OF_BUDGET]: isFormValid && nextRemainingBudget < 0
      };
      const todoListFragment = buildTodoListNodes(
        _todoItemsEl, route.actionPlanItems, hasDefaultTodo
      );

      updateNodeVisibility( _averageCostHelperEl, route.isMonthlyCost );
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

      updateDom( _timeHoursEl, route.transitTimeHours || '-' );
      updateDom( _timeMinutesEl, route.transitTimeMinutes || '-' );
      updateTodoList( todoListFragment );

      alertView.render( {
        alertValues: valuesForNotification,
        alertTarget
      } );
    }
  };
}

routeDetailsView.CLASSES = CLASSES;

export default routeDetailsView;
