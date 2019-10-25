import Expandable from 'cf-expandables/src/Expandable';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import { toArray } from './util';
import averageCostView from './views/average-cost';
import budgetFormView from './budget-form-view';
import createRoute from './models/route';
import daysPerWeekView from './views/days-per-week';
import drivingCostEstimateView from './views/driving-cost-estimate';
import expandableView from './views/expandable';
import goalsView from './views/goals';
import milesView from './views/miles';
import printButton from './views/review/print-button';
import reviewChoiceView from './views/review/choice';
import reviewDetailsView from './views/review/details';
import reviewGoalsView from './views/review/goals';
import routeDetailsView from './views/route/details';
import routeOptionFormView from './views/route/option-view';
import routeOptionToggleView from './views/route/option-toggle-view';
import store from './store';
import transitTimeView from './views/transit-time';

toArray(
  document.querySelectorAll( 'input, textarea' )
).forEach( input => {
  input.removeAttribute( 'disabled' );
} );

const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;
const OPTION_TOGGLE_CLASSES = routeOptionToggleView.CLASSES;
const GOALS_CLASSES = goalsView.CLASSES;
const REVIEW_GOALS_CLASSES = reviewGoalsView.CLASSES;

const goalsViewEl = document.querySelector( ` .${ GOALS_CLASSES.CONTAINER }` );
const goalsFormView = goalsView( goalsViewEl, { store } );
goalsFormView.init();

const budgetFormEl = document.querySelector( `.${ BUDGET_CLASSES.FORM }` );
const budgetForm = budgetFormView( budgetFormEl, { store } );
budgetForm.init();

const expandables = Expandable.init();

expandables.forEach( expandable => {
  expandableView( expandable.element, {
    expandable
  } ).init();
} );

const routeOptionForms = expandables.map( ( expandable, index ) => {
  store.dispatch( addRouteOptionAction( createRoute() ) );

  const routeOptionsEl = expandable.element.querySelector( `.${ OPTION_CLASSES.FORM }` );
  return routeOptionFormView( routeOptionsEl, {
    store,
    routeIndex: index,
    routeDetailsView,
    averageCostView,
    daysPerWeekView,
    drivingCostEstimateView,
    milesView,
    transitTimeView
  } );
} );

expandables[0].element.querySelector( '.o-expandable_target' ).click();
expandables[1].element.classList.add( 'u-hidden' );
routeOptionToggleView(
  document.querySelector( `.${ OPTION_TOGGLE_CLASSES.BUTTON }` ), {
    expandable: expandables[1],
    routeOptionForm: routeOptionForms[1]
  }
).init();

/**
 * Only initialize the first route option form, the second is initialized when
 * the user clicks the 'add another option' button.
*/
routeOptionForms[0].init();

reviewChoiceView(
  document.querySelector( `.${ reviewChoiceView.CLASSES.CONTAINER }` ),
  { store }
).init();

const reviewDetailsEl = document.querySelector(
  `.${ reviewDetailsView.CLASSES.CONTAINER }`
);
reviewDetailsView( reviewDetailsEl, {
  store, routeDetailsView
} ).init();

reviewGoalsView(
  document.querySelector( `.${ REVIEW_GOALS_CLASSES.CONTAINER }`
  ), { store }
).init();

printButton(
  document.querySelector( `.${ printButton.CLASSES.BUTTON }` )
).init();
