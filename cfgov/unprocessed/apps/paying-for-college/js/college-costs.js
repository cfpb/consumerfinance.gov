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
import { updateModelsFromQueryString } from './dispatchers/update-models.js';


/**
 * Initialize the app
 */
const init = function() {
  const body = document.querySelector( 'body' );
  const query = getQueryVariables();
  constantsModel.init();
  expensesModel.init();
  financialModel.init();

  schoolView.init( body );
  expensesView.init( body );
  financialView.init();
  navigationView.init( body, query.iped );
  chartView.init( body );
  appView.init();
  Expandable.init();

  updateModelsFromQueryString( query );

  financialView.updateFinancialItems();
  appView.updateUI();
};

window.addEventListener( 'load', init );
