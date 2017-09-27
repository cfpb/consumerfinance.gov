'use strict';

const utils = require( '../utils' );

const defaultActionCreators = () => {

  const actions = {
    setGeo: ( geoId, geoName, geoType ) => ( {
      type: 'SET_GEO',
      geo: {
        type: geoType,
        id: geoId,
        name: geoName
      }
    } ),
    clearGeo: () => ( {
      type: 'CLEAR_GEO'
    } ),
    updateChart: ( geoId, geoName, geoType, includeComparison ) => {
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
    },
    updateNational: includeComparison => {
      var action = {
        type: 'UPDATE_CHART',
        includeComparison
      };
      return action;
    },
    updateDate: date => ( {
      type: 'UPDATE_DATE',
      date: date
    } ),
    requestCounties: () => ( {
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true
    } ),
    requestMetros: () => ( {
      type: 'REQUEST_METROS',
      isLoadingMetros: true
    } ),
    requestNonMetros: () => ( {
      type: 'REQUEST_NON_METROS',
      isLoadingNonMetros: true
    } ),
    fetchNonMetros: ( metroState, includeComparison ) => dispatch => {
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
    },
    setMetros: metros => ( {
      type: 'SET_METROS',
      metros: metros
    } ),
    setNonMetros: metros => ( {
      type: 'SET_NON_METROS',
      nonMetros: metros
    } ),
    setCounties: counties => ( {
      type: 'SET_COUNTIES',
      counties: counties
    } ),
    startLoading: () => ( {
      type: 'START_LOADING',
      isLoading: true
    } ),
    stopLoading: () => ( {
      type: 'STOP_LOADING',
      isLoading: false
    } )
  };

  return actions;

};

module.exports = defaultActionCreators;
