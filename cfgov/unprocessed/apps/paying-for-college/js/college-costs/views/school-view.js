/* schoolView specifically covers the school search and associated fields, such as
   program length and living situation. */
import {
  getProgramList,
  getSchoolValue,
  getStateValue,
} from '../dispatchers/get-model-values.js';
import {
  clearFinancialCosts,
  refreshExpenses,
  updateFinancial,
  updateSchoolData,
  updateFinancialsFromSchool,
} from '../dispatchers/update-models.js';
import {
  updateFinancialView,
  updateGradMeterChart,
  updateRepaymentMeterChart,
} from '../dispatchers/update-view.js';
import { decimalToPercentString } from '../util/number-utils.js';
import {
  formatUSD,
  convertStringToNumber,
} from '../../../../../js/modules/util/format.js';
import { schoolSearch } from '../dispatchers/get-api-values.js';
import { updateState } from '../dispatchers/update-state.js';

const schoolView = {
  _searchSection: null,
  _searchBox: null,
  _searchResults: null,
  _programRadioLabels: null,
  _programRadioInputs: null,
  _schoolInfo: null,
  _schoolItems: [],
  _stateItems: [],
  _programSelect: null,
  _programIncome: null,

  updateSchoolView: () => {
    updateFinancialView();
    updateGradMeterChart();
    updateRepaymentMeterChart();
    schoolView._updateSchoolRadioButtons();
    schoolView._updateSchoolName();
    schoolView.updateSchoolItems();
    schoolView._updateProgramList();
    schoolView._programIncome.value = getStateValue('programIncome');
    document.querySelectorAll('.scorecard-school').forEach((elem) => {
      elem.setAttribute(
        'href',
        'https://collegescorecard.ed.gov/school/?' + getSchoolValue('schoolID'),
      );
    });
  },

  updateSchoolItems: function () {
    this._schoolItems.forEach((elem) => {
      const prop = elem.dataset.schoolItem;
      let val = getSchoolValue(prop);
      // Prevent improper values from being displayed on the page
      if (typeof val === 'undefined' || val === false || val === null) {
        val = '';
      }

      if (elem.dataset.numberDisplay === 'currency') {
        val = formatUSD({ amount: val });
      }

      if (elem.dataset.numberDisplay === 'percentage') {
        val = decimalToPercentString(val, 0);
      }

      elem.innerText = val;
    });

    this._stateItems.forEach((elem) => {
      const prop = elem.dataset.stateItem;
      let val = getStateValue(prop);
      // Prevent improper values from being displayed on the page
      if (typeof val === 'undefined' || val === false || val === null) {
        val = '';
      }
      elem.innerText = val;
    });
  },

  _updateProgramList: () => {
    if (getSchoolValue('schoolID') === null) return;
    const programType = getStateValue('programType');
    let level = 'undergrad';

    if (programType === 'graduate') {
      level = 'graduate';
    }

    const list = getProgramList(level, programType);

    if (list.length > 0) {
      updateState.byProperty('schoolHasPrograms', 'yes');
    } else {
      updateState.byProperty('schoolHasPrograms', 'no');
    }

    if (list.length > 0) {
      let html = '<option selected="selected" value="null">Select...</option>';
      list.forEach((elem) => {
        html += `
          <option data-program-salary="${elem.salary}" value="${elem.code}">
                ${elem.level} - ${elem.name}
          </option>`;
      });
      html +=
        '\n<option value="null">My program is not listed here/I am undecided.</option>';

      schoolView._programSelect.innerHTML = html;

      // If there's a program id in the state, select that program
      if (getStateValue('pid')) {
        schoolView._programSelect.value = getStateValue('pid');
      }

      schoolView._programIncome.value = getStateValue('programIncome');
      schoolView._programSelect.parentNode.parentNode.style.display = 'block';
    } else {
      schoolView._programSelect.parentNode.parentNode.style.display = 'none';
    }
  },

  _updateSchoolName: () => {
    const school = getSchoolValue('school');

    schoolView._searchResults.classList.remove('active');
    if (school) schoolView._searchBox.value = school;
    schoolView._schoolInfo.classList.add('active');
  },

  _updateSchoolRadioButtons: () => {
    const buttons = [
      'programLength',
      'programType',
      'programHousing',
      'programProgress',
      'programRate',
      'programDependency',
    ];

    buttons.forEach((name) => {
      const val = getStateValue(name);
      if (typeof val !== 'undefined') {
        schoolView.clickRadioButton(name, val);
      }
    });
  },

  clickRadioButton: (name, value) => {
    if (name !== null && value !== false) {
      const input = document.querySelector(
        'INPUT[name="' + name + '"][value="' + value + '"]',
      );
      if (input) input.checked = true;
    }
  },

  init: (body) => {
    // Set up nodeLists
    schoolView._searchSection = body.querySelector(
      '#college-costs_school-search',
    );
    schoolView._searchBox = body.querySelector('#search__school-input');
    schoolView._searchResults = body.querySelector('#search-results');
    schoolView._programRadioLabels = body.querySelectorAll(
      '.school-search__additional-info label',
    );
    schoolView._programRadioInputs = body.querySelectorAll(
      '.school-search__additional-info input[type="radio"]',
    );
    schoolView._programSelect = body.querySelector('#program-select');
    schoolView._schoolInfo = body.querySelector(
      '.school-search__additional-info',
    );
    schoolView._schoolItems = document.querySelectorAll('[data-school-item]');
    schoolView._stateItems = document.querySelectorAll('[data-state-item]');
    schoolView._programIncome = document.querySelector('#program-income');

    // Initialize listeners
    _addListeners();
  },
};

/**
 * Add all event listeners for school search view
 */
function _addListeners() {
  schoolView._searchBox.addEventListener('keyup', _handleInputChange);
  schoolView._searchResults.addEventListener('click', _handleResultButtonClick);

  schoolView._programRadioLabels.forEach((elem) => {
    elem.addEventListener('click', _handleProgramRadioClick);
  });

  schoolView._programRadioInputs.forEach((elem) => {
    elem.addEventListener('change', _handleProgramRadioClick);
  });

  schoolView._programSelect.addEventListener(
    'change',
    _handleProgramSelectChange,
  );

  schoolView._programIncome.addEventListener(
    'change',
    _handleIncomeSelectChange,
  );
}

/**
 * Convert JSON string of school search results into markup.
 * @param {string} responseText - JSON string of school info.
 */
function _formatSearchResults(responseText) {
  const obj = JSON.parse(responseText);
  let html = '<ul>';
  for (const key in obj) {
    const school = obj[key];
    html +=
      '\n<li><button role="button" data-school_id="' +
      school.id +
      '"><strong>' +
      school.schoolname +
      '</strong>';
    html +=
      '<p><em>' + school.city + ', ' + school.state + '</em></p></button></li>';
  }
  html += '</li>';
  schoolView._searchResults.innerHTML = html;
  schoolView._searchResults.classList.add('active');
}

let _keyupDelay;

/**
 * Show search indicator
 */
function startSearching() {
  schoolView._searchBox.parentNode.className = 'searching';
}

/**
 * Hide search indicator
 */
function stopSearching() {
  schoolView._searchBox.parentNode.className = '';
}

/**
 * Text has been entered in the school search input.
 */
function _handleInputChange() {
  startSearching();
  clearTimeout(_keyupDelay);
  _keyupDelay = setTimeout(function () {
    const searchTerm = schoolView._searchBox.value.trim();

    /* TODO - clean up searchbox text, remove non-alphanumeric characters
       Searches of less than 3 characters are prevented in the API fetch, so
       we represent that visually by hiding the search results DIV */
    if (searchTerm.length < 3) {
      schoolView._searchResults.classList.remove('active');
      stopSearching();
    } else {
      schoolSearch(searchTerm).then(
        (resp) => {
          stopSearching();
          _formatSearchResults(resp.responseText);
        },
        (error) => {
          stopSearching();
          console.log(error);
        },
      );
    }
  }, 300);
}

/**
 * The income dropdown has been selected
 */
function _handleIncomeSelectChange() {
  const selected = schoolView._programIncome.value;
  updateState.byProperty('programIncome', selected);
  updateFinancial('netPrice', getSchoolValue('netPrice_' + selected));
}

/**
 * Graduate program selection has changed.
 * @param {Event} event - change event object.
 */
function _handleProgramSelectChange(event) {
  const target = event.target;
  const salary = target.options[target.selectedIndex].dataset.programSalary;
  let programName = target.options[target.selectedIndex].innerText;
  let pid = target.value;
  if (pid === 'null') {
    pid = false;
    programName = '';
  }
  updateState.byProperty('pid', pid);
  updateState.byProperty('programName', programName);
  if (salary) {
    updateFinancial('salary_annual', salary);
  } else {
    updateFinancial(
      'salary_annual',
      convertStringToNumber(getSchoolValue('medianAnnualPay6Yr')),
    );
  }
  refreshExpenses();
}

/**
 * An item in the search results box was clicked.
 * @param {MouseEvent} event - click event object.
 */
function _handleResultButtonClick(event) {
  const target = event.target;
  let button;
  // Find the button in the clickable area
  if (target.tagName === 'BUTTON') {
    button = target;
  } else {
    button = target.closest('BUTTON');
  }

  schoolView._searchResults.classList.remove('active');

  // Clear pid from state
  updateState.byProperty('pid', false);

  // If there's an existing school, clear financials and choice value
  if (getStateValue('schoolID') !== false) {
    clearFinancialCosts();
    updateState.byProperty('costsQuestion', false);
  }

  // If there's a school_id, then proceed with schoolInfo
  if (typeof button.dataset.school_id !== 'undefined') {
    const iped = button.dataset.school_id;
    if (iped !== null && typeof iped !== 'undefined') {
      startSearching();
      // Add schoolData to schoolModel
      updateSchoolData(iped, true).then(() => stopSearching());
    }
  }
}

/**
 * A school program selection radio button was clicked.
 * @param {MouseEvent} event - click event object.
 */
function _handleProgramRadioClick(event) {
  const target = event.target;
  if (target.tagName !== 'INPUT') return;

  // Update the model with program info
  const prop = target.getAttribute('name');
  const value = target.value;
  setTimeout(() => {
    updateState.byProperty(prop, value);
    updateFinancialsFromSchool();
    if (prop === 'programType') {
      schoolView._updateProgramList();
    }
  }, 0);
}

export { schoolView };
