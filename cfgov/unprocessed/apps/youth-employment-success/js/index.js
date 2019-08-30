import Expandable from 'cf-expandables/src/Expandable';
import { addRouteOptionAction } from './reducers/route-option-reducer';
import budgetFormView from './budget-form-view';
import createRoute from './route.js';
import routeOptionFormView from './route-option-view';
import store from './store';


const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;

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
   the user clicks the add another option button */
routeOptionForms[0].init();

expandables[0].element.querySelector( '.o-expandable_target' ).click();
// target the last element, reverse is destructive
expandables[1].element.classList.add( 'u-hidden' );

window.onbeforeunload = () => {
  budgetForm.destroy();
};
