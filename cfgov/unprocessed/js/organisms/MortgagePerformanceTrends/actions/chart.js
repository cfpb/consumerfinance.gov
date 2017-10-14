'use strict';

const utils = require( '../utils' );
const defaultActionCreators = require( './default' );

const chartActionCreators = defaultActionCreators();

/**
 * fetchMetroStates - Creates async action to fetch list of valid metro states.
 *
 * @param {String} metroState Two-letter U.S. state abbreviation.
 *
 * @returns {Function} Thunk called with metro states.
 */
chartActionCreators.fetchMetroStates = metroState => dispatch =>
  utils.getMetroData( states => {
    let metroStates = [];
    let reuseState = false;
    Object.keys( states ).forEach( state => {
      const isValid = states[state].metros.reduce( ( prev, curr ) => {
        if ( curr.fips.indexOf( '-non' ) > -1 ) {
          return prev;
        }
        return prev || curr.valid || false;
      }, false );
      if ( isValid ) {
        reuseState = reuseState || metroState === state;
        metroStates.push( {
          abbr: state,
          fips: states[state].state_fips,
          name: states[state].state_name,
          selected: metroState === state
        } );
      }
    } );
    // Alphabetical order
    metroStates = metroStates.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    // If the provided state isn't valid for this location type,
    // use the first state in the list.
    if ( !reuseState ) {
      metroState = metroStates[0].abbr;
    }
    dispatch( chartActionCreators.setStates( metroStates ) );
    dispatch( chartActionCreators.fetchMetros( metroState ) );
    return metroStates;
  } );

/**
 * fetchNonMetroStates - Creates async action to fetch list of valid metro states.
 *
 * @param {String} nonMetroState Two-letter U.S. state abbreviation.
 *
 * @returns {Function} Thunk called with metro states.
 */
chartActionCreators.fetchNonMetroStates = nonMetroState => dispatch =>
  utils.getNonMetroData( states => {
    let nonMetroStates = [];
    states.forEach( state => {
      if ( state.valid ) {
        nonMetroStates.push( {
          abbr: state.abbr,
          fips: state.fips,
          name: state.state_name,
          text: state.name,
          selected: nonMetroState === state.abbr
        } );
      }
    } );
    // Alphabetical order
    nonMetroStates = nonMetroStates.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    dispatch( chartActionCreators.setStates( nonMetroStates ) );
    dispatch( chartActionCreators.fetchNonMetros( nonMetroState ) );
    return nonMetroStates;
  } );

/**
 * fetchCountyStates - Creates async action to fetch list of valid metro states.
 *
 * @param {String} countyState Two-letter U.S. state abbreviation.
 *
 * @returns {Function} Thunk called with county states.
 */
chartActionCreators.fetchCountyStates = countyState => dispatch =>
  utils.getCountyData( states => {
    let countyStates = [];
    let reuseState = false;
    Object.keys( states ).forEach( state => {
      const isValid = states[state].counties.reduce( ( prev, curr ) =>
        prev || curr.valid || false
      , false );
      if ( isValid ) {
        reuseState = reuseState || countyState === state;
        countyStates.push( {
          abbr: state,
          fips: states[state].state_fips,
          name: states[state].state_name,
          selected: countyState === state
        } );
      }
    } );
    // Alphabetical order
    countyStates = countyStates.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    // If the provided state isn't valid for this location type,
    // use the first state in the list.
    if ( !reuseState ) {
      countyState = countyStates[0].abbr;
    }
    dispatch( chartActionCreators.setStates( countyStates ) );
    dispatch( chartActionCreators.fetchCounties( countyState ) );
    return countyStates;
  } );

/**
 * setStates - New U.S. states.
 *
 * @param {Array} states List of U.S. states.
 * @returns {Object} Action with new U.S. states.
 */
chartActionCreators.setStates = states => ( {
  type: 'SET_STATES',
  states: states
} );

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
