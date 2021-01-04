import { appView } from '../views/app-view.js';
import { chartView } from '../views/chart-view.js';
import { expensesView } from '../views/expenses-view.js';
import { financialView } from '../views/financial-view.js';
import { navigationView } from '../views/navigation-view.js';
import { schoolView } from '../views/school-view.js';

/**
 * This file is a dispatcher to call various methods of the view Objects.
 */

/**
 * updateAppView - updates the AppView
 */
const updateAppView = () => {
  appView.updateView();
};

/**
 * Update the URL query string to contain app/financial information
 */
const updateUrlQueryString = () => {
  appView.setUrlQueryString();
};

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

/**
 * updateStateInDom - manages dataset for the MAIN element, which helps display UI elements
 * properly
 * @param {String} prop - The state property to modify
 * @param {String} value - The new value of the property
 * NOTE: if the value is null or the Boolean 'false', the data attribute will be removed
 */
const updateStateInDom = ( prop, value ) => {
  navigationView.updateStateInDom( prop, value );
};

const updateCostOfBorrowingChart = () => {
  chartView.updateCostOfBorrowingChart();
};

const updateMakePlanChart = () => {
  chartView.updateMakePlanChart();
};

const updateMaxDebtChart = () => {
  chartView.updateMaxDebtChart();
};

const updateAffordingChart = () => {
  chartView.updateAffordingChart();
};

const updateGradMeterChart = () => {
  chartView.updateGradMeterChart();
};

const updateRepaymentMeterChart = () => {
  chartView.updateRepaymentMeterChart();
};

const updateFinancialViewAndFinancialCharts = () => {
  updateFinancialView();
  updateCostOfBorrowingChart();
  updateMakePlanChart();
  updateMaxDebtChart();
  updateAffordingChart();
};

const updateSchoolFormWithErrors = () => {
  schoolView.updateViewWithErrors();
};

export {
  updateAppView,
  updateExpensesView,
  updateFinancialView,
  updateNavigationView,
  updateSchoolItems,
  updateSchoolView,
  updateStateInDom,
  updateCostOfBorrowingChart,
  updateFinancialViewAndFinancialCharts,
  updateMakePlanChart,
  updateMaxDebtChart,
  updateAffordingChart,
  updateGradMeterChart,
  updateRepaymentMeterChart,
  updateUrlQueryString
};
