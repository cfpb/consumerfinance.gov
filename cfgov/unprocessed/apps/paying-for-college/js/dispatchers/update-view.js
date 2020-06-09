import { chartView } from '../views/chart-view.js';
import { expensesView } from '../views/expenses-view.js';
import { financialView } from '../views/financial-view.js';
import { navigationView } from '../views/navigation-view.js';
import { schoolView } from '../views/school-view.js';

const updateExpensesView = () => {
  expensesView.updateExpensesView();
};

const updateFinancialView = () => {
  financialView.updateFinancialItems();
};

const updateNavigationView = () => {
  navigationView.updateView();
};

const updateSchoolView = () => {
  schoolView.updateSchoolView();
};

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
