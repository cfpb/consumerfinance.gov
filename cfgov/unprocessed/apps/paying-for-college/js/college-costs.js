// This file controls the college costs application

import studentDebtCalculator from 'student-debt-calc';
import { schoolModel } from './models/school-model.js';
import { debtModel } from './models/debt-model.js';
import { expensesModel } from './models/expenses-model.js';

import { financialView } from './views/financial-view.js';
import { searchView } from './views/search-view.js';


/* init() - Initialize the app */

const init = function() {
  const body = document.querySelector( 'body' );
  searchView.init( body );
};


window.addEventListener( 'load', init );
