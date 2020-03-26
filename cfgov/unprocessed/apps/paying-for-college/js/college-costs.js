// This file controls the college costs application

import { schoolModel } from './models/school-model.js';
import { constantsModel } from './models/constants-model.js';
import { financialModel } from './models/financial-model.js';
import { expensesModel } from './models/expenses-model.js';
import { stateModel } from './models/state-model.js';

import { navigationView } from './views/navigation-view.js';
import { financialView } from './views/financial-view.js';
import { schoolView } from './views/school-view.js';
import { chartView } from './views/chart-view.js';
import { fixedSticky } from './views/fixed-sticky-view.js';

import { updateState } from './dispatchers/update-state.js';
import { updateSchoolData } from './dispatchers/update-models.js';
import Expandable from '../../../../../node_modules/@cfpb/cfpb-expandables/src/Expandable.js';

/* init() - Initialize the app */

const _demoData = function() {
  navigationView._handleGetStartedBtnClick();
  // updateState.activeSection( 'make-a-plan' );

  document.querySelector( '#search__school-input' ).value = 'Example University';
  document.querySelector( 'label[for="program-type-radio_bachelors"]' ).click();
  document.querySelector( 'label[for="program-length-radio_4"]' ).click();
  document.querySelector( 'label[for="program-rate-radio_in-state"]' ).click();
  document.querySelector( 'label[for="program-housing-radio_on-campus"]' ).click();

  updateSchoolData( '999999' );
  schoolView._schoolInfo.classList.add( 'active' );

  financialModel.setValue( 'dirCost_tuition', 10892 );
  financialModel.setValue( 'dirCost_housing', 9384 );
  financialModel.setValue( 'indiCost_books', 1200 );
  financialModel.setValue( 'indiCost_other', 4420 );

  financialModel.setValue( 'grant_school', 4000 );
  financialModel.setValue( 'grant_pell', 5070 );

  financialModel.setValue( 'fedLoan_directSub', 3500 );

  financialModel.setValue( 'fedLoan_directUnsub', 2000 );
  financialModel.setValue( 'savings_family', 827 );

  // "Step two"
  financialModel.setValue( 'instiLoan_institutional', 2500 );
  financialModel.setValue( 'rate_institutionalLoan', 0.0858 );
  financialModel.setValue( 'income_job', 2999 );
  financialModel.setValue( 'other_programLength', 4 );

  financialModel.setValue( 'salary_annual', 51000 );
  financialModel.setValue( 'salary_monthly', 4130 );
  expensesModel.setValue( 'total_expenses', 4230 );

  console.log( 'val', expensesModel.values );

  financialView.updateFinancialItems();

  chartView.updateCostOfBorrowingChart();
  chartView.updateMakePlanChart();
  chartView.updateMaxDebtChart();
  chartView.updateAffordingChart();

  console.log( financialModel.values );
  console.log( stateModel.programData );
  console.log( schoolModel );
};

const init = function() {
  const body = document.querySelector( 'body' );
  stateModel.init();
  constantsModel.init();
  schoolView.init( body );
  financialView.init( body );
  navigationView.init( body );
  chartView.init( body );
  Expandable.init();

  financialModel.init();

  financialView.updateFinancialItems();

  fixedSticky.init( '.costs-not-covered' );

  // For testing purposes:
  // _demoData();

};

window.addEventListener( 'load', init );

