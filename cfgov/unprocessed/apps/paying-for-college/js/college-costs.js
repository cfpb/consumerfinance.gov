// This file controls the college costs application
import Expandable from '../../../../../node_modules/@cfpb/cfpb-expandables/src/Expandable.js';
import { appView } from './views/app-view.js';
import { chartView } from './views/chart-view.js';
import { constantsModel } from './models/constants-model.js';
import { expensesModel } from './models/expenses-model.js';
import { expensesView } from './views/expenses-view.js';
import { financialModel } from './models/financial-model.js';
import { financialView } from './views/financial-view.js';
import { getQueryVariables } from './util/url-parameter-utils.js';
import { navigationView } from './views/navigation-view.js';
import { schoolModel } from './models/school-model.js';
import { schoolView } from './views/school-view.js';
import { stateModel } from './models/state-model.js';
import { updateModelsFromQueryString, updateSchoolData } from './dispatchers/update-models.js';
import { updateState } from './dispatchers/update-state.js';

/**
 * Initialize the app
 */
const init = function() {
  const body = document.querySelector( 'body' );
  constantsModel.init();
  expensesModel.init();
  financialModel.init();

  schoolView.init( body );
  expensesView.init( body );
  financialView.init( body );
  navigationView.init( body );
  chartView.init( body );
  appView.init();
  Expandable.init();

  updateModelsFromQueryString( getQueryVariables() );

  financialView.updateFinancialItems();

};

window.addEventListener( 'load', init );
