'use strict';

var ccb = require( 'cfpb-chart-builder' );
var actions = require( '../actions' );
var Store = require( '../stores/map' );
var utils = require( '../utils' );

var store = new Store( [ utils.thunkMiddleware, utils.loggerMiddleware ] );

var _plurals = {
  state: 'states',
  metro: 'metros',
  county: 'counties'
};

class MortgagePerformanceMap {

  constructor( { container } ) {
    this.$container = document.getElementById( container );
    this.$form = this.$container.querySelector( '#mp-map-controls' );
    this.$geo = this.$container.querySelector( '#mp-map-geo' );
    this.$state = this.$container.querySelector( '#mp-map-state' );
    this.$metro = this.$container.querySelector( '#mp-map-metro' );
    this.$county = this.$container.querySelector( '#mp-map-county' );
    this.$month = this.$container.querySelector( '#mp-map-month' );
    this.$year = this.$container.querySelector( '#mp-map-year' );
    this.$map = this.$container.querySelector( '#mp-map' );
    this.$mapTitle = document.querySelector( '#mp-map-title-status' );
    this.$mapTitleLocation = document.querySelector( '#mp-map-title-location' );
    this.$mapTitleDate = document.querySelector( '#mp-map-title-date' );
    this.$loadingSpinner = document.querySelector( '#mp-map-loading' );
    this.timespan = this.$container.getAttribute( 'data-chart-time-span' );
    this.chart = ccb.createChart( {
      el: this.$container.querySelector( '#mp-map' ),
      source: `map-data/${ this.timespan }/states/2008-01`,
      type: 'geo-map',
      color: this.$container.getAttribute( 'data-chart-color' ),
      metadata: 'states',
      tooltipFormatter: this.renderTooltip()
    } );
    this.eventListeners();
    utils.hideEl( this.$loadingSpinner );
  }

}

MortgagePerformanceMap.prototype.eventListeners = function() {
  this.$form.addEventListener( 'change', this.onChange.bind( this ) );
  store.subscribe( this.renderChart.bind( this ) );
  store.subscribe( this.renderChartTitle.bind( this ) );
  store.subscribe( this.renderChartForm.bind( this ) );
  store.subscribe( this.renderCounties.bind( this ) );
  store.subscribe( this.renderMetros.bind( this ) );
};

MortgagePerformanceMap.prototype.onClick = function( event ) {
  var change = new Event( 'change' );
  this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).checked = false;
  this.$form.dispatchEvent( change );
  event.preventDefault();
};

MortgagePerformanceMap.prototype.onChange = function( event ) {
  var abbr, action, geoEl, geoType, geoId, geoName, countyState, date;

  switch ( event.target.id ) {
    case 'mp-map_geo-state':
    case 'mp-map_geo-metro':
    case 'mp-map_geo-county':
      geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );
      geoId = '';
      geoName = '';
      this.chart.highchart.chart.zoomOut();
      action = actions.setGeo( geoId, geoName, geoType );
      break;
    case 'mp-map-state':
      geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );
      if ( geoType === 'metro' ) {
        abbr = this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' );
        if ( !abbr ) {
          return this.chart.highchart.chart.zoomOut();
        }
        action = actions.fetchMetros( abbr );
        break;
      }
      if ( geoType === 'county' ) {
        abbr = this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' );
        if ( !abbr ) {
          return this.chart.highchart.chart.zoomOut();
        }
        action = actions.fetchCounties( abbr );
        break;
      }
      geoId = this.$state.value;
      geoName = this.$state.options[this.$state.selectedIndex].text;
      action = actions.updateChart( geoId, geoName, geoType );
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

MortgagePerformanceMap.prototype.renderChart = function( prevState, state ) {
  if ( !state.geo.id ) {
    this.chart.highchart.chart.zoomOut();
  }
  if ( prevState.date === state.date && prevState.geo.type === state.geo.type && state.geo.id ) {
    this.chart.highchart.chart.get( state.geo.id ).select( true );
    this.chart.highchart.chart.get( state.geo.id ).zoomTo();
    this.chart.highchart.chart.mapZoom( 5 );
  }
  if ( prevState.date !== state.date || prevState.geo.type !== state.geo.type ) {
    store.dispatch( actions.startLoading() );
    this.chart.update( {
      source: `map-data/${ this.timespan }/${ _plurals[state.geo.type] }/${ state.date }`,
      metadata: _plurals[state.geo.type],
      tooltipFormatter: this.renderTooltip()
    } ).then( () => {
      if ( prevState.geo.type !== state.geo.type ) {
        this.$state.value = '';
        this.$metro.value = '';
        this.$county.value = '';
        this.$county.innerHTML = '';
        this.chart.highchart.chart.zoomOut();
      }
      store.dispatch( actions.stopLoading() );
    } );
  }
};

MortgagePerformanceMap.prototype.renderChartForm = function( prevState, state ) {
  var geoType = state.geo.type;
  if ( state.isLoadingCounties ) {
    geoType = 'county';
  }
  if ( state.isLoadingMetros ) {
    geoType = 'metro';
  }
  var geo = this.$container.querySelector( `#mp-map-${ geoType }-container` );
  var containers = this.$container.querySelectorAll( '.mp-map-select-container' );
  for ( var i = 0; i < containers.length; ++i ) {
    utils.hideEl( containers[i] );
  }
  if ( geoType === 'county' || geoType === 'metro' ) {
    utils.showEl( this.$container.querySelector( '#mp-map-state-container' ) );
  }
  if ( !state.geo.type ) {
    return this.chart.highchart.chart.zoomOut();
  }
  if ( geo ) {
    utils.showEl( geo );
  }
  return geoType;
};

MortgagePerformanceMap.prototype.renderChartTitle = function( prevState, state ) {
  let loc = state.geo.name;
  if ( !loc ) {
    loc = `${ state.geo.type } view`;
  }
  this.$mapTitleLocation.innerText = loc;
  this.$mapTitleDate.innerText = utils.getDate( state.date );
};

MortgagePerformanceMap.prototype.renderCounties = function( prevState, state ) {
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

MortgagePerformanceMap.prototype.renderMetros = function( prevState, state ) {
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

MortgagePerformanceMap.prototype.renderTooltip = function() {
  return ( point, meta ) => {
    var percent = Math.round( point.value * 10 ) / 10;
    var nationalPercent = Math.round( meta.national_average * 1000 ) / 10;
    return `<dl class='m-mp-map-tooltip'>
      <dt>${ point.name }</dt>
      <dd><strong>${ percent }%</strong> mortgage delinquency rate</dd>
      <dd><strong>${ nationalPercent }%</strong> national average</dd>
    </dl>`;
  };
};

module.exports = MortgagePerformanceMap;
