'use strict';

const utils = require( '../utils' );
const defaultActionCreators = require( './default' );

const chartActionCreators = defaultActionCreators();

/**
 * fetchMetros - Creates async action to fetch list of metros
 *
 * @param {String} metroState Two-letter U.S. state abbreviation.
 * @param {Boolean} includeComparison Include national comparison?
 *
 * @returns {Function} Thunk called with new metros
 */
chartActionCreators.fetchMetros = ( metroState, includeComparison ) => dispatch => {
  dispatch( chartActionCreators.requestMetros( metroState ) );
  return utils.getMetroData( data => {
    // Alphabetical order
    var newMetros = data[metroState].metros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newMetros = newMetros.filter( metro => metro.valid );
    if ( !newMetros.length ) {
      newMetros = [ {
        fips: null,
        name: 'No metros have sufficient data'
      } ];
    }
    dispatch( chartActionCreators.setMetros( newMetros ) );
    dispatch( chartActionCreators.setGeo( newMetros[0].fips, newMetros[0].name, 'metro' ) );
    dispatch( chartActionCreators.updateChart( newMetros[0].fips, newMetros[0].name, 'metro', includeComparison ) );
    return newMetros;
  } );
};

/**
 * fetchCounties - Creates async action to fetch list of counties
 *
 * @param {String} countyState Two-letter U.S. state abbreviation.
 * @param {Boolean} includeComparison Include national comparison?
 *
 * @returns {Function} Thunk called with new metros
 */
chartActionCreators.fetchCounties = ( countyState, includeComparison ) => dispatch => {
  dispatch( chartActionCreators.requestCounties( countyState ) );
  return utils.getCountyData( data => {
    // Alphabetical order
    var newCounties = data[countyState].counties.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newCounties = newCounties.filter( county => county.valid );
    dispatch( chartActionCreators.setCounties( newCounties ) );
    dispatch( chartActionCreators.setGeo( newCounties[0].fips, newCounties[0].name, 'county' ) );
    dispatch( chartActionCreators.updateChart( newCounties[0].fips, newCounties[0].name, 'county', includeComparison ) );
    return newCounties;
  } );
};

module.exports = chartActionCreators;
