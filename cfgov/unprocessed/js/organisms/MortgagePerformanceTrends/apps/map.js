'use strict';

const ccb = require( 'cfpb-chart-builder' );
const actions = require( '../actions' );
const Store = require( '../stores/map' );
const utils = require( '../utils' );

const store = new Store( [ utils.thunkMiddleware, utils.loggerMiddleware ] );

const _plurals = {
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
  let abbr, action, geoType, geoId, geoName, date;

  abbr = this.$state.options[this.$state.selectedIndex].getAttribute( 'data-abbr' );
  geoType = this.$container.querySelector( 'input[name="mp-map_geo"]:checked' ).id.replace( 'mp-map_geo-', '' );

  switch ( event.target.id ) {
    case 'mp-map_geo-state':
    case 'mp-map_geo-metro':
    case 'mp-map_geo-county':
      geoId = '';
      geoName = '';
      action = actions.updateChart( geoId, geoName, geoType );
      // If a state has been pre-selected, populate the metros dropdown
      if ( abbr && geoType === 'metro' ) {
        store.dispatch( actions.fetchMetros( abbr ) );
      }
      // If a state has been pre-selected, populate the counties dropdown
      if ( abbr && geoType === 'county' ) {
        store.dispatch( actions.fetchCounties( abbr ) );
      }
      break;
    case 'mp-map-state':
      if ( geoType === 'metro' || geoType === 'county' ) {
        // If no state is selected, zoom out and abort
        if ( !abbr ) {
          this.chart.highchart.chart.zoomOut();
          action = actions.updateChart( '', '', geoType );
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
      if ( !geoId ) {
        action = actions.updateChart( '', '' );
        break;
      }
      geoName = this.$metro.options[this.$metro.selectedIndex].text;
      action = actions.updateChart( geoId, geoName );
      break;
    case 'mp-map-county':
      geoId = this.$county.value;
      if ( !geoId ) {
        action = actions.updateChart( '', '' );
        break;
      }
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
  const prevType = prevState.geo.type;
  const currType = state.geo.type;
  const prevId = prevState.geo.id;
  const currId = state.geo.id;
  let zoomLevel;
  if ( prevId && prevId !== currId ) {
    this.chart.highchart.chart.get( prevId ).select( false );
  }
  if ( prevState.date === state.date && prevType === currType && currId ) {
    // Highcharts zooming is unreliable and difficult to customize :(
    // http://api.highcharts.com/highmaps/Chart.mapZoom
    // If it's a state or non-metro, zoom in more than other location types
    zoomLevel = currType === 'state' || utils.isNonMetro( currId ) ? 5 : 10;
    this.chart.highchart.chart.get( currId ).select( true );
    this.chart.highchart.chart.get( currId ).zoomTo();
    this.chart.highchart.chart.mapZoom( zoomLevel );
  }
  if ( state.zoomTarget ) {
    let centroid = utils.stateCentroids[state.zoomTarget];
    this.chart.highchart.chart.mapZoom( utils.calcZoomLevel( 5 ), centroid[0], centroid[1] );
  }
  // If no geo is selected, ensure metro and county dropdowns are cleared
  if ( !currId || prevType !== currType ) {
    this.$metro.value = '';
    this.$metro.innerHTML = '';
    this.$county.value = '';
    this.$county.innerHTML = '';
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
  let option;
  this.$county.disabled = state.isLoadingCounties;
  if ( JSON.stringify( state.counties ) === JSON.stringify( {} ) ) {
    return;
  }
  state.counties.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
  const fragment = document.createDocumentFragment();
  option = utils.addOption( {
    document,
    value: '',
    text: 'Please select a county'
  } );
  fragment.appendChild( option );
  state.counties.forEach( county => {
    option = utils.addOption( {
      document,
      value: county.fips,
      text: county.name
    } );
    fragment.appendChild( option );
  } );
  this.$county.innerHTML = '';
  this.$county.appendChild( fragment );
};

MortgagePerformanceMap.prototype.renderMetros = function( prevState, state ) {
  let option;
  this.$metro.disabled = state.isLoadingMetros;
  if ( JSON.stringify( state.metros ) === JSON.stringify( {} ) ) {
    return;
  }
  state.metros.sort( ( a, b ) => {
    // Alphabetize location names except for non-metros, keep them at the bottom
    if ( a.name < b.name && !utils.isNonMetro( a.fips ) ) {
      return -1;
    }
    return 1;
  } );
  const fragment = document.createDocumentFragment();
  option = utils.addOption( {
    document,
    value: '',
    text: 'Please select an area'
  } );
  fragment.appendChild( option );
  state.metros.forEach( metro => {
    option = document.createElement( 'option' );
    option = utils.addOption( {
      document,
      value: metro.fips,
      text: metro.name
    } );
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
