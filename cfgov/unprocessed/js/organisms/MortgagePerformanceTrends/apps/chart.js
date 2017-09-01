'use strict';

var ccb = require( 'cfpb-chart-builder-canary' );
var actions = require( '../actions' );
var Store = require( '../stores/chart' );
var utils = require( '../utils' );

var store = new Store( [ utils.thunkMiddleware, utils.loggerMiddleware ] );

class MortgagePerformanceLineChart {
  constructor( { container } ) {
    this.$container = document.getElementById( container );
    this.$form = this.$container.querySelector( '#mp-line-chart-controls' );
    this.$geo = this.$container.querySelector( '#mp-line-chart-geo' );
    this.$state = this.$container.querySelector( '#mp-line-chart-state' );
    this.$metro = this.$container.querySelector( '#mp-line-chart-metro' );
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
};

MortgagePerformanceLineChart.prototype.onClick = function( event ) {
  var change = new Event( 'change' );
  this.$container.querySelector( 'input[name="mp-line-chart_geo"]:checked' ).checked = false;
  this.$form.dispatchEvent( change );
  event.preventDefault();
};

MortgagePerformanceLineChart.prototype.onChange = function( event ) {

  var action, geoEl, geoType, geoId, geoName;
  var includeNational = this.$compare.checked;

  switch ( event.target.id ) {
    case 'mp-line-chart_geo-state':
    case 'mp-line-chart_geo-metro':
      // Reset the county dropdown to the first item if we're no longer using it
      this.$county.selectedIndex = 0;
      geoType = this.$container.querySelector( 'input[name="mp-line-chart_geo"]:checked' ).id.replace( 'mp-line-chart_geo-', '' );
      geoEl = this['$' + geoType];
      geoId = geoEl.value;
      geoName = geoEl.options[geoEl.selectedIndex].text;
      action = actions.setGeo( geoId, geoName, geoType );
      break;
    case 'mp-line-chart_geo-county':
      action = actions.fetchCounties( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ) );
      break;
    case 'mp-line-chart-state':
      geoType = this.$container.querySelector( 'input[name="mp-line-chart_geo"]:checked' ).id.replace( 'mp-line-chart_geo-', '' );
      if ( geoType === 'state' ) {
        geoId = this.$state.value;
        geoName = this.$state.options[this.$state.selectedIndex].text;
        action = actions.updateChart( geoId, geoName, 'state', includeNational );
      } else {
        geoId = this.$county.value;
        geoName = this.$county.options[this.$county.selectedIndex].text;
        action = actions.fetchCounties( this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' ), includeNational );
      }
      break;
    case 'mp-line-chart-metro':
      geoId = this.$metro.value;
      geoName = this.$metro.options[this.$metro.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, 'metro', includeNational );
      break;
    case 'mp-line-chart-county':
      geoId = this.$county.value;
      geoName = this.$county.options[this.$county.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, 'county', includeNational );
      break;
    case 'mp-line-chart-compare':
      action = actions.updateNational( includeNational );
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
  if ( prevState.geo.id === state.geo.id && prevState.includeNational === state.includeNational ) {
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
  if ( state.includeNational ) {
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
  } else {
    geoType = state.geo.type;
  }
  var geo = this.$container.querySelector( `#mp-line-chart-${ geoType }-container` );
  var containers = this.$container.querySelectorAll( '.mp-line-chart-select-container' );
  for ( var i = 0; i < containers.length; ++i ) {
    utils.hideEl( containers[i] );
  }
  if ( geoType === 'county' ) {
    utils.showEl( this.$container.querySelector( '#mp-line-chart-state-container' ) );
  }
  if ( state.geo.type ) {
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
  var includeNational = state.includeNational;
  if ( geoName ) {
    utils.showEl( this.$chartTitle );
    this.$chartTitleGeo.innerHTML = geoName;
  } else {
    utils.hideEl( this.$chartTitle );
  }
  if ( includeNational ) {
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
  state.counties.sort( ( a, b ) => a.county < b.county ? -1 : 1 );
  var fragment = document.createDocumentFragment();
  state.counties.forEach( county => {
    var option = document.createElement( 'option' );
    option.value = county.fips;
    option.text = county.county;
    fragment.appendChild( option );
  } );
  this.$county.innerHTML = '';
  this.$county.appendChild( fragment );
};

module.exports = MortgagePerformanceLineChart;
