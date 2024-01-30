import {
  changeElText,
  changeElHTML,
  addClass,
  removeClass,
} from './dom-tools.js';
import { reset } from './count.js';

const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

/**
 * Hide the data sections. These get shown as needed in addresses.js (render)
 */
function _hideData() {
  addClass('#rural', 'u-hidden');
  addClass('#notRural', 'u-hidden');
  addClass('#duplicate', 'u-hidden');
  addClass('#notFound', 'u-hidden');
}

/**
 * Setup the main UI.
 */
function setup() {
  // set year
  const yearValue = document.querySelector('#year').value;

  changeElText('.chosenYear', yearValue);
  changeElText('.chosenYear1', yearValue + 1);
  changeElText('.chosenYear2', yearValue + 2);

  // set report generated date
  const date = new Date();
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear();

  changeElText(
    '.report-date',
    'Report generated ' + monthNames[monthIndex] + ' ' + day + ', ' + year,
  );

  addClass('#file-error', 'u-hidden');
  addClass('#error-message', 'u-hidden');
  removeClass('#spinner', 'u-hidden');

  reset();
  _resetHTML();
  _showResults();
}

/**
 * Show the results of a search.
 */
function _showResults() {
  // hide search-tool and about
  addClass('#search-tool', 'u-hidden');
  _hideData();

  // show the results
  removeClass('#results', 'u-hidden');
}

/**
 * Clear the body of all the tables (data).
 */
function _resetHTML() {
  changeElHTML('tbody', '');
}

export default {
  setup,
};
