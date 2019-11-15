// This file controls the college costs application

import studentDebtCalculator from 'student-debt-calc';
import { schoolModel } from './models/school-model.js';
import { financialModel } from './models/financial-model.js';
import { expensesModel } from './models/expenses-model.js';
import { stateModel } from './models/state-model.js';

import { navigationView } from './views/navigation-view.js';
import { financialView } from './views/financial-view.js';
import { schoolView } from './views/school-view.js';


/* init() - Initialize the app */

const init = function() {
  const body = document.querySelector( 'body' );
  stateModel.init();
  schoolView.init( body );
  financialView.init( body );
  navigationView.init( body );

  financialModel.init();

  financialView.updateFinancialItems();

  console.log( financialModel.values );

  /* Get stuff started
     navigationView.activateGetStartedBtn();
     navigationView._handleGetStartedBtnClick(); */

};


window.addEventListener( 'load', init );

