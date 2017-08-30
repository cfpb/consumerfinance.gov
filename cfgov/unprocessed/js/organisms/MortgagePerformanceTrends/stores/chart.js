'use strict';

const Store = require( './store' );

const updateGeo = ( geo, action ) => {
  switch ( action.type ) {
    case 'CLEAR_GEO':
      return {
        type: null,
        id: null,
        name: null
      };
    case 'SET_GEO':
    case 'UPDATE_CHART':
      if ( !action.geo ) {
        return geo;
      }
      return {
        type: action.geo.type || geo.type,
        id: action.geo.id,
        name: action.geo.name
      };
    default:
      return geo;
  }
};

const isLoadingMetros = action => {
  switch ( action.type ) {
    case 'REQUEST_METROS':
      return true;
    default:
      return false;
  }
};

const isLoadingCounties = action => {
  switch ( action.type ) {
    case 'REQUEST_COUNTIES':
      return true;
    default:
      return false;
  }
};

const isLoading = action => {
  switch ( action.type ) {
    case 'UPDATE_CHART':
    case 'SET_GEO':
      return true;
    default:
      return false;
  }
};

const updateMetros = ( metros, action ) => {
  switch ( action.type ) {
    case 'SET_METROS':
      return action.metros;
    case 'FETCH_METROS':
    case 'REQUEST_METROS':
    default:
      return metros;
  }
};

const updateCounties = ( counties, action ) => {
  switch ( action.type ) {
    case 'SET_COUNTIES':
      return action.counties;
    case 'FETCH_COUNTIES':
    case 'REQUEST_COUNTIES':
    default:
      return counties;
  }
};

const includeNational = ( include, action ) => {
  switch ( action.type ) {
    case 'UPDATE_CHART':
      return typeof action.includeNational === 'undefined' ? include : action.includeNational;
    default:
      return include;
  }
};

const initialState = {
  geo: {
    // 'state', 'metro' or 'county'
    type: null,
    // FIPS code of the geo, e.g. '04194'
    id: null,
    // Geo name, e.g. 'Ohio'
    name: null
  },
  counties: {},
  metros: {},
  // Is the chart waiting for data?
  isLoading: false,
  // Is the county dropdown waiting for data?
  isLoadingCounties: false,
  // Is the chart being re-rendered?
  isLoadingChart: false,
  // Should the national trend be shown alongside the geo's?
  includeNational: true
};

class LineChartStore extends Store {
  constructor( middleware ) {
    super( middleware );
    this.prevState = {};
    this.state = initialState;
    this.state = this.reduce( this.state, {} );
  }
  reduce( state, action ) {
    var newState = {
      geo: updateGeo( state.geo, action ),
      isLoading: isLoading( action ),
      isLoadingMetros: isLoadingMetros( action ),
      isLoadingCounties: isLoadingCounties( action ),
      includeNational: includeNational( state.includeNational, action ),
      counties: updateCounties( state.counties, action ),
      metros: updateMetros( state.metros, action )
    };
    return newState;
  }
}

module.exports = LineChartStore;
