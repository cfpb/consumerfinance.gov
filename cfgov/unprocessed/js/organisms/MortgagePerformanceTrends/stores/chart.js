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

const isLoadingNonMetros = action => {
  switch ( action.type ) {
    case 'REQUEST_NON_METROS':
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

const updateStates = ( states, action ) => {
  switch ( action.type ) {
    case 'SET_STATES':
      return action.states;
    case 'FETCH_STATES':
    case 'REQUEST_STATES':
    default:
      return states;
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

const updateNonMetros = ( nonMetros, action ) => {
  switch ( action.type ) {
    case 'SET_NON_METROS':
      return action.nonMetros;
    case 'FETCH_NON__METROS':
    case 'REQUEST_NON_METROS':
    default:
      return nonMetros;
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

const includeComparison = ( include, action ) => {
  switch ( action.type ) {
    case 'UPDATE_CHART':
      return typeof action.includeComparison === 'undefined' ? include : action.includeComparison;
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
  nonMetros: {},
  states: {},
  // Is the chart waiting for data?
  isLoading: false,
  // Is the county dropdown waiting for data?
  isLoadingCounties: false,
  // Is the chart being re-rendered?
  isLoadingChart: false,
  // Should the national trend be shown alongside the geo's?
  includeComparison: true
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
      isLoadingNonMetros: isLoadingNonMetros( action ),
      isLoadingCounties: isLoadingCounties( action ),
      includeComparison: includeComparison( state.includeComparison, action ),
      counties: updateCounties( state.counties, action ),
      metros: updateMetros( state.metros, action ),
      nonMetros: updateNonMetros( state.nonMetros, action ),
      states: updateStates( state.states, action )
    };
    return newState;
  }
}

module.exports = LineChartStore;
