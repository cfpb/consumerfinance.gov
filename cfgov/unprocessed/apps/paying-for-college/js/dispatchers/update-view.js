import { chartView } from '../views/chart-view.js';
import { expensesView } from '../views/expenses-view.js';
import { financialView } from '../views/financial-view.js';
import { navigationView } from '../views/navigation-view.js';
import { schoolView } from '../views/school-view.js';

/**
 * This file is a dispatcher to call various methods of the view Objects. 
 */

/**
 * updateExpensesView - updates the expensesView 
 */
const updateExpensesView = () => {
  expensesView.updateExpensesView();
};

/**
 * updateFinancialView - updates the financialView 
 */
const updateFinancialView = () => {
  financialView.updateFinancialItems();
};

/**
 * updateNavigationView - updates the navigationView 
 */
const updateNavigationView = () => {
  navigationView.updateView();
};

/**
 * updateSchoolView - updates the schoolView 
 */
const updateSchoolView = () => {
  schoolView.updateSchoolView();
};

/**
 * updateSchoolItems - updates the data-school-item elements 
 */
const updateSchoolItems = () => {
  schoolView.updateSchoolItems();
};

export {
  updateExpensesView,
  updateFinancialView,
  updateNavigationView,
  updateSchoolItems,
  updateSchoolView
};
