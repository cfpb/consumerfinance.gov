'use strict';

var utils = require( './utils' );

var actions = {};

actions.setGeo = ( geoId, geoName, geoType ) => ( {
  type: 'SET_GEO',
  geo: {
    type: geoType,
    id: geoId,
    name: geoName
  }
} );

actions.clearGeo = () => ( {
  type: 'CLEAR_GEO'
} );

actions.updateChart = ( geoId, geoName, geoType, includeComparison ) => {
  var action = {
    type: 'UPDATE_CHART',
    geo: {
      id: geoId,
      name: geoName
    },
    includeComparison
  };
  if ( geoType ) {
    action.geo.type = geoType;
  }
  return action;
};

actions.updateNational = includeComparison => {
  var action = {
    type: 'UPDATE_CHART',
    includeComparison
  };
  return action;
};

actions.updateDate = date => ( {
  type: 'UPDATE_DATE',
  date: date
} );

actions.requestCounties = () => ( {
  type: 'REQUEST_COUNTIES',
  isLoadingCounties: true
} );

actions.requestMetros = () => ( {
  type: 'REQUEST_METROS',
  isLoadingMetros: true
} );

actions.requestNonMetros = () => ( {
  type: 'REQUEST_NON_METROS',
  isLoadingNonMetros: true
} );

actions.fetchMetros = ( metroState, includeComparison ) => dispatch => {
  dispatch( actions.requestMetros( metroState ) );
  return utils.getMetroData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting metro data', err );
    }
    // Alphabetical order
    var newMetros = data[metroState].metros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newMetros = newMetros.filter( metro => metro.valid );
    if ( !newMetros.length ) {
      newMetros = [{
        fips: null,
        name: 'No metros have sufficient data'
      }];
    }
    dispatch( actions.setMetros( newMetros ) );
    dispatch( actions.setGeo( newMetros[0].fips, newMetros[0].name, 'metro' ) );
    dispatch( actions.updateChart( newMetros[0].fips, newMetros[0].name, 'metro', includeComparison ) );
    return newMetros;
  } );
};

actions.fetchNonMetros = ( metroState, includeComparison ) => dispatch => {
  dispatch( actions.requestNonMetros() );
  return utils.getNonMetroData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting non-metro data', err );
    }
    var nonMetros = data.filter( nonMetro => nonMetro.valid );
    // Alphabetical order
    nonMetros = nonMetros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    dispatch( actions.setNonMetros( nonMetros ) );
    dispatch( actions.setGeo( nonMetros[0].fips, nonMetros[0].name, 'non-metro' ) );
    dispatch( actions.updateChart( nonMetros[0].fips, nonMetros[0].name, 'non-metro', includeComparison ) );
    return nonMetros;
  } );
};

actions.fetchCounties = ( countyState, includeComparison ) => dispatch => {
  dispatch( actions.requestCounties( countyState ) );
  return utils.getCountyData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting county data', err );
    }
    // Alphabetical order
    var newCounties = data[countyState].counties.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newCounties = newCounties.filter( county => county.valid );
    dispatch( actions.setCounties( newCounties ) );
    dispatch( actions.setGeo( newCounties[0].fips, newCounties[0].name, 'county' ) );
    dispatch( actions.updateChart( newCounties[0].fips, newCounties[0].name, 'county', includeComparison ) );
    return newCounties;
  } );
};

actions.setMetros = metros => ( {
  type: 'SET_METROS',
  metros: metros
} );

actions.setNonMetros = metros => ( {
  type: 'SET_NON_METROS',
  nonMetros: metros
} );

actions.setCounties = counties => ( {
  type: 'SET_COUNTIES',
  counties: counties
} );

actions.startLoading = () => ( {
  type: 'START_LOADING',
  isLoading: true
} );

actions.stopLoading = () => ( {
  type: 'STOP_LOADING',
  isLoading: false
} );

module.exports = actions;
