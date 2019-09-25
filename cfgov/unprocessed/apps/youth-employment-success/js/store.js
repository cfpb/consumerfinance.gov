import YesStore from './yes-store';
import budgetReducer from './reducers/budget-reducer';
import { combineReducers } from './util';
import goalReducer from './reducers/goal-reducer';
import routeOptionReducer from './reducers/route-option-reducer';

/**
 * Function to create a new store instance
 * @returns {YesStore} an instance of the YesStore class
 */
function configureStore() {
  return new YesStore(
    combineReducers( {
      budget: budgetReducer,
      goals: goalReducer,
      routes: routeOptionReducer
    } )
  );
}

const appStore = configureStore();

// Export configure store to expose non-singleton for testing
export { configureStore };

export default appStore;
