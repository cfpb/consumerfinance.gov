import 'core-js/features/promise';
import 'core-js/features/object';
import 'core-js/features/dom-collections';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import { appView } from './views/app-view.js';
import { chartView } from './views/chart-view.js';
import { constantsModel } from './models/constants-model.js';
import { expensesModel } from './models/expenses-model.js';
import { expensesView } from './views/expenses-view.js';
import { financialModel } from './models/financial-model.js';
import { financialView } from './views/financial-view.js';
import { getQueryVariables } from './util/url-parameter-utils.js';
import { navigationView } from './views/navigation-view.js';
import { schoolView } from './views/school-view.js';
import { stateModel } from './models/state-model.js';
import { updateModelsFromQueryString } from './dispatchers/update-models.js';
import { updateState } from './dispatchers/update-state.js';


/**
 * Initialize the app
 */
function init() {
  const body = document.querySelector( 'body' );
  const query = getQueryVariables();

  expensesModel.init( body );
  constantsModel.init();
  expensesView.init();
  financialModel.init();
  schoolView.init( body );
  financialView.init();
  navigationView.init( body, query.iped );
  chartView.init( body );
  appView.init();
  Expandable.init();

  financialView.updateFinancialItems();
  appView.updateUI();

  updateModelsFromQueryString( query );
}

window.addEventListener( 'load', init );
