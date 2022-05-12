import DT from './dom-tools';

/**
 * Checks whether an address is a duplicate to that in an array of addresses.
 * @param {string} address - An address.
 * @param {Array} duplicates - An array of addresses.
 * @returns {boolean} True if it is a duplicate, false otherwise.
 */
function isDup( address, duplicates ) {
  return typeof address === 'string' &&
         Array.isArray( duplicates ) &&
         duplicates.indexOf( address ) !== -1;
}

/**
 * @param {Object} response - Object with addressMatches and input.
 * @returns {boolean} True if there was a match, false otherwise.
 */
function isFound( response ) {
  const match = response.addressMatches;

  return Array.isArray( match ) && match.length !== 0;
}

/**
 *
 * @param {string} fips - An ID.
 * @param {Object} counties - Object from the census API.
 * @returns {boolean} Whether the county is rural.
 */
function isRural( fips, counties ) {
  for ( let i = 0; i < counties.length; i++ ) {
    if ( fips === counties[i] ) return true;
  }
  return false;
}

/**
 * @param {Array} urbanClusters - Array from census API.
 * @param {Array} urbanAreas - Array from census API.
 * @returns {boolean} True if address is rural, false otherwise.
 */
function isRuralCensus( urbanClusters, urbanAreas ) {
  return ( urbanClusters === null || urbanClusters.length === 0 ) &&
         ( urbanAreas === null || urbanAreas.length === 0 );
}

/**
 * @param {Array} row - Row from a CSV.
 * @returns {boolean} True if row has correct fields, false otherwise.
 */
function isValid( row ) {
  return row.meta.fields[0] === 'Street Address' &&
         row.meta.fields[1] === 'City' &&
         row.meta.fields[2] === 'State' &&
         row.meta.fields[3] === 'Zip';
}

/**
 * Add an address table row to the page's markup.
 * @param {Object} result - Address data.
 */
function render( result ) {
  let rowCount = DT.getEls( '#' + result.type + ' tbody tr' ).length;
  if ( result.type === 'rural' || result.type === 'notRural' ) {
    rowCount = DT.getEls( '#' + result.type + ' tbody tr' ).length / 2;
  }

  let hideRow = false;
  if ( rowCount >= 5 ) {
    hideRow = true;
    DT.removeClass( '#' + result.type + 'More', 'u-hidden' );
    DT.removeClass( '#' + result.type + 'All', 'u-hidden' );
  }

  let rural;
  if ( result.type === 'rural' ) {
    rural = 'Yes';
  } else if ( result.type === 'notRural' ) {
    rural = 'No';
  } else {
    rural = '-';
  }

  let rowHTML = '<tr class="data';
  if ( hideRow === true ) {
    rowHTML += ' u-hidden';
  }
  rowHTML = rowHTML + '"><td>' + result.input + '</td>' +
    '<td>' + result.address + '</td>' +
    '<td>' + result.countyName + '</td>' +
    '<td>' + rural;
  // add the map link if needed
  if ( rural !== '-' ) {
    rowHTML = rowHTML +
      ' <a href="#" class="no-decoration hide-print' +
      ' jsLoadMap right" data-map="false" data-lat="' +
      result.x + '" data-lon="' + result.y + '" data-id="loc-' +
      result.id +
      '">Show map <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"></path></svg></a>';
  }
  rowHTML += '</td></tr>';
  // add the map if needed
  if ( rural !== '-' ) {
    rowHTML = rowHTML +
    '<tr class="u-hidden"><td colspan="5">' +
    '<div class="map" id="loc-' + result.id + '"></div></td></tr>';
  }

  DT.removeClass( '#' + result.type, 'u-hidden' );
  DT.addEl( DT.getEl( '#' + result.type + ' tbody' ), rowHTML );
}

/**
 * @param {Object} row - Address data from a CSV.
 * @param {Array} addresses - List of addresses.
 * @returns {Array} Return the updated list of addresses.
 */
function pushAddress( row, addresses ) {
  addresses.push( row.data['Street Address'] +
    ', ' +
    row.data.City + ', ' +
    row.data.State + ' ' +
    row.data.Zip );
  return addresses;
}

export default {
  isDup,
  isFound,
  isRural,
  isRuralCensus,
  isValid,
  render,
  pushAddress
};
