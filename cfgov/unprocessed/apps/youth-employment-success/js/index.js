import { combineReducers } from './util';
import budgetFormView from './budget-form-view';
import budgetReducer from './reducers/budget-reducer';
import Expandable from 'cf-expandables/src/Expandable';
import routeOptionFormView from './route-option-view';
import YesStore from './yes-store';

const appStore = new YesStore(
  combineReducers( {
    budget: budgetReducer
  } )
);

const BUDGET_CLASSES = budgetFormView.CLASSES;
const OPTION_CLASSES = routeOptionFormView.CLASSES;

const budgetFormEl = document.querySelector( `.${ BUDGET_CLASSES.FORM }` );
const budgetForm = budgetFormView( budgetFormEl );

const routeOptionsEl = document.querySelector( `.${ OPTION_CLASSES.FORM }` );
const routeOptionsForm = routeOptionFormView( routeOptionsEl );

budgetForm.init();
const expandables = Expandable.init();
routeOptionsForm.init();

expandables.reverse().forEach( expandable => {
  expandable.element.querySelector( '.o-expandable_target' ).click();

  /* why doesn't this work properly?
     expandable.toggleTargetState(
     expandable.element.querySelector('.o-expandable_target')
     )
     expandable.toggleTargetState(
     expandable.element.querySelector('.o-expandable_content')
     ) */
} );

window.onbeforeunload = () => {
  budgetForm.destroy();
};
