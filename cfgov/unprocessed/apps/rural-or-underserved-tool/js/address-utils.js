import { addEl, getEl, getEls, removeClass } from './dom-tools.js';

import PLUS_ROUND_ICON from '@cfpb/cfpb-design-system/icons/plus-round.svg';

/**
 * Checks whether an address is a duplicate to that in an array of addresses.
 * @param {string} address - An address.
 * @param {Array} duplicates - An array of addresses.
 * @returns {boolean} True if it is a duplicate, false otherwise.
 */
function isDup(address, duplicates) {
  return (
    typeof address === 'string' &&
    Array.isArray(duplicates) &&
    duplicates.indexOf(address) !== -1
  );
}

/**
 * @param {object} response - Object with addressMatches and input.
 * @returns {boolean} True if there was a match, false otherwise.
 */
function isFound(response) {
  const match = response.addressMatches;

  return Array.isArray(match) && match.length !== 0;
}

/**
 *
 * @param {string} fips - An ID.
 * @param {object} counties - Object from the census API.
 * @returns {boolean} Whether the county is rural.
 */
function isRural(fips, counties) {
  for (let i = 0; i < counties.length; i++) {
    if (fips === counties[i]) return true;
  }
  return false;
}

/**
 * @param {Array} urbanAreas - Array from census API.
 * @returns {boolean} True if address is rural, false otherwise.
 */
function isRuralCensus(urbanAreas) {
  return urbanAreas === null || urbanAreas.length === 0;
}

/**
 * @param {Array} row - Row from a CSV.
 * @returns {boolean} True if row has correct fields, false otherwise.
 */
function isValid(row) {
  return (
    row.meta.fields[0] === 'Street Address' &&
    row.meta.fields[1] === 'City' &&
    row.meta.fields[2] === 'State' &&
    row.meta.fields[3] === 'Zip'
  );
}

/**
 * Add an address table row to the page's markup.
 * @param {object} result - Address data.
 */
function render(result) {
  let rowCount = getEls('#' + result.type + ' tbody tr').length;
  if (result.type === 'rural' || result.type === 'notRural') {
    rowCount = getEls('#' + result.type + ' tbody tr').length / 2;
  }

  let hideRow = false;
  if (rowCount >= 5) {
    hideRow = true;
    removeClass('#' + result.type + 'More', 'u-hidden');
    removeClass('#' + result.type + 'All', 'u-hidden');
  }

  let rural;
  if (result.type === 'rural') {
    rural = 'Yes';
  } else if (result.type === 'notRural') {
    rural = 'No';
  } else {
    rural = '-';
  }

  let rowHTML = '<tr class="data';
  if (hideRow === true) {
    rowHTML += ' u-hidden';
  }
  rowHTML = `${rowHTML}">
    <td>${result.input}</td>
    <td>${result.address}</td>
    <td>${result.countyName}</td>
    <td>${rural}`;
  // add the map link if needed
  if (rural !== '-') {
    rowHTML = `${rowHTML}
      <a href="#"
         class="no-decoration hide-print js-load-map right"
         data-map="false"
         data-lat="${result.x}"
         data-lon="${result.y}"
         data-id="loc-${result.id}">
          Show map ${PLUS_ROUND_ICON}`;
  }
  rowHTML += '</td></tr>';
  // add the map if needed
  if (rural !== '-') {
    rowHTML = `${rowHTML}
      <tr class="u-hidden">
        <td colspan="5">
          <div class="map" id="loc-${result.id}"></div>
        </td>
      </tr>`;
  }

  removeClass('#' + result.type, 'u-hidden');
  addEl(getEl('#' + result.type + ' tbody'), rowHTML);
}

/**
 * @param {object} row - Address data from a CSV.
 * @param {Array} addresses - List of addresses.
 * @returns {Array} Return the updated list of addresses.
 */
function pushAddress(row, addresses) {
  addresses.push(
    row.data['Street Address'] +
      ', ' +
      row.data.City +
      ', ' +
      row.data.State +
      ' ' +
      row.data.Zip,
  );
  return addresses;
}

export { isDup, isFound, isRural, isRuralCensus, isValid, render, pushAddress };
