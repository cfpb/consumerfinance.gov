/**
 * Update the values of models
 */
import { expensesModel } from '../models/expenses-model.js';
import { expensesView } from '../views/expenses-view.js';
import { financialModel } from '../models/financial-model.js';
import { financialView } from '../views/financial-view.js';
import { getStateByCode } from '../util/other-utils.js';
import { getSchoolData } from '../dispatchers/get-api-values.js';
import {
  updateFinancialViewAndFinancialCharts,
  updateSchoolView,
} from '../dispatchers/update-view.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';
import { convertStringToNumber } from '../../../../../js/modules/util/format.js';
import { isNumeric } from '../util/number-utils.js';
import {
  getProgramInfo,
  getSchoolValue,
  getStateValue,
} from '../dispatchers/get-model-values.js';
import { urlParameters } from '../util/url-parameter-utils.js';
import { updateState } from '../dispatchers/update-state.js';

/**
 * initializeExpenseValues - Create financial model values based on the input
 * fields that exist in the DOM
 */
function initializeExpenseValues() {
  const expenseItems = document.querySelectorAll('[data-expenses-item]');
  expenseItems.forEach((elem) => {
    expensesModel.setValue(elem.dataset.expensesItem, 0, false);
  });
}

/**
 * initializeFinancialValues - Create financial model values based on the input
 * fields that exist in the DOM
 */
function initializeFinancialValues() {
  const financialItems = document.querySelectorAll('[data-financial-item]');
  financialItems.forEach((elem) => {
    financialModel.createFinancialProperty(elem.dataset.financialItem, 0);
  });
}

/**
 * updateFinancial - Update a property of the financial model
 * @param {string} name - The name of the property to update
 * @param {*} value - The new value of the property
 * @param {boolean} updateView - (defaults true) should view be updated?
 */
function updateFinancial(name, value, updateView) {
  financialModel.setValue(name, value, updateView);
}

/**
 * createFinancial - Create a new financial property
 * @param {string} name - The name of the property to update
 * @param {*} value - The new value of the property
 */
function createFinancial(name, value) {
  financialModel.createFinancialProperty(name, value);
}

/**
 * recalculateFinancials - Run the financialModel's internal calculations
 */
function recalculateFinancials() {
  financialModel.recalculate();
}

/**
 * updateExpense - Update a property of the expense model
 * @param {string} name - The name of the property to update
 * @param {*} value - The new value of the property
 */
function updateExpense(name, value) {
  expensesModel.setValue(name, value);
}

/**
 * recalculateExpenses - Run the expenseModel's internal calculations
 */
function recalculateExpenses() {
  expensesModel.calculateTotals();
}

/**
 * updateRegion - Update the region of the expenses model
 * @param {string} region - A two-character string of the new region
 */
function updateRegion(region) {
  expensesModel.setValuesByRegion(region);
}

/**
 * refreshExpenses - Update the expenses with stored values
 */
function refreshExpenses() {
  expensesModel.setValuesByRegion(schoolModel.values.region);
}

/**
 * Clears the financial model costs.
 */
function clearFinancialCosts() {
  financialModel.clearCosts();
}

/**
 * getTopThreePrograms - Update the expenses with stored values
 * @param {string} programs - list of top programs (programsPopular)
 * @returns {string} - top three programs
 */
function getTopThreePrograms(programs) {
  const topThree = '';
  if (programs !== null) {
    const topThreeArr = programs.slice(0, 3);
    schoolModel.values.programsTopThree = topThreeArr.join(', ');
  }
  return topThree;
}

/**
 * @param {object} data - Data from school API
 */
function setSchoolValues(data) {
  for (const key in data) {
    const val = data[key];
    schoolModel.setValue(key, val, false);

    // Update state to reflect any missing rate values
    if (
      ['repay3yr', 'gradRate', 'defaultRate'].indexOf(key) > -1 &&
      !isNumeric(val)
    ) {
      stateModel.setValue(key + 'missing', true);
    }
  }
}

/**
 * updateSchoolData - Fetch API data for school and update the model
 * @param {string} iped - The id of the school
 * @param {boolean} assumptions - if true, make assumptions about data and loans
 * @returns {object} Promise of the XHR request
 */
function updateSchoolData(iped, assumptions) {
  stateModel.setValue('schoolID', iped);
  return getSchoolData(iped)
    .then((resp) => {
      const data = JSON.parse(resp.responseText);
      setSchoolValues(data);
      const pid = getStateValue('pid');

      // Create objects of programs keyed by program ID
      schoolModel.createProgramLists();
      const programInfo = getProgramInfo(pid);

      // If we have a pid, validate it has info
      if (!programInfo) {
        stateModel.setValue('pid', false);
      }

      // Check for investigation
      if (schoolModel.values.underInvestigation === true) {
        stateModel.setValue('investigation', 'yes');
      } else {
        stateModel.setValue('investigation', 'no');
      }

      // Rename the net price averages
      if (data.netPriceAvgSlices) {
        const slices = ['0_30k', '30k_48k', '48k_75k', '75k_110k', '110k_plus'];
        slices.forEach((income) => {
          // We replace the underscore with a dash
          schoolModel.values['netPrice_' + income.replace('_', '-')] =
            data.netPriceAvgSlices[income];
        });
      }

      // Take only the top 3 programs
      schoolModel.values.programsTopThree = getTopThreePrograms(
        schoolModel.values.programsPopular,
      );

      // add the full state name to the schoolModel
      schoolModel.values.stateName = getStateByCode(schoolModel.values.state);

      // Some values must migrate to the financial model
      if (programInfo) {
        financialModel.setValue(
          'salary_annual',
          convertStringToNumber(programInfo.salary),
        );
        stateModel.setValue('programName', programInfo.name);
      } else {
        financialModel.setValue(
          'salary_annual',
          convertStringToNumber(getSchoolValue('medianAnnualPay6Yr')),
        );
      }

      // Update expenses by region
      if ({}.hasOwnProperty.call(schoolModel.values, 'region')) {
        document.querySelector('#expenses__region').value =
          schoolModel.values.region;
        updateRegion(schoolModel.values.region);
      }

      // Make assumptions for initial data
      if (assumptions === true) {
        updateState.byProperty('costsQuestion', 'y');
        updateFinancialsFromSchool();
      }

      updateSchoolView();
    })
    .catch(function (error) {
      iped = iped.replace(/\D/g, '');
      console.log(
        'An error occurred when accessing school data for ' + iped,
        error,
      );
    });
}

/**
 * updateFinancialsFromSchool - Copies useful values from the schoolModel to the financialModel
 */
function updateFinancialsFromSchool() {
  financialModel.updateModelFromSchoolModel();
  financialView.updateFinancialItems();
}

/**
 * parseQueryParameters - put query values into models
 * @param {object} queryObj - an Object containing query key/value pairs
 */
function parseQueryParameters(queryObj) {
  const modelMatch = {
    expensesModel: expensesModel.bulkSetValue,
    financialModel: financialModel.bulkSetValue,
    schoolModel: schoolModel.bulkSetValue,
    stateModel: stateModel.bulkSetValue,
  };

  const modelArrays = {
    expensesModel: [],
    financialModel: [],
    schoolModel: [],
    stateModel: [],
  };

  Object.keys(queryObj).forEach((key) => {
    const match = urlParameters[key].split('.');
    modelArrays[match[0]].push([match[1], queryObj[key]]);

    if (key === 'plus') {
      modelArrays.financialModel.push([
        'plusLoan_gradPlus',
        convertStringToNumber(queryObj[key]),
      ]);
    }
  });

  // Copy programLength into the financial model
  modelArrays.financialModel.push([
    'other_programLength',
    convertStringToNumber(queryObj.lenp),
  ]);

  Object.keys(modelMatch).forEach((key) => {
    modelMatch[key](modelArrays[key]);
  });

  stateModel._setProgramLevel();
  stateModel._setSalaryAvailable();
  stateModel._checkRequiredFields();
  recalculateFinancials();
  updateFinancialViewAndFinancialCharts();
  expensesView.updateExpensesView();
}

/**
 * updateModelsFromQueryString - Translate query values into model values
 * @param {object} queryObj - An object representing the url query string.
 */
function updateModelsFromQueryString(queryObj) {
  // If there's an offerID, set cobs to 'o' (offer)
  if ({}.hasOwnProperty.call(queryObj, 'oid')) {
    queryObj.cobs = 'o';
  }

  // If we have no cobs, check if there are costs values
  if (!{}.hasOwnProperty.call(queryObj, 'cobs')) {
    const costKeys = ['tuit', 'hous', 'diro', 'book', 'indo', 'nda', 'tran'];
    let costsFound = false;
    costKeys.forEach((key) => {
      if ({}.hasOwnProperty.call(queryObj, key)) {
        costsFound = true;
      }
    });

    if (costsFound) {
      queryObj.cobs = 'y';
    }
  }

  parseQueryParameters(queryObj);

  if ({}.hasOwnProperty.call(queryObj, 'iped')) {
    updateSchoolData(queryObj.iped, true);
  }
}

export {
  clearFinancialCosts,
  createFinancial,
  initializeExpenseValues,
  initializeFinancialValues,
  recalculateExpenses,
  recalculateFinancials,
  refreshExpenses,
  updateExpense,
  updateFinancial,
  updateFinancialsFromSchool,
  updateModelsFromQueryString,
  updateRegion,
  updateSchoolData,
};
