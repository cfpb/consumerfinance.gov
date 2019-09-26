import Expandable from 'cf-expandables/src/Expandable';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import budgetFormView from './budget-form-view';
import createRoute from './route.js';
import averageCostView from './views/average-cost';
import daysPerWeekView from './views/days-per-week';
import milesView from './views/miles';
import goalsView from './views/goals';
import reviewGoalsView from './views/review/goals';
import routeOptionFormView from './route-option-view';
import routeOptionToggleView from './route-option-toggle-view';
import routeDetailsView from './views/route-details';
import expandableView from './views/expandable';
import store from './store';
import transitTimeView from './views/transit-time';

Array.prototype.slice.call(
  document.querySelectorAll( 'input' )
).forEach( input => {
  input.removeAttribute( 'disabled' );
} );

const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;
const OPTION_TOGGLE_CLASSES = routeOptionToggleView.CLASSES;
const DETAILS_CLASSES = routeDetailsView.CLASSES;
const GOALS_CLASSES = goalsView.CLASSES;
const REVIEW_GOALS_CLASSES = reviewGoalsView.CLASSES;

const goalsViewEl = document.querySelector( ` .${ GOALS_CLASSES.CONTAINER }` );
const goalsFormView = goalsView( goalsViewEl, { store } );
goalsFormView.init();

const budgetFormEl = document.querySelector( `.${ BUDGET_CLASSES.FORM }` );
const budgetForm = budgetFormView( budgetFormEl, { store } );
budgetForm.init();

reviewGoalsView( document.querySelector( `.${ REVIEW_GOALS_CLASSES.CONTAINER }` ), { store } ).init();

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
    detailsView: routeDetailsView( document.querySelector( `.${ DETAILS_CLASSES.CONTAINER }` ) ),
    averageCostView,
    daysPerWeekView,
    milesView,
    transitTimeView
  } );
} );

/**
 * Only initialize the first route option form, the second is initialized when
 * the user clicks the 'add another option' button.
*/
routeOptionForms[0].init();
routeOptionToggleView(
  document.querySelector( `.${ OPTION_TOGGLE_CLASSES.BUTTON }` ), {
    expandable: expandables[1],
    routeOptionForm: routeOptionForms[1]
  }
).init();

expandables[0].element.querySelector( '.o-expandable_target' ).click();
expandables[1].element.classList.add( 'u-hidden' );
