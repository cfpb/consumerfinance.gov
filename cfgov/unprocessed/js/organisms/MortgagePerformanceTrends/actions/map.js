'use strict';

const utils = require( '../utils' );
const defaultActionCreators = require( './default' );

const mapActionCreators = defaultActionCreators();

mapActionCreators.zoomChart = stateAbbr => {
  var action = {
    type: 'ZOOM_CHART',
    target: stateAbbr
  };
  return action;
};

mapActionCreators.updateChart = ( geoId, geoName, geoType ) => {
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
  if ( !geoId ) {
    action.counties = [];
    action.metros = [];
  }
  return action;
};

mapActionCreators.fetchMetros = ( metroState, shouldZoom ) => dispatch => {
  dispatch( mapActionCreators.requestMetros( metroState ) );
  return utils.getMetroData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting metro data', err );
    }
    // Alphabetical order
    let newMetros = data[metroState].metros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newMetros = newMetros.filter( metro => metro.valid );
    if ( !newMetros.length ) {
      newMetros = [ {
        fips: null,
        name: 'No metros have sufficient data'
      } ];
    }
    dispatch( mapActionCreators.setMetros( newMetros ) );
    if ( newMetros.length && shouldZoom ) {
      dispatch( mapActionCreators.zoomChart( metroState ) );
    }
    return newMetros;
  } );
};

mapActionCreators.fetchCounties = ( countyState, shouldZoom ) => dispatch => {
  dispatch( mapActionCreators.requestCounties( countyState ) );
  return utils.getCountyData( ( err, data ) => {
    if ( err ) {
      return console.error( 'Error getting county data', err );
    }
    // Alphabetical order
    var newCounties = data[countyState].counties.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
    newCounties = newCounties.filter( county => county.valid );
    dispatch( mapActionCreators.setCounties( newCounties ) );
    if ( newCounties.length && shouldZoom ) {
      dispatch( mapActionCreators.zoomChart( countyState ) );
    }
    return newCounties;
  } );
};

module.exports = mapActionCreators;
