'use strict';

var ccb = require( 'cfpb-chart-builder' );
var actions = require( '../actions' );
var Store = require( '../stores/chart' );
var utils = require( '../utils' );

var store = new Store( [ utils.thunkMiddleware, utils.loggerMiddleware ] );

class MortgagePerformanceLineChart {
  constructor( { container } ) {
    // TODO: Make these selections less verbose.
    this.$container = document.getElementById( container );
    this.$form = this.$container.querySelector( '#mp-line-chart-controls' );
    this.$geo = this.$container.querySelector( '#mp-line-chart-geo' );
    this.$state = this.$container.querySelector( '#mp-line-chart-state' );
    this.$metro = this.$container.querySelector( '#mp-line-chart-metro' );
    this.$nonMetro = this.$container.querySelector( '#mp-line-chart-non-metro' );
    this.$county = this.$container.querySelector( '#mp-line-chart-county' );
    this.$compareContainer = this.$container.querySelector( '#mp-line-chart-compare-container' );
    this.$compare = this.$container.querySelector( '#mp-line-chart-compare' );
    this.$chart = this.$container.querySelector( '#mp-line-chart' );
    this.$chartTitle = document.querySelector( '#mp-line-chart-title-status' );
    this.$chartTitleGeo = document.querySelector( '#mp-line-chart-title-status-geo' );
    this.$chartTitleComparison = document.querySelector( '#mp-line-chart-title-status-comparison' );
    this.$loadingSpinner = document.querySelector( '#mp-chart-loading' );
    this.timespan = this.$container.getAttribute( 'data-chart-time-span' );
    this.chart = ccb.createChart( {
      el: this.$chart,
      source: `time-series/${ this.timespan }/national`,
      type: 'line-comparison'
    } );
    this.eventListeners();
    utils.hideEl( this.$chartTitleComparison );
    utils.hideEl( this.$loadingSpinner );
    utils.hideEl( this.$compareContainer );
  }
}

MortgagePerformanceLineChart.prototype.eventListeners = function() {
  this.$form.addEventListener( 'change', this.onChange.bind( this ) );
  store.subscribe( this.renderChart.bind( this ) );
  store.subscribe( this.renderChartTitle.bind( this ) );
  store.subscribe( this.renderChartForm.bind( this ) );
  store.subscribe( this.renderCounties.bind( this ) );
  store.subscribe( this.renderMetros.bind( this ) );
  store.subscribe( this.renderNonMetros.bind( this ) );
};

MortgagePerformanceLineChart.prototype.onClick = function( event ) {
  var change = new Event( 'change' );
  this.$container.querySelector( 'input[name="mp-line-chart_geo"]:checked' ).checked = false;
  this.$form.dispatchEvent( change );
  event.preventDefault();
};

MortgagePerformanceLineChart.prototype.onChange = function( event ) {

  var action, geoEl, geoType, geoId, geoName;
  var includeComparison = this.$compare.checked;

  switch ( event.target.id ) {
    case 'mp-line-chart_geo-state':
      // Reset the county dropdown to the first item if we're no longer using it
      this.$metro.selectedIndex = 0;
      this.$nonMetro.selectedIndex = 0;
      this.$county.selectedIndex = 0;
      geoId = this.$state.value;
      geoName = this.$state.options[this.$state.selectedIndex].text;
      action = actions.setGeo( geoId, geoName, 'state' );
      break;
    case 'mp-line-chart_geo-metro':
      action = actions.fetchMetros( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ) );
      break;
    case 'mp-line-chart_geo-non-metro':
      action = actions.fetchNonMetros();
      break;
    case 'mp-line-chart_geo-county':
      action = actions.fetchCounties( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ) );
      break;
    case 'mp-line-chart-state':
      geoType = this.$container.querySelector( 'input[name="mp-line-chart_geo"]:checked' ).id.replace( 'mp-line-chart_geo-', '' );
      // TODO: Waaaaay too much code repetition here.
      if ( geoType === 'state' ) {
        geoId = this.$state.value;
        geoName = this.$state.options[this.$state.selectedIndex].text;
        action = actions.updateChart( geoId, geoName, 'state', includeComparison );
      }
      if ( geoType === 'metro' ) {
        geoId = this.$metro.value;
        geoName = this.$metro.options[this.$metro.selectedIndex].text;
        action = actions.fetchMetros( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ), includeComparison );
      }
      if ( geoType === 'non-metro' ) {
        geoId = this.$nonMetro.value;
        geoName = this.$nonMetro.options[this.$nonMetro.selectedIndex].text;
        action = actions.fetchNonMetros( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ), includeComparison );
      }
      if ( geoType === 'county' ) {
        geoId = this.$county.value;
        geoName = this.$county.options[this.$county.selectedIndex].text;
        action = actions.fetchCounties( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ), includeComparison );
      }
      break;
    case 'mp-line-chart-metro':
      geoId = this.$metro.value;
      geoName = this.$metro.options[this.$metro.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, 'metro', includeComparison );
      break;
    case 'mp-line-chart-non-metro':
      geoId = this.$nonMetro.value;
      geoName = this.$nonMetro.options[this.$nonMetro.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, 'non-metro', includeComparison );
      break;
    case 'mp-line-chart-county':
      geoId = this.$county.value;
      geoName = this.$county.options[this.$county.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, 'county', includeComparison );
      break;
    case 'mp-line-chart-compare':
      utils.hideEl( this.$chartTitleComparison );
      action = actions.updateNational( includeComparison );
      break;
    default:
      action = actions.clearGeo();
  }

  store.dispatch( action );

};

MortgagePerformanceLineChart.prototype.renderChart = function( prevState, state ) {
  var source;
  var baseSource = `time-series/${ this.timespan }/national`;
  // If the geo hasn't changed, don't re-render the chart.
  if ( prevState.geo.id === state.geo.id && prevState.includeComparison === state.includeComparison ) {
    return;
  }

  // If no geo is provided, default to national data
  if ( !state.geo.id || !state.geo.type ) {
    this.chart.update( {
      source: baseSource
    } ).then( () => {
      store.dispatch( actions.stopLoading() );
    } );
    return;
  }

  // Otherwise, load the geo and optionally national data
  source = `time-series/${ this.timespan }/${ state.geo.id }`;
  if ( state.includeComparison ) {
    source = `${ source };${ baseSource }`;
  }
  this.chart.update( {
    source: source
  } ).then( () => {
    store.dispatch( actions.stopLoading() );
  } );
};

MortgagePerformanceLineChart.prototype.renderChartForm = function( prevState, state ) {
  // If we're waiting for data, abort.
  // if ( state.isLoading ) {
  //   return utils.showEl( this.$loadingSpinner );
  // }
  // utils.hideEl( this.$loadingSpinner );
  var geoType;
  if ( prevState.isLoadingCounties || state.isLoadingCounties ) {
    geoType = 'county';
  } else if ( prevState.isLoadingMetros || state.isLoadingMetros ) {
    geoType = 'metro';
  } else if ( prevState.isLoadingNonMetros || state.isLoadingNonMetros ) {
    geoType = 'non-metro';
  } else {
    geoType = state.geo.type;
  }
  var geo = this.$container.querySelector( `#mp-line-chart-${ geoType }-container` );
  var containers = this.$container.querySelectorAll( '.mp-line-chart-select-container' );
  for ( var i = 0; i < containers.length; ++i ) {
    utils.hideEl( containers[i] );
  }
  if ( geoType === 'county' || geoType === 'metro' ) {
    utils.showEl( this.$container.querySelector( '#mp-line-chart-state-container' ) );
  }
  if ( geoType ) {
    utils.showEl( this.$compareContainer );
  } else {
    utils.hideEl( this.$compareContainer );
  }
  if ( geo ) {
    utils.showEl( geo );
  }
};

MortgagePerformanceLineChart.prototype.renderChartTitle = function( prevState, state ) {
  var geoName = state.geo.name;
  var includeComparison = state.includeComparison;
  if ( geoName ) {
    utils.showEl( this.$chartTitle );
    this.$chartTitleGeo.innerText = geoName;
  } else {
    this.$chartTitleGeo.innerText = 'national average';
  }
  if ( includeComparison ) {
    utils.showEl( this.$chartTitleComparison );
  } else {
    utils.hideEl( this.$chartTitleComparison );
  }
};

MortgagePerformanceLineChart.prototype.renderCounties = function( prevState, state ) {
  this.$county.disabled = state.isLoadingCounties;
  if ( JSON.stringify( prevState.counties ) === JSON.stringify( state.counties ) ) {
    return;
  }
  state.counties.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
  var fragment = document.createDocumentFragment();
  state.counties.forEach( county => {
    var option = document.createElement( 'option' );
    option.value = county.fips;
    option.text = county.name;
    fragment.appendChild( option );
  } );
  this.$county.innerHTML = '';
  this.$county.appendChild( fragment );
};

MortgagePerformanceLineChart.prototype.renderMetros = function( prevState, state ) {
  this.$metro.disabled = state.isLoadingMetros;
  if ( JSON.stringify( prevState.metros ) === JSON.stringify( state.metros ) ) {
    return;
  }
  state.metros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
  var fragment = document.createDocumentFragment();
  state.metros.forEach( metro => {
    var option = document.createElement( 'option' );
    option.value = metro.fips;
    option.text = metro.name;
    fragment.appendChild( option );
  } );
  this.$metro.innerHTML = '';
  this.$metro.appendChild( fragment );
};

MortgagePerformanceLineChart.prototype.renderNonMetros = function( prevState, state ) {
  this.$nonMetro.disabled = state.isLoadingNonMetros;
  if ( JSON.stringify( prevState.nonMetros ) === JSON.stringify( state.nonMetros ) ) {
    return;
  }
  state.nonMetros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
  var fragment = document.createDocumentFragment();
  state.nonMetros.forEach( nonMetro => {
    var option = document.createElement( 'option' );
    option.value = nonMetro.fips;
    option.text = nonMetro.name;
    fragment.appendChild( option );
  } );
  this.$nonMetro.innerHTML = '';
  this.$nonMetro.appendChild( fragment );
};

module.exports = MortgagePerformanceLineChart;
