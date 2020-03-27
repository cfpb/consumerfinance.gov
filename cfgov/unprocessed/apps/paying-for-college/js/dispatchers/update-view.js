import { chartView } from '../views/chart-view.js';
import { expensesView } from '../views/expenses-view.js';
import { financialView } from '../views/financial-view.js';

const updateExpensesView = () => {
  expensesView.updateExpensesView();
}

const updateFinancialView = () => {
  financialView.updateFinancialItems();
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

export {
  updateExpensesView,
  updateFinancialView,
  updateCostOfBorrowingChart,
  updateMakePlanChart,
  updateMaxDebtChart,
  updateAffordingChart,
  updateGradMeterChart,
  updateRepaymentMeterChart
};
