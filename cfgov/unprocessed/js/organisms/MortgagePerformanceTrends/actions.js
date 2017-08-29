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

actions.updateChart = ( geoId, geoName, geoType, includeNational ) => {
  var action = {
    type: 'UPDATE_CHART',
    geo: {
      id: geoId,
      name: geoName
    }
  };
  if ( geoType ) {
    action.geo.type = geoType;
  }
  if ( includeNational ) {
    action.includeNational = includeNational;
  }
  return action;
};

actions.updateNational = includeNational => {
  var action = {
    type: 'UPDATE_CHART',
    includeNational
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

actions.fetchMetros = metroState => dispatch => {
  dispatch( actions.requestMetros( metroState ) );
  return utils.getMetroData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting metro data', err );
    }
    // Alphabetical order
    var newMetros = data[metroState].msas.sort( ( a, b ) => (a.name < b.name ? -1 : 1) );
    newMetros = newMetros.filter( msa => msa.valid );
    dispatch( actions.setMetros( newMetros ) );
    dispatch( actions.setGeo( newMetros[0].fips, newMetros[0].name, 'metro' ) );
    dispatch( actions.updateChart( newMetros[0].fips, newMetros[0].name, 'metro' ) );
    return newMetros;
  } );
};

actions.fetchCounties = ( countyState, includeNational ) => dispatch => {
  dispatch( actions.requestCounties( countyState ) );
  return utils.getCountyData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting county data', err );
    }
    // Alphabetical order
    var newCounties = data[countyState].counties.sort( ( a, b ) => a.county < b.county ? -1 : 1 );
    newCounties = newCounties.filter( county => county.valid );
    dispatch( actions.setCounties( newCounties ) );
    dispatch( actions.setGeo( newCounties[0].fips, newCounties[0].county, 'county' ) );
    dispatch( actions.updateChart( newCounties[0].fips, newCounties[0].county, 'county', includeNational ) );
    return newCounties;
  } );
};

actions.setMetros = metros => ( {
  type: 'SET_METROS',
  metros: metros
} );

actions.setCounties = counties => ( {
  type: 'SET_COUNTIES',
  counties: counties
} );

actions.startLoading = () => ( {
  type: 'STOP_LOADING',
  isLoading: true
} );

actions.stopLoading = () => ( {
  type: 'STOP_LOADING',
  isLoading: false
} );

module.exports = actions;
