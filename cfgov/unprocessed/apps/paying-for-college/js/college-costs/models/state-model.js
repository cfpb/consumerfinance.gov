/**
 * This file contains the model for the application state - that is, an Object
 * which tracks the current app state and allows the views to update based on
 * state.
 */
import { getSchoolValue } from '../dispatchers/get-model-values.js';
import {
  recalculateFinancials,
  updateFinancial,
} from '../dispatchers/update-models.js';
import {
  updateFinancialViewAndFinancialCharts,
  updateNavigationView,
  updateSchoolItems,
  updateStateInDom,
  updateUrlQueryString,
} from '../dispatchers/update-view.js';

/*
// These are currently unused.
const urlVals = [
  'pid',
  'programHousing',
  'programType',
  'programProgress',
  'programLength',
  'programRate',
  'programDependency',
  'costsQuestion',
  'expensesRegion',
  'impactOffer',
  'impactLoans',
  'utmSource',
  'utm_medium',
  'utm_campaign'
];
*/

const stateModel = {
  stateDomElem: null,
  values: {
    activeSection: false,
    constantsLoaded: false,
    hoursToCoverPaymentText: '',
    showSchoolErrors: false,
    schoolSelected: false,
    gotStarted: false,
    gradMeterCohort: 'cohortRankByHighestDegree',
    gradMeterCohortName: 'U.S.',
    programType: 'bachelors',
    programTypeText: "Bachelor's Degree",
    programLength: '4',
    programLengthText: '4 years',
    programLevel: 'undergrad',
    programRate: 'inState',
    programRateText: 'In-state',
    programHousing: 'onCampus',
    programHousingText: 'On campus',
    programDependency: 'dependent',
    programProgress: '0',
    programIncome: 'not-selected',
    repayMeterCohort: 'cohortRankByHighestDegree',
    repayMeterCohortName: 'U.S.',
    schoolID: false,
    initialQuery: null,
    navDestination: null,
    usingNetPrice: 'yes',
  },
  textVersions: {
    programType: {
      certificate: 'certificate',
      associates: "Associates's Degree",
      bachelors: "Bachelor's Degree",
      graduate: "Graduate's Degree",
    },
    programLength: {
      1: '1 year',
      2: '2 years',
      3: '3 years',
      4: '4 years',
      5: '5 years',
      6: '6 years',
    },
    programHousing: {
      onCampus: 'On campus',
      offCampus: 'Off campus (you will pay rent/mortgage)',
      withFamily: 'With family (you will not pay rent/mortgage)',
    },
    programRate: {
      inState: 'In-state',
      outOfState: 'Out of state',
      inDistrict: 'In district',
    },
    programIncome: {
      '0-30k': 'from $0 to $30,000',
      '30k-48k': 'from $30,000 to $48,000',
      '48k-75k': 'from $48,000 to $75,000',
      '75k-110k': 'from $75,000 to $110,000',
      '110k-plus': 'of $110,000 or more',
    },
  },

  /**
   * Check whether required fields are selected
   * @returns {boolean} false if the school form is incomplete, true otherwise
   */
  _checkRequiredFields: function () {
    // Don't check required fields until the
    if (stateModel.showSchoolErrors === false) {
      return false;
    }
    const smv = stateModel.values;
    const control = getSchoolValue('control');
    smv.schoolErrors = 'no';
    updateStateInDom('schoolErrors', 'no');

    const displayErrors = {
      // These are true if the error should be shown, false otherwise
      schoolSelected: getSchoolValue('schoolID') === false,
      programTypeSelected: smv.programType === 'not-selected',
      programLengthSelected: smv.programLength === 'not-selected',
      programProgressSelected: smv.programProgress === 'not-selected',
      rateSelected: smv.programRate === 'not-selected' && control === 'Public',
      housingSelected:
        smv.programLevel === 'undergrad' &&
        smv.programHousing === 'not-selected',
      dependencySelected:
        smv.programLevel === 'undergrad' &&
        smv.programDependency === 'not-selected',
      incomeSelected: smv.programIncome === 'not-selected',
    };

    // Change values to "required" which triggers error notification CSS rules
    for (const key in displayErrors) {
      if (displayErrors[key] === true) {
        stateModel.values[key] = 'required';
        updateStateInDom(key, 'required');
        stateModel.values.schoolErrors = 'yes';
        updateStateInDom('schoolErrors', 'yes');
      } else {
        stateModel.values[key] = false;
        updateStateInDom(key, false);
      }
    }

    if (stateModel.values.schoolErrors === 'no') {
      stateModel.values.showSchoolErrors = false;
      updateStateInDom('showSchoolErrors', false);
    }

    return true;
  },

  /**
   * set the salaryAvailable property based on other values
   */
  _setSalaryAvailable: () => {
    let available = 'yes';
    const smv = stateModel.values;
    if (smv.programLevel === 'graduate' && smv.pid === false) {
      available = 'no';
    }
    stateModel.values.salaryAvailable = available;
    updateStateInDom('salaryAvailable', available);
  },

  /**
   * set programLevel property based on programType
   */
  _setProgramLevel: () => {
    const programType = stateModel.values.programType;
    let programLevel = 'undergrad';
    if (programType === 'graduate') {
      programLevel = 'graduate';
    }

    stateModel.values.programLevel = programLevel;
    updateStateInDom('programLevel', programLevel);
  },

  /**
   * update the application state based on the 'property' parameter.
   * @param {string} property - What property to update based on
   */
  _updateApplicationState: (property) => {
    const urlParams = [
      'pid',
      'programHousing',
      'programType',
      'programProgress',
      'programLength',
      'programRate',
      'programDependency',
      'costsQuestion',
      'expensesRegion',
      'impactOffer',
      'impactLoans',
      'utmSource',
      'utm_medium',
      'utm_campaign',
    ];

    const finUpdate = [
      'programType',
      'programRate',
      'programDependency',
      'programLength',
      'programHousing',
    ];

    // Properties which require a URL querystring update:
    if (urlParams.indexOf(property) > 0) {
      updateUrlQueryString();
    }

    // Properties which require a financialModel and financialView update:
    if (finUpdate.indexOf(property) > 0) {
      recalculateFinancials();
      updateFinancialViewAndFinancialCharts();
    }

    if ({}.hasOwnProperty.call(stateModel.textVersions, property)) {
      const value = stateModel.values[property];
      const key = property + 'Text';
      stateModel.values[key] = stateModel.textVersions[property][value];
      updateSchoolItems();
    }

    // When the meter buttons are clicked, updateSchoolItems
    if (property.indexOf('MeterThird') > 0) {
      updateSchoolItems();
    }

    // Update state values which are based on other values
    stateModel._setProgramLevel();
    stateModel._setSalaryAvailable();
    stateModel._checkRequiredFields();
  },

  /**
   * pushStateToHistory - Push current application state to window.history
   */
  pushStateToHistory: () => {
    const historyState = {
      activeSection: stateModel.values.activeSection,
    };
    window.history.pushState(historyState, null, window.location.search);
  },

  /**
   * replaceStateInHistory - Replace current application state in window.history
   * @param {string} queryString - The queryString to put in the history object
   */
  replaceStateInHistory: (queryString) => {
    const historyState = {
      activeSection: stateModel.values.activeSection,
    };
    if (typeof queryString === 'undefined')
      queryString = window.location.search;
    window.history.replaceState(historyState, null, queryString);
  },

  /**
   * setValue - Public method to update model values
   * @param {string} name - the name of the property to update
   * @param {*} value - the value to be assigned
   */
  setValue: function (name, value) {
    // In case this method gets used to update activeSection...
    if (name === 'activeSection') {
      stateModel.setActiveSection(value);
    } else if (name === 'programLength') {
      updateFinancial('other_programLength', value, true);
    } else if (name === 'programRate') {
      updateFinancial('dirCost_tuition', 'refactor');
    } else if (
      name === 'usingNetPrice' &&
      value !== stateModel.values.usingNetPrice
    ) {
      stateModel.values[name] = value;
      recalculateFinancials();
      updateFinancialViewAndFinancialCharts();
    }
    stateModel.values[name] = value;
    updateStateInDom(name, value);

    stateModel._updateApplicationState(name);
  },

  /**
   * bulkSetValue - Used to set a value
   * @param {Array} tuples - values to update
   */
  bulkSetValue: (tuples) => {
    tuples.forEach((v) => {
      const name = v[0];
      const value = v[1];

      if (name === 'activeSection') {
        stateModel.setActiveSection(value);
      }

      stateModel.values[name] = value;

      if ({}.hasOwnProperty.call(stateModel.textVersions, name)) {
        const key = name + 'Text';
        stateModel.values[key] = stateModel.textVersions[name][value];
      }

      updateStateInDom(name, value);
    });
  },

  /**
   * setActiveSection - Method to update the app's active section
   * @param {*} value - the value to be assigned
   * @param {boolean} popState - true if the update is the result of a popState event
   */
  setActiveSection: function (value, popState) {
    updateStateInDom('activeSection', value);
    stateModel.setValue('save-for-later', false);
    stateModel.values.activeSection = value;
    if (popState !== true) {
      stateModel.pushStateToHistory();
    }
    updateNavigationView();
  },

  /**
   * useNetPrice - Uses various state items to determine whether netPrice should
   * be used by the financial-model in calculations.
   * @returns {boolean} True if using netPrice, false otherwise.
   */
  useNetPrice: function () {
    const earlyPages = [
      'school-info',
      'school-costs',
      'estimate-debt',
      'debt-at-grad',
    ];
    const vals = stateModel.values;
    // If we are before the customize page, always use netPrice
    const section =
      vals.navDestination !== null ? vals.navDestination : vals.activeSection;
    if (earlyPages.indexOf(section) > -1) {
      return true;
      // If the user already set the value to "yes" or we're on the customize estimate page, don't use netPrice.
    } else if (
      vals.usingNetPrice === 'no' ||
      section === 'customize-estimate'
    ) {
      return false;
    }
    // Assume "yes" otherwise
    return true;
  },
};

export { stateModel };
