// import TileMap from 'cfpb-chart-builder/src/js/charts/TileMap';

import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import getTileMapState from 'cfpb-chart-builder/src/js/utils/get-tile-map-state';

/* ----------------------------------------------------------------------------
   Utility Functions */
/**
* A reducer function to process the maximum value in the state complaint data
*
* @param {number} accum the current max value
* @param {Object} stateComplaint a candidate value
* @returns {string} the maximum between the current and a state entry
*/
function findMaxComplaints( accum, stateComplaint ) {
  return Math.max( accum, stateComplaint.displayValue );
}

/**
 * helper function to get the bins for legend and colors, etc.
 * @param {Array} data all of the states w/ displayValue, complaintCount, raw
 * @param {Array} colors an array of colors
 * @returns {Array} the bins with bounds, name, and color
 */
function getBins( data, colors ) {
  const binCount = colors.length;
  const max = data.reduce( findMaxComplaints, 0 );
  const min = 1;

  // Early exit
  if ( max === 0 ) return [];

  const bins = [];
  const step = ( max - min + 1 ) / binCount;

  for ( let i = 0, curr = min; i < binCount; i++, curr += step ) {
    const minValue = Math.round( curr );
    const displayValue = Math.round( curr / 1000 );

    bins.push( {
      from: minValue,
      to: Math.round( curr + step ),
      color: colors[i],
      name: displayValue > 0 ? `≥ ${ displayValue }K` : '≥ 0'
    } );
  }

  // The last bin is unbounded
  // eslint-disable-next-line no-undefined
  bins[binCount - 1].to = undefined;

  return bins;
}

/**
 * helper function to get the per Capita bins for legend and colors, etc.
 * @param {Array} data all of the states w/ displayValue, complaintCount, raw
 * @param {Array} colors an array of colors
 * @returns {Array} contains bins with bounds, colors, name, and color
 */
function getPerCapitaBins( data, colors ) {
  const binCount = colors.length;
  const max = data.reduce( findMaxComplaints, 0 );
  const min = 1;

  // Early exit
  if ( max === 0 ) return [];

  const step = ( max - min ) / binCount;
  const bins = [ { from: 0, to: step, color: '#fff', name: '>0' } ];

  for ( let i = 0, curr = min; i < binCount; i++, curr += step ) {
    curr = parseFloat( curr.toFixed( 2 ) );
    const minValue = curr;
    const displayValue = curr;
    bins.push( {
      from: minValue,
      to: parseFloat( ( curr + step ).toFixed( 2 ) ),
      color: colors[i],
      name: displayValue > 0 ? `≥ ${ displayValue }` : '≥ 0'
    } );
  }

  // The last bin is unbounded
  // eslint-disable-next-line no-undefined
  bins[binCount - 1].to = undefined;

  console.log( bins );

  return bins;
}

/* ----------------------------------------------------------------------------
   Utility Functions 2 */
/**
 * @param {Object} data - Data to process. add in state paths to the data obj
 * @param {Array} bins - contains different buckets for the values
 * @returns {Object} The processed data.
 */
function processMapData( data, bins ) {
  // Filter out any empty values just in case
  data = data.filter( function( row ) {
    return Boolean( row.name );
  } );

  data = data.map( function( obj ) {
    const state = getTileMapState[obj.name];
    return {
      ...obj,
      color: getColorByValue( obj.displayValue, bins ),
      path: state.path
    };
  } );

  return data;
}

/**
 * helper function to search color in the bins
 * @param {number} value the number of complaints or perCapita
 * @param {array} bins contains bin objects
 * @returns {string} color hex or rgb code for a color
 */
function getColorByValue( value, bins ) {
  let color = '#ffffff';
  for ( let i = 0; i < bins.length; i++ ) {
    if ( value > bins[i].from ) {
      color = bins[i].color;
    }
  }
  return color;
}

/* ----------------------------------------------------------------------------
   Highcharts callbacks */

/**
 * Draw a legend on a chart.
 * @param {Object} chart A highchart chart.
 */
function _drawLegend( chart ) {
  const bins = chart.options.bins;

  const marginTop = chart.margin[0] || 0;
  const boxWidth = 50;
  const boxHeight = 15;
  const boxPadding = 1;

  /* args: (str, x, y, shape, anchorX, anchorY, useHTML, baseline, className)
     const labelTx = 'Map shading: Complaints';
     chart.renderer
       .label( labelTx, 5, 5, null, null, null, true, false, 'label__tile-map' )
       .add(); */
  /* https://api.highcharts.com/class-reference/Highcharts.SVGRenderer#label
     boxes and labels for legend buckets */
  const legend = chart.renderer.g( 'legend__tile-map' )
    .translate( 10, marginTop )
    .add();

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

/**
 * callback function to format the individual tiles in HTML
 * @returns {string} html output
 */
function tileFormatter() {
  const value = this.point.displayValue.toLocaleString();
  return '<div class="highcharts-data-label-state">' +
    '<span class="abbr">' + this.point.name + '</span>' +
    '<br />' +
    '<span class="value">' + value + '</span>' +
    '</div>';
}

/**
 * callback function to format the tooltip in HTML
 * @returns {string} html output
 */
function tooltipFormatter() {
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
    '<p class="u-float-left">Per capita</p>' +
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

/* ----------------------------------------------------------------------------
   Tile Map class */

accessibility( Highcharts );

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );

const colors = [
  'rgba(247, 248, 249, 0.5)',
  'rgba(212, 231, 230, 0.5)',
  'rgba(180, 210, 209, 0.5)',
  'rgba(137, 182, 181, 0.5)',
  'rgba(86, 149, 148, 0.5)',
  'rgba(37, 116, 115, 0.5)'
];

/* ----------------------------------------------------------------------------
   Tile Map class */

class TileMap {
  constructor( { el, description, data, isPerCapita } ) {
    const bins = isPerCapita ?
      getPerCapitaBins( data, colors ) : getBins( data, colors );
    data = processMapData( data, bins );

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
      description: description,
      credits: false,
      legend: {
        enabled: false
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
          }
        }
      },

      series: [ {
        type: 'map',
        clip: false,
        data: data
      } ]
    };

    return Highcharts.mapChart( el, options, _drawLegend );
  }
}

export default TileMap;
