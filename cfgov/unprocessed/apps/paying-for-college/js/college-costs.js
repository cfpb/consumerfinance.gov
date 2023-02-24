import Expandable from '@cfpb/cfpb-expandables/src/Expandable.js';
import { appView } from './college-costs/views/app-view.js';
import { chartView } from './college-costs/views/chart-view.js';
import { constantsModel } from './college-costs/models/constants-model.js';
import { expensesModel } from './college-costs/models/expenses-model.js';
import { expensesView } from './college-costs/views/expenses-view.js';
import { financialModel } from './college-costs/models/financial-model.js';
import { financialView } from './college-costs/views/financial-view.js';
import { getQueryVariables } from './college-costs/util/url-parameter-utils.js';
import { navigationView } from './college-costs/views/navigation-view.js';
import { schoolView } from './college-costs/views/school-view.js';
import { updateModelsFromQueryString } from './college-costs/dispatchers/update-models.js';

/**
 * Initialize the app
 */
function init() {
  const body = document.querySelector('body');
  const query = getQueryVariables();

  expensesModel.init(body);
  constantsModel.init();
  expensesView.init();
  financialModel.init();
  schoolView.init(body);
  financialView.init();
  navigationView.init(body, query.iped);
  chartView.init(body);
  appView.init();
  Expandable.init();

  financialView.updateFinancialItems();
  appView.updateUI();

  updateModelsFromQueryString(query);
}

window.addEventListener('load', init);
