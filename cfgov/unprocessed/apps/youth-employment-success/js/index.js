import Expandable from 'cf-expandables/src/Expandable';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import budgetFormView from './budget-form-view';
import createRoute from './route.js';
import routeOptionFormView from './route-option-view';
import routeOptionToggleView from './route-option-toggle-view';
import store from './store';

Array.prototype.slice.call(
  document.querySelectorAll( 'input' )
).forEach( input => {
  input.removeAttribute( 'disabled' );
} );

const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;
const OPTION_TOGGLE_CLASSES = routeOptionToggleView.CLASSES;

const budgetFormEl = document.querySelector( `.${ BUDGET_CLASSES.FORM }` );
const budgetForm = budgetFormView( budgetFormEl, { store } );
budgetForm.init();

const expandables = Expandable.init();
const routeOptionForms = expandables.map( ( expandable, index ) => {
  store.dispatch( addRouteOptionAction( createRoute() ) );

  const routeOptionsEl = expandable.element.querySelector( `.${ OPTION_CLASSES.FORM }` );
  return routeOptionFormView( routeOptionsEl, { store, routeIndex: index } );
} );

/* only initialize the first form, the other gets initialized when
  the user clicks 'add another option' button */
routeOptionForms[0].init();
routeOptionToggleView(
  document.querySelector( `.${ OPTION_TOGGLE_CLASSES.BUTTON }` ), {
    expandable: expandables[1],
    routeOptionForm: routeOptionForms[1]
  }
).init();

expandables[0].element.querySelector( '.o-expandable_target' ).click();
// target the last element, reverse is destructive
expandables[1].element.classList.add( 'u-hidden' );

window.onbeforeunload = () => {
  budgetForm.destroy();
};
