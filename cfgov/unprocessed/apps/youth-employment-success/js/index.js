import Expandable from 'cf-expandables/src/Expandable';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import { toArray } from './util';
import addRouteOptionView from './add-route-option-view';
import averageCostView from './views/average-cost';
import budgetFormView from './budget-form-view';
import createRoute from './route.js';
import daysPerWeekView from './views/days-per-week';
import drivingCostEstimateView from './views/driving-cost-estimate';
import expandableView from './views/expandable';
import goalsView from './views/goals';
import milesView from './views/miles';
import printButton from './views/print-button';
import reviewChoiceView from './views/review/choice';
import reviewDetailsView from './views/review/details';
import reviewGoalsView from './views/review/goals';
import routeDetailsView from './views/route-details';
import routeOptionFormView from './route-option-view';
import store from './store';
import transitTimeView from './views/transit-time';

toArray(
  document.querySelectorAll( 'input, textarea' )
).forEach( input => {
  input.removeAttribute( 'disabled' );
} );

const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;
const OPTION_TOGGLE_CLASSES = addRouteOptionView.CLASSES;
const GOALS_CLASSES = goalsView.CLASSES;
const REVIEW_GOALS_CLASSES = reviewGoalsView.CLASSES;

// Create factory initializers for all of these view initialize calls, separate files?
const goalsViewEl = document.querySelector( ` .${ GOALS_CLASSES.CONTAINER }` );
const goalsFormView = goalsView( goalsViewEl, { store } );
goalsFormView.init();

const budgetFormEl = document.querySelector( `.${ BUDGET_CLASSES.FORM }` );
const budgetForm = budgetFormView( budgetFormEl, { store } );
budgetForm.init();

let expandables = [];

/**
 * Given a container element, initialize a new expandable and route option form. If
 * a DOM element is not supplied, clone the form 'template' element and initialize the
 * JS views with it.
 * @param {HTMLElement} el A DOM node
 */
function addRouteExpandable( el ) {
  let routeEl = el;

  if ( !routeEl ) {
    const parent = document.querySelector( '.yes-routes-option-clone' );
    const target = parent.querySelector( '.js-option-wrapper' );
    routeEl = target.cloneNode( true );
    document.querySelector( '.js-initial-routes' ).appendChild( routeEl );
  }

  // Initialize a single expandable up-front.
  const newExpandable = Expandable.init( routeEl );
  expandables = expandables.concat( newExpandable );

  const routeIndex = expandables.length - 1;
  const expandable = expandables[expandables.length - 1];
  expandableView( expandable.element, {
    expandable,
    index: routeIndex
  } ).init();

  store.dispatch( addRouteOptionAction( createRoute() ) );

  const routeOptionsEl = expandable.element.querySelector( `.${ OPTION_CLASSES.FORM }` );
  const routeOptionForm = routeOptionFormView( routeOptionsEl, {
    store,
    routeIndex,
    routeDetailsView,
    averageCostView,
    daysPerWeekView,
    drivingCostEstimateView,
    milesView,
    transitTimeView
  } );
  routeOptionForm.init();
}

addRouteExpandable(
  document.querySelector( '.js-route-option-1' )
);

addRouteOptionView(
  document.querySelector( `.${ OPTION_TOGGLE_CLASSES.BUTTON }` ), {
    onAddExpandable: addRouteExpandable
  }
).init();

/**
 * Only initialize the first route option form, the second is initialized when
 * the user clicks the 'add another option' button.
*/
routeOptionForms[0].init();

// Initialize subviews for the review section
function handleShowReviewPlan() {
  reviewGoalsView(
    document.querySelector( `.${ REVIEW_GOALS_CLASSES.CONTAINER }`
    ), { store }
  ).init();

  const reviewDetailsEl = document.querySelector(
    `.${ reviewDetailsView.CLASSES.CONTAINER }`
  );
  reviewDetailsView( reviewDetailsEl, {
    store, routeDetailsView
  } ).init();

  printButton(
    document.querySelector( `.${ printButton.CLASSES.BUTTON }` )
  ).init();
}

reviewChoiceView(
  document.querySelector( `.${ reviewChoiceView.CLASSES.CONTAINER }` ),
  { store, onShowReviewPlan: handleShowReviewPlan }
).init();

/* remove the second expandable so we can properly initialize it when
   the add additional route button is clicked. This will still preserve
   the second route option when JS is unavailable */
const routesEl = document.querySelector( '.js-initial-routes' );

routesEl.removeChild(
  routesEl.querySelector( '.js-option-wrapper-2' )
);
