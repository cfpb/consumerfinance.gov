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
      action = actions.setGeo( geoId, geoName, geoType );
      break;
    case 'mp-map-state':
      geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );
      if ( geoType === 'metro' || geoType === 'county' ) {
        abbr = this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' );
        // If no state is selected, zoom out and abort
        if ( !abbr ) {
          this.chart.highchart.chart.zoomOut();
          action = actions.setGeo( '', '', geoType );
          break;
        }
      }
      if ( geoType === 'metro' ) {
        action = actions.fetchMetros( abbr );
        break;
      }
      if ( geoType === 'county' ) {
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
  let zoomLevel;
  const prevType = prevState.geo.type;
  const currType = state.geo.type;
  const prevId = prevState.geo.id;
  const currId = state.geo.id;
  if ( prevState.geo.id && prevState.geo.id !== state.geo.id ) {
    this.chart.highchart.chart.get( prevState.geo.id ).select( false );
  }
  if ( prevState.date === state.date && prevType === currType && state.geo.id ) {
    // Highcharts zooming is unreliable and difficult to customize :(
    // http://api.highcharts.com/highmaps/Chart.mapZoom
    // If it's a state or non-metro, zoom in more than other location types
    zoomLevel = currType === 'state' || utils.isNonMetro( state.geo.id ) ? 5 : 10;
    this.chart.highchart.chart.get( state.geo.id ).select( true );
    this.chart.highchart.chart.get( state.geo.id ).zoomTo();
    this.chart.highchart.chart.mapZoom( zoomLevel );
  }
  // If no geo is selected, ensure metro and county dropdowns are cleared
  if ( !currId || prevType !== currType ) {
    this.$metro.value = '';
    this.$metro.innerHTML = '';
    this.$county.value = '';
    this.$county.innerHTML = '';
  }
  // If the geo type was changed, ensure the state dropdown is cleared as well
  if ( prevType !== currType ) {
    this.$state.value = '';
  }
  if ( prevState.date !== state.date || prevType !== currType ) {
    store.dispatch( actions.startLoading() );
    this.chart.update( {
      source: `map-data/${ this.timespan }/${ _plurals[currType] }/${ state.date }`,
      metadata: _plurals[currType],
      tooltipFormatter: this.renderTooltip()
    } ).then( () => {
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
  state.metros.sort( ( a, b ) => {
    // Alphabetize location names except for non-metros, keep them at the bottom
    if ( a.name < b.name && !utils.isNonMetro( a.fips ) ) {
      return -1;
    }
    return 1;
  } );
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
    var percent;
    var nationalPercent = Math.round( meta.national_average * 1000 ) / 10;
    if ( point.value === null ) {
      return "<div class='m-mp-map-tooltip'>Insufficient data for this area</div>";
    }
    if ( point.value < 0 ) {
      percent = 'Insufficient data';
    } else {
      percent = Math.round( point.value * 10 ) / 10;
      percent = `<strong>${ percent }%</strong> mortgage delinquency rate`;
    }
    return `<dl class='m-mp-map-tooltip'>
      <dt>${ point.name }</dt>
      <dd>${ percent }</dd>
      <dd><strong>${ nationalPercent }%</strong> national average</dd>
    </dl>`;
  };
};

module.exports = MortgagePerformanceMap;
