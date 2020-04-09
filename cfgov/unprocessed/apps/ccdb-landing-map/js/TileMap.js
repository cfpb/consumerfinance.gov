import * as d3 from 'd3';
import Highcharts from 'highcharts/highmaps';
import { STATE_TILES } from './constants';
import accessibility from 'highcharts/modules/accessibility';
import moment from 'moment';

const TEN_K = 10000;
const HUN_K = 100000;
const MILLION = 1000000;

const WHITE = '#ffffff';

/**
 * helper function to get date interval for legend
 * @returns {string} formatted string
 */
export function calculateDateInterval() {
  let today = new Date();
  today = today.toLocaleDateString( 'en-US' );
  let past = new Date( moment().subtract( 3, 'years' ).calendar() );
  past = past.toLocaleDateString( 'en-US' );
  return past + ' - ' + today;
}

/* ----------------------------------------------------------------------------
   Utility Functions */
/**
 * Creates N evenly spaced ranges in the data
 *
 * @param {Array} data all of the states w/ displayValue, complaintCount, raw
 * @param {Array} colors an array of colors
 * @returns {Array} floating point numbers that mark the max of each range
 */
export function makeScale( data, colors ) {
  const allValues = data.map( x => x.displayValue )
  const uniques = new Set( allValues )

  let scale = d3.scaleQuantile().range( [ WHITE, ...colors ] )
  // This catches the condition where all the complaints are in one state
  if ( uniques.size < colors.length ) {
    scale = scale.domain( [ ...uniques ] )
  } else {
    scale = scale.domain( allValues )
  }

  return scale
}

/**
 * Creates a shorter version of a number. 1,234 => 1.2K
 *
 * @param {Number} value the raw value
 * @returns {string} A string representing a shortened value
 */
export function makeShortName( value ) {
  if ( value < 1000 ) {
    return value.toLocaleString();
  } else if ( value < TEN_K ) {
    return ( Math.floor( value / 100 ) / 10 ).toFixed( 1 ) + 'K'
  } else if ( value < MILLION ) {
    return Math.floor( value / 1000 ) + 'K'
  }

  return ( Math.floor( value / HUN_K ) / 10 ).toFixed( 1 ) + 'M'
}


/**
 * helper function to get the bins for legend and colors, etc.
 *
 * @param {Array} quantiles floats that mark the max of each range
 * @param {Function} scale scaling function for color
 * @returns {Array} the bins with bounds, name, and color
 */
export function getBins( quantiles, scale ) {
  const rounds = quantiles.map( x => Math.round( x ) )
  const ceils = quantiles.map( x => Math.ceil( x ) )
  const mins = Array.from( new Set( rounds ) ).filter( x => x > 0 )

  const bins = [
    { from: 0, color: WHITE, name: '≥ 0', shortName: '≥ 0' }
  ];

  mins.forEach( minValue => {
    // The color is the equivalent ceiling from the floor
    const i = rounds.indexOf( minValue )

    const prefix = ceils[i] === minValue ? '≥' : '>'
    const displayValue = minValue.toLocaleString();
    const shortened = makeShortName( minValue )

    bins.push( {
      from: minValue,
      color: scale( ceils[i] ),
      name: `${ prefix } ${ displayValue }`,
      shortName: `${ prefix } ${ shortened }`
    } );
  } )

  return bins
}


/**
 * helper function to get the Per 1000 population bins for legend and colors
 *
 * @param {Array} quantiles floats that mark the max of each range
 * @param {Function} scale scaling function for color
 * @returns {Array} the bins with bounds, name, and color
 */
export function getPerCapitaBins( quantiles, scale ) {
  const trunc100 = x => Math.floor( x * 100 ) / 100

  const values = quantiles.map( x => trunc100( x ) )
  const mins = Array.from( new Set( values ) ).filter( x => x > 0 )

  const bins = [
    { from: 0, color: WHITE, name: '≥ 0', shortName: '≥ 0' }
  ];

  mins.forEach( minValue => {
    // The color is the equivalent quantile
    const i = values.indexOf( minValue )

    const prefix = values[i] === quantiles[i] ? '≥' : '>'
    const displayValue = minValue.toFixed( 2 );
    const name = `${ prefix } ${ displayValue }`
    bins.push( {
      from: minValue,
      color: scale( quantiles[i] ),
      name,
      shortName: name
    } );
  } )

  return bins
}

/* ----------------------------------------------------------------------------
   Utility Functions 2 */
/**
 * @param {Object} data - Data to process. add in state paths to the data obj
 * @param {Function} scale - contains different buckets for the values
 * @returns {Object} The processed data.
 */
export function processMapData( data, scale ) {
  // Filter out any empty values just in case
  data = data.filter( function( row ) {
    return Boolean( row.name );
  } );

  data = data.map( function( obj ) {
    const color = getColorByValue( obj.displayValue, scale );
    if ( color === WHITE ) {
      obj.className = 'empty';
    }
    return {
      ...obj,
      color,
      path: STATE_TILES[obj.name]
    };
  } );

  return data;
}

/**
 * helper function to set the color.
 *
 * Highcharts could normally handle it, but it gets confused by values
 * less than 1 that are frequently encountered in perCapita
 *
 * Also, walk through the array backwards to pick up the most saturated
 * color. This helps the "only three values" case
 *
 * @param {number} value the number of complaints or perCapita
 * @param {Function} scale scaling function for color
 * @returns {string} color hex or rgb code for a color
 */
export function getColorByValue( value, scale ) {
  if ( !value ) return WHITE

  return scale( value );
}

/* ----------------------------------------------------------------------------
   Highcharts callbacks */
/**
 * callback function for reporting the series point in a voiceover text
 *
 * @param {Object} p the point in the series
 * @returns {string} the text to speak
 */
export function pointDescriptionFormatter( p ) {
  return `${ p.fullName } ${ p.displayValue }`
}

/**
 * handles the click action for the tile map
 * @param {boolean} isPerCapita determines if it is a percapita value
 * @param {object} t the highchart element containing point, and other props
 */
export function clickHandler( isPerCapita, t ) {
  let capText = 'dataNormalization=';
  capText += isPerCapita ? 'Per%201000%20pop.' : 'None';
  const stateUrl = 'search/?dateInterval=3y&' + capText +
    '&state=' + t.point.name;
  const loc = location.protocol + '//' + location.host + location.pathname;
  location.assign( loc + stateUrl );
}

/**
 * callback function for mouseout a point to remove hover class from tile label
 */
export function mouseoutPoint() {
  const name = '.tile-' + this.name;
  d3.select( name ).classed( 'hover', false );
}

/**
 * callback function for mouseover point to add hover class to tile label
 */
export function mouseoverPoint() {
  const name = '.tile-' + this.name;
  d3.select( name ).classed( 'hover', true );
}

/**
 * callback function to format the individual tiles in HTML
 * @returns {string} html output
 */
export function tileFormatter() {
  const value = this.point.displayValue.toLocaleString();
  return '<div class="highcharts-data-label-state tile-' + this.point.name +
    ' ">' +
    '<span class="abbr">' + this.point.name + '</span>' +
    '<br />' +
    '<span class="value">' + value + '</span>' +
    '</div>';
}

/**
 * callback function to format the tooltip in HTML
 * @returns {string} html output
 */
export function tooltipFormatter() {
  const product = this.product ? '<div class="row u-clearfix">' +
    '<p class="u-float-left">Product with highest complaint volume</p>' +
    '<p class="u-right">' + this.product + '</p>' +
    '</div>' : '';

  const issue = this.issue ? '<div class="row u-clearfix">' +
    '<p class="u-float-left">Issue with highest complaint volume</p>' +
    '<p class="u-right">' + this.issue + '</p>' +
    '</div>' : '';

  const value = this.value.toLocaleString();
  const perCapita = this.perCapita ? '<div class="row u-clearfix">' +
    '<p class="u-float-left">Per 1000 population</p>' +
    '<p class="u-right">' + this.perCapita + '</p>' +
    '</div>' : '';

  return '<div class="title">' + this.fullName + '</div>' +
    '<div class="row u-clearfix">' +
    '<p class="u-float-left">Complaints</p>' +
    '<p class="u-right">' + value + '</p>' +
    '</div>' +
    perCapita +
    product +
    issue;
}

/**
 * Draw a legend on a chart.
 * @param {Object} chart A highchart chart.
 */
// eslint-disable-next-line max-lines-per-function, require-jsdoc
export function _drawLegend( chart ) {
  const bins = chart.options.bins;
  const marginTop = chart.margin[0] || 0;
  const boxWidth = 50;
  const boxHeight = 15;
  const boxPadding = 1;

  /* https://api.highcharts.com/class-reference/Highcharts.SVGRenderer#label
     boxes and labels for legend buckets */
  // main container
  const legendContainer = chart.renderer.g( 'legend-container' )
    .translate( 10, marginTop )
    .add();

  const legendText = chart.renderer.g( 'legend-title' )
    .translate( boxPadding, 0 )
    .add( legendContainer );
  // key
  chart.renderer
    .label( 'Key', 0, 0, null, null, null, true, false, 'legend-key' )
    .add( legendText );

  // horizontal separator line
  chart.renderer.path( [ 'M', 0, 0, 'L', bins.length * ( boxWidth + boxPadding ), 0 ] )
    .attr( {
      'class': 'separator',
      'stroke-width': 1,
      'stroke': 'gray'
    } )
    .translate( 0, 25 )
    .add( legendText );

  // what legend represents
  const labelTx = 'Map shading: <span class="type">' +
    chart.options.legend.legendTitle + '</span>';
  chart.renderer
    .label( labelTx, 0, 28, null, null, null, true, false, 'legend-description' )
    .add( legendText );

  const labelDates = `Dates: <span class="type">${ calculateDateInterval() }` +
    '</span>';
  chart.renderer
    .label( labelDates, 0, 44, null, null, null, true, false, 'legend-dates' )
    .add( legendText );

  // bars
  const legend = chart.renderer.g( 'legend__tile-map' )
    .translate( 3, 64 )
    .add( legendContainer );

  for ( let i = 0; i < bins.length; i++ ) {
    const g = chart.renderer.g( `g${ i }` )
      .translate( i * ( boxWidth + boxPadding ), 0 )
      .add( legend );

    const bin = bins[i];

    chart.renderer
      .rect( 0, 0, boxWidth, boxHeight )
      .attr( { fill: bin.color } )
      .addClass( 'legend-box' )
      .add( g );

    chart.renderer
      .text( bin.name, 2, boxHeight - 2 )
      .addClass( 'legend-text' )
      .add( g );
  }
}

/* ----------------------------------------------------------------------------
   Tile Map class */

accessibility( Highcharts );

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );

const colors = [
  'rgba(212, 231, 230, 1)',
  'rgba(180, 210, 209, 1)',
  'rgba(158, 196, 195, 1)',
  'rgba(137, 182, 181, 1)',
  'rgba(112, 166, 165, 1)',
  'rgba(87, 150, 149, 1)'
];

/* ----------------------------------------------------------------------------
   Tile Map class */
class TileMap {
  // eslint-disable-next-line max-lines-per-function
  constructor( { el, data, isPerCapita } ) {
    const scale = makeScale(data, colors);
    const quantiles = scale.quantiles();

    let bins, legendTitle;

    if (isPerCapita) {
      bins = getPerCapitaBins(quantiles, scale);
      legendTitle = 'Complaints per 1,000';
    } else {
      bins = getBins(quantiles, scale);
      legendTitle = 'Complaints';
    }

    data = processMapData( data, scale );

    const options = {
      bins,
      chart: {
        styledMode: true
      },
      colors,
      colorAxis: {
        dataClasses: bins,
        dataClassColor: 'category'
      },
      title: false,
      credits: false,
      legend: {
        enabled: false,
        legendTitle
      },
      tooltip: {
        className: 'tooltip',
        enabled: true,
        headerFormat: '',
        pointFormatter: tooltipFormatter,
        useHTML: true
      },
      plotOptions: {
        series: {
          dataLabels: {
            enabled: true,
            formatter: tileFormatter,
            useHTML: true
          },
          events: {
            click: clickHandler.bind( this, isPerCapita )
          },
          point: {
            events: {
              mouseOver: mouseoverPoint,
              mouseOut: mouseoutPoint
            }
          }
        }
      },

      series: [ {
        type: 'map',
        clip: false,
        data: data,
        accessibility: {
          description: legendTitle + ' in the United States',
          exposeAsGroupOnly: false,
          keyboardNavigation: { enabled: true },
          pointDescriptionFormatter: pointDescriptionFormatter
        }
      } ]
    };

    this.draw( el, options );
  }

  draw( el, options ) {
    Highcharts.mapChart( el, options, _drawLegend );
  }
}

export default TileMap;
