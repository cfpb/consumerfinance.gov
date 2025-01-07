/* ==========================================================================
   Common application-wide scripts for rural-or-underserved-tool.
   ========================================================================== */

import { ExpandableGroup } from '@cfpb/cfpb-design-system';
import * as addressUtils from './address-utils.js';
import callCensus from './call-census.js';
import contentControl from './content-control.js';
import { updateCount, updateAddressCount } from './count.js';
import {
  bindEvents,
  addEl,
  getElData,
  createEl,
  addClass,
  hasClass,
  removeClass,
  getEl,
  getEls,
  getParentEls,
} from './dom-tools.js';
import { resetError, setError, getUploadName, isCSV } from './file-input.js';
import Papaparse from 'papaparse';
import getRuralCounties from './get-rural-counties.js';
import * as textInputs from './text-inputs.js';
import callTiger from './call-tiger.js';

import('./show-map.js');

ExpandableGroup.init();

const MAX_CSV_ROWS = 250;

/**
 * @param {object} data - Census API results object.
 * @param {object} ruralCounties - Object from the census API.
 */
function censusAPI(data, ruralCounties) {
  const result = {};
  if (addressUtils.isFound(data.result)) {
    result.x = data.result.addressMatches[0].coordinates.x;
    result.y = data.result.addressMatches[0].coordinates.y;

    /*
    In the 2024 tigerweb API the layer IDs/name mappings are as follows:
    82 = Counties
    88 = 2020 Census Urban Areas
    */
    Promise.all([
      callTiger(result.x, result.y, '82'),
      callTiger(result.x, result.y, '88'),
    ])
      .then(function ([censusCounty, censusUA]) {
        result.input = data.result.input.address.address;
        result.address = data.result.addressMatches[0].matchedAddress;
        result.countyName = censusCounty.features[0].attributes.BASENAME;

        const fips =
          censusCounty.features[0].attributes.STATE +
          censusCounty.features[0].attributes.COUNTY;

        if (addressUtils.isRural(fips, ruralCounties)) {
          result.type = 'rural';
        } else if (addressUtils.isRuralCensus(censusUA.features)) {
          result.type = 'rural';
        } else {
          result.type = 'notRural';
        }

        result.id = Date.now();

        addressUtils.render(result);
        updateCount(result.type);
      })
      .catch(function (err) {
        console.log(err);
        const addressElement = createEl('<li>' + result.address + '</li>');
        addEl(getEl('#process-error-desc'), addressElement);
        removeClass('#process-error', 'u-hidden');
      });
  } else {
    result.input = data.result.input.address.address;
    result.address = 'Address not identfied';
    result.countyName = '-';
    result.block = '-';
    result.type = 'notFound';
    updateCount(result.type);
    addressUtils.render(result);
  }
}

/**
 * @param {Array} addresses - A list of addresses.
 */
function processAddresses(addresses) {
  const processed = [];

  getRuralCounties(getEl('#year').value).then(function (ruralCounties) {
    addresses.forEach(function (address) {
      if (addressUtils.isDup(address, processed)) {
        // setup the result to render
        const result = {};
        result.input = address;
        result.address = 'Duplicate';
        result.countyName = '-';
        result.block = '-';
        result.type = 'duplicate';
        addressUtils.render(result);
        updateCount(result.type);
      } else {
        // if its not dup
        callCensus(address, ruralCounties, censusAPI);
        processed.push(address);
      }
    });
  });
}

// On submit of address entered manually.
const addressFormDom = document.querySelector('#geocode');
addressFormDom.addEventListener('submit', function (evt) {
  evt.preventDefault();

  window.location.hash = 'rural-or-underserved';
  const addresses = [];

  contentControl.setup();

  [].slice.call(getEls('.input-address')).forEach(function (element) {
    if (element.value !== '') {
      addresses.push(element.value);
    }
  });

  if (addresses.length > 1) {
    removeClass('#results-total', 'u-hidden');
  }

  updateAddressCount(addresses.length);
  processAddresses(addresses);
});

// when file upload is used
const fileChangeDom = document.querySelector('#file');
fileChangeDom.addEventListener('change', function () {
  let rowCount = 0;
  const fileElement = getEl('#file');
  const fileValue = fileElement.value;

  textInputs.reset();
  getEl('#file-name').value = getUploadName(fileValue);

  resetError();

  if (isCSV(fileValue)) {
    // parse the csv to get the count
    Papaparse.parse(fileElement.files[0], {
      header: true,
      step: function (results, parser) {
        if (!addressUtils.isValid(results)) {
          parser.abort();
          setError(
            'The header row of your CSV file does not match' +
              ' our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
              ' title="Download CSV template">CSV template</a>.' +
              ' Please adjust your CSV file and try again.',
          );
          return;
        }
        if (results.data['Street Address'] !== '') {
          rowCount++;
        }
      },
      error: function () {
        console.log(arguments);
      },
      complete: function (/*results, file*/) {
        if (rowCount === 0) {
          setError(
            'There are no rows in this csv. Please update and try again.',
          );
        }
        if (rowCount >= MAX_CSV_ROWS) {
          const leftOver = rowCount - MAX_CSV_ROWS;
          setError(
            'You entered ' +
              rowCount +
              ' addresses for ' +
              getEl('#year').value +
              ' safe harbor designation. We have a limit of ' +
              MAX_CSV_ROWS +
              ' addresses. You can run the first ' +
              MAX_CSV_ROWS +
              ' now, but please recheck the remaining ' +
              leftOver +
              '.',
          );
        }
      },
    });
  } else {
    setError(
      'The file uploaded is not a CSV file. ' +
        'Please try again with a CSV file that uses ' +
        'our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
        'title="Download CSV template">CSV template</a>.' +
        ' For more information about CSV files, view our' +
        ' Frequently Asked Questions below.',
    );
  }
});

// on file submission
const geocodeCSVDom = document.querySelector('#geocode-csv');
geocodeCSVDom.addEventListener('submit', function (evt) {
  evt.preventDefault();

  window.location.hash = 'rural-or-underserved';
  let fileElement = getEl('#file-name');
  const fileValue = fileElement.value;
  if (
    fileValue === '' ||
    fileValue === 'No file chosen' ||
    fileValue === null
  ) {
    setError(
      'You have not selected a file. ' +
        'Use the "Select file" button to select the file with your addresses.',
    );
  } else if (isCSV(fileValue)) {
    let pass = true;
    let rowCount = 0;
    let addresses = [];
    fileElement = getEl('#file');
    textInputs.reset();

    // Parse the csv to get the
    Papaparse.parse(fileElement.files[0], {
      header: true,
      step: function (results, parser) {
        if (addressUtils.isValid(results)) {
          if (
            rowCount < MAX_CSV_ROWS &&
            results.data['Street Address'] !== ''
          ) {
            addresses = addressUtils.pushAddress(results, addresses);
          }
          rowCount++;
        } else {
          parser.abort();
          pass = false;
          setError(
            'The header row of your CSV file does not match' +
              ' our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
              ' title="Download CSV template">CSV template</a>.' +
              ' Please adjust your CSV file and try again.',
          );
        }
      },
      complete: function (/* results, file */) {
        if (rowCount === 0) {
          pass = false;
          setError(
            'There are no rows in this csv. Please update and try again.',
          );
        }
        if (rowCount >= MAX_CSV_ROWS) {
          const leftOver = rowCount - MAX_CSV_ROWS;
          setError(
            'You entered ' +
              rowCount +
              ' addresses for ' +
              getEl('#year').value +
              ' safe harbor designation. We have a limit of ' +
              MAX_CSV_ROWS +
              ' addresses. You can run the first ' +
              MAX_CSV_ROWS +
              ' now, but please recheck the remaining ' +
              leftOver +
              '.',
          );
        }
        if (addresses.length > 1) {
          removeClass('#results-total', 'u-hidden');
        }
        if (pass === true) {
          contentControl.setup();
          updateAddressCount(addresses.length);
          processAddresses(addresses);
        }
      },
    });
  } else {
    setError(
      'The file uploaded is not a CSV file.' +
        ' Please try again with a CSV file that uses our' +
        ' <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
        ' title="Download CSV template">CSV template</a>.' +
        ' For more information about CSV files,' +
        ' view our Frequently Asked Questions below.',
    );
  }

  return false;
});

// add inputs
const addAnotherLinkDom = document.querySelector('#add-another');
addAnotherLinkDom.addEventListener('click', function (evt) {
  evt.preventDefault();
  textInputs.add();
});

// input blur
const inputAddressDom = document.querySelector('.input-address');
inputAddressDom.addEventListener('blur', function (evt) {
  textInputs.toggleError(evt);
});

// show more rows
bindEvents('.button-more', 'click', function (evt) {
  const moreButton = evt.target;
  evt.preventDefault();
  const tableID = getElData(moreButton, 'table');
  const tableRows = getEls('#' + tableID + ' tbody tr.data');
  const tableRowsLength = tableRows.length;
  const lengthShown = Array.prototype.filter.call(tableRows, function (item) {
    return !item.classList.contains('u-hidden');
  }).length;
  for (let i = lengthShown; i < lengthShown + 10; i++) {
    removeClass(tableRows[i], 'u-hidden');
  }

  if (lengthShown + 10 >= tableRowsLength) {
    addClass('#' + tableID + 'More', 'u-hidden');
    addClass('#' + tableID + 'All', 'u-hidden');
  }
});

bindEvents('.view-all', 'click', function (evt) {
  evt.preventDefault();
  const tableID = getElData(evt.target, 'table');
  removeClass('#' + tableID + ' tbody tr.data', 'u-hidden');
  addClass('#' + tableID + 'More', 'u-hidden');
  addClass('#' + tableID + 'All', 'u-hidden');
});

// print
bindEvents('#print', 'click', window.print.bind(window));

// csv download
/**
 * // TODO: Refactor to remove this. We're in a post-IE world.
 * Detect whether IE is used or not.
 * @returns {number|boolean} IE version number, or false if not IE.
 */
function detectIE() {
  const ua = window.navigator.userAgent;

  const msie = ua.indexOf('MSIE ');
  if (msie > 0) {
    // IE 10 or older => return version number
    return parseInt(ua.substring(msie + 5, ua.indexOf('.', msie)), 10);
  }

  const trident = ua.indexOf('Trident/');
  if (trident > 0) {
    // IE 11 => return version number
    const rv = ua.indexOf('rv:');
    return parseInt(ua.substring(rv + 3, ua.indexOf('.', rv)), 10);
  }

  const edge = ua.indexOf('Edge/');
  if (edge > 0) {
    // IE 12 => return version number
    return parseInt(ua.substring(edge + 5, ua.indexOf('.', edge)), 10);
  }

  // other browser
  return false;
}

bindEvents('#download', 'click', function (evt) {
  evt.preventDefault();
  const theCSV = generateCSV();
  if (detectIE() === false) {
    window.open(' data:text/csv;charset=utf-8,' + encodeURIComponent(theCSV));
  } else {
    const blob = new Blob([theCSV], { type: 'text/csv;charset=utf-8,' });
    navigator.msSaveOrOpenBlob(blob, 'rural-or-underserved.csv');
  }
});

/**
 * @returns {string} A comma-separate values string of address info.
 */
function generateCSV() {
  let theCSV = '';
  const date = new Date();
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear();

  theCSV =
    'Address entered, Address identified, County, Rural' +
    ' or underserved?, Date processed\n';

  /**
   * Process each cell in a table row.
   * @param {HTMLElement} element - A table data element to process.
   */
  function _loopHandler(element) {
    const isHidden = hasClass(getParentEls('.js-table'), 'u-hidden');

    /* Add a data row, if table isn't hidden (!)
       and map cols have colspan and we don't want those. */
    if (isHidden === false && element.getAttribute('colspan') === null) {
      const CSVLabel = element.textContent.replace('Show map', '');

      // Put the content in first.
      theCSV += '"' + CSVLabel + '"';

      if (element.matches(':last-child')) {
        theCSV = theCSV + ',' + monthIndex + '/' + day + '/' + year + '\n';
      } else {
        theCSV += ',';
      }
    }
  }

  // loop through each row
  [].slice
    .call(getEls('.rout-results-table tbody tr td'))
    .forEach(_loopHandler);

  return theCSV;
}
