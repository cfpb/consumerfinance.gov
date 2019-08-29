import { combineReducers } from './util';
import budgetReducer from './reducers/budget-reducer';
import routeOptionReducer from './reducers/route-option-reducer';
import YesStore from './yes-store';

/**
 * Function to create a new store instance
 * @returns {YesStore} an instance of the YesStore class
 */
function configureStore() {
  return new YesStore(
    combineReducers( {
      budget: budgetReducer,
      route: routeOptionReducer
    } )
  );
}

const appStore = configureStore();

// Export configure store to expose non-singleton for testing
export { configureStore };

export default appStore;
