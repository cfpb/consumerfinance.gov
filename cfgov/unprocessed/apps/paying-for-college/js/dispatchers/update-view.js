import { financialView } from '../views/financial-view.js';
import { chartView } from '../views/chart-view.js';

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
  updateFinancialView,
  updateCostOfBorrowingChart,
  updateMakePlanChart,
  updateMaxDebtChart,
  updateAffordingChart,
  updateGradMeterChart,
  updateRepaymentMeterChart
};
