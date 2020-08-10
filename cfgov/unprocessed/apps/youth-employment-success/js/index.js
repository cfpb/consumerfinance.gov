import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import {
  averageCostView,
  daysPerWeekView,
  drivingCostEstimateView,
  milesView,
  transitTimeView
} from './views/route/form-questions';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import { toArray } from './util';
import budgetFormView from './views/budget';
import createRoute from './models/route';
import expandableView from './views/expandable';
import goalsView from './views/goals';
import printButton from './views/print-button';
import reviewChoiceView from './views/review/choice';
import reviewDetailsView from './views/review/details';
import reviewGoalsView from './views/review/goals';
import routeDetailsView from './views/route/details';
import routeOptionFormView from './views/route/option-form';
import routeOptionToggleView from './views/route/option-toggle';
import store from './store';


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
