'use strict';

var ccb = require( 'cfpb-chart-builder-canary' );
var actions = require( '../actions' );
var Store = require( '../stores/map' );
var utils = require( '../utils' );

var store = new Store( [ utils.thunkMiddleware, utils.loggerMiddleware ] );

var _plurals = {
  state: 'states',
  metro: 'metros',
  county: 'counties'
};

function MortgagePerformanceMap( { container } ) {
  this.$container = document.getElementById( container );
  this.$form = this.$container.querySelector( '#mp-map-controls' );
  this.$geo = this.$container.querySelector( '#mp-map-geo' );
  this.$state = this.$container.querySelector( '#mp-map-state' );
  this.$metro = this.$container.querySelector( '#mp-map-metro' );
  this.$countyState = this.$container.querySelector( '#mp-map-county-state' );
  this.$county = this.$container.querySelector( '#mp-map-county' );
  this.$month = this.$container.querySelector( '#mp-map-month' );
  this.$year = this.$container.querySelector( '#mp-map-year' );
  this.$map = this.$container.querySelector( '#mp-map' );
  this.$mapTitle = document.querySelector( '#mp-map-title-status' );
  this.$mapTitleDate = document.querySelector( '#mp-map-title-date' );
  this.$loadingSpinner = document.querySelector( '#mp-map-loading' );
  this.timespan = this.$container.getAttribute( 'data-chart-time-span' );
  this.chart = ccb.createChart( {
    el: this.$container.querySelector( '#mp-map' ),
    source: `map-data/${ this.timespan }/states/2009-01`,
    type: 'geo-map',
    metadata: 'states'
  } );
  this.eventListeners();
  utils.hideEl( this.$loadingSpinner );
}

MortgagePerformanceMap.prototype.eventListeners = function() {
  this.$form.addEventListener( 'change', this.onChange.bind( this ) );
  store.subscribe( this.renderChart.bind( this ) );
  store.subscribe( this.renderChartTitle.bind( this ) );
  store.subscribe( this.renderChartForm.bind( this ) );
  store.subscribe( this.renderCounties.bind( this ) );
};

MortgagePerformanceMap.prototype.onClick = function( event ) {
  var change = new Event( 'change' );
  this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).checked = false;
  this.$form.dispatchEvent( change );
  event.preventDefault();
};

MortgagePerformanceMap.prototype.onChange = function( event ) {
  var action, geoEl, geoType, geoId, geoName, countyState, date;

  switch ( event.target.id ) {
    case 'mp-map_geo-state':
    case 'mp-map_geo-metro':
    case 'mp-map_geo-county':
      geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );
      geoId = '';
      geoName = '';
      action = actions.setGeo( geoId, geoName, geoType );
      break;
    case 'mp-map-state':
      geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );
      if ( geoType === 'state' ) {
        geoId = this.$state.value;
        geoName = this.$state.options[this.$state.selectedIndex].text;
        action = actions.updateChart( geoId, geoName, geoType );
      } else {
        var abbr = this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' );
        if ( !abbr ) {
          return this.chart.highchart.chart.zoomOut();
        }
        action = actions.fetchCounties( abbr );
      }
      break;
    case 'mp-map-metro':
      geoId = this.$metro.value;
      geoName = this.$metro.options[this.$metro.selectedIndex].text;
      action = actions.updateChart( geoId, geoName );
      break;
    case 'mp-map-county':
      geoId = this.$county.value;
      geoName = this.$county.options[this.$county.selectedIndex].text;
      action = actions.updateChart( geoId, geoName );
      break;
    case 'mp-map-month':
    case 'mp-map-year':
      date = `${ this.$year.value }-${ this.$month.value }`;
      action = actions.updateDate( date );
      break;
    default:
      action = actions.clearGeo();
  }

  return store.dispatch( action );

};

MortgagePerformanceMap.prototype.zoom = function( prevState, state ) {
  this.chart.highchart.chart.get( state.geo.id ).zoomTo();
};

MortgagePerformanceMap.prototype.renderChart = function( prevState, state ) {
  if ( !state.geo.id ) {
    this.chart.highchart.chart.zoomOut();
  }
  if ( prevState.date === state.date && prevState.geo.type === state.geo.type && state.geo.id ) {
    this.chart.highchart.chart.get( state.geo.id ).select();
    this.chart.highchart.chart.get( state.geo.id ).zoomTo();
    this.chart.highchart.chart.mapZoom( 5 );
  }
  if ( prevState.date !== state.date || prevState.geo.type !== state.geo.type ) {
    store.dispatch( actions.startLoading() );
    this.chart.update( {
      source: `map-data/${ this.timespan }/${ _plurals[state.geo.type] }/${ state.date }`,
      metadata: _plurals[state.geo.type]
    } ).then( () => {
      this.$state.value = '';
      this.$metro.value = '';
      this.$county.value = '';
      this.$county.innerHTML = '';
      this.chart.highchart.chart.zoomOut();
      store.dispatch( actions.stopLoading() );
    } );
  }
};

MortgagePerformanceMap.prototype.renderChartForm = function( prevState, state ) {
  // If we're waiting for data, abort.
  if ( state.isLoading ) {
    return utils.showEl( this.$loadingSpinner );
  }
  utils.hideEl( this.$loadingSpinner );
  // If counties aren't being loaded and the geo type hasn't changed, nothing to do here.
  if ( !state.isLoadingCounties && prevState.geo.type === state.geo.type ) {
    return false;
  }
  var geoType;
  if ( state.isLoadingCounties ) {
    geoType = 'county';
  } else {
    geoType = state.geo.type;
  }
  var geo = this.$container.querySelector( `#mp-map-${ geoType }-container` );
  var containers = this.$container.querySelectorAll( '.mp-map-select-container' );
  for ( var i = 0; i < containers.length; ++i ) {
    utils.hideEl( containers[i] );
  }
  if ( geoType === 'county' ) {
    utils.showEl( this.$container.querySelector( '#mp-map-state-container' ) );
  }
  if ( !state.geo.type ) {
    return this.chart.highchart.chart.zoomOut();
  }
  return utils.showEl( geo );
};

MortgagePerformanceMap.prototype.renderChartTitle = function( prevState, state ) {
  this.$mapTitleDate.innerHTML = utils.getDate( state.date );
};

MortgagePerformanceMap.prototype.renderCounties = function( prevState, state ) {
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

module.exports = MortgagePerformanceMap;
