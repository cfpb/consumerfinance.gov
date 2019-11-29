import { financialView } from '../views/financial-view.js';

const updateFinancialView = function() {
  financialView.updateFinancialItems();
};

export {
  updateFinancialView
};
