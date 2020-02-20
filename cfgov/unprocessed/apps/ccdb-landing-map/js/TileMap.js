// import TileMap from 'cfpb-chart-builder/src/js/charts/TileMap';

import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import getTileMapState from 'cfpb-chart-builder/src/js/utils/get-tile-map-state';

// ----------------------------------------------------------------------------
// Utility Functions

/**
* A reducer function to process the maximum value in the state complaint data
*
* @param {number} accum the current max value
* @param {Object} stateComplaint a candidate value
* @returns {string} the maximum between the current and a state entry
*/
function findMaxComplaints( accum, stateComplaint ) {
  return Math.max( accum, stateComplaint.value );
}

/**
 * helper function to get the bins for legend and colors, etc.
 * @param data
 * @param {Array} colors an array of colors
 * @returns {[]|Array}
 */
function getBins( data, colors ) {
  const binCount = colors.length;
  const max = data.reduce( findMaxComplaints, 0 );
  const min = 1;

  // Early exit
  if ( max === 0 ) return [];

  const bins = [ { from: 0, to: 1, color: '#fff', name: 'N/A' } ];
  const step = ( max - min + 1 ) / binCount;

  for ( let i = 0, curr = min; i < binCount; i++, curr += step ) {
    const minValue = Math.round( curr );
    const displayValue = Math.round( curr/1000 );

    bins.push( {
      from: minValue,
      to: Math.round( curr + step ),
      color: colors[i],
      name: displayValue > 0 ? `≥ ${ displayValue }K` : '≥ 0'
    } );
  }

  // The last bin is unbounded
  bins[binCount - 1].to = undefined;

  return bins;
}

// ----------------------------------------------------------------------------
// Utility Functions 2

/**
 * @param {Object} data - Data to process.
 * @returns {Object} The processed data.
 */
function processMapData( data ) {
  // Filter out any empty values just in case
  data = data.filter( function( row ) {
    return Boolean( row.name );
  } );

  data = data.map( function( obj, i ) {
    const state = getTileMapState[obj.name];
    return {
      ...obj,
      perCapita: obj.perCapita.toFixed(2),
      path: state.path,
    };
  } );

  return data;
}

// ----------------------------------------------------------------------------
// Highcharts callbacks

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

  // args: (str, x, y, shape, anchorX, anchorY, useHTML, baseline, className)
  // const labelTx = 'Map shading: Complaints';
  // chart.renderer
  //   .label( labelTx, 5, 5, null, null, null, true, false, 'label__tile-map' )
  //   .add();

  const legend = chart.renderer.g( 'legend__tile-map' )
    .translate(10, marginTop)
    .add();

  for (var i = 0; i < bins.length; i++) {
    const g = chart.renderer.g( `g${ i }` )
      .translate(i * (boxWidth + boxPadding), 0)
      .add(legend);

    const bin = bins[i];

    chart.renderer
      .rect( 0, 0, boxWidth, boxHeight )
      .attr( { 'fill': bin.color } )
      .addClass( 'legend-box' )
      .add( g );

    chart.renderer
      .text( bin.name, 2, boxHeight - 2 )
      .addClass( 'legend-text' )
      .add( g );
  }
}

// ----------------------------------------------------------------------------
// Tile Map class

accessibility( Highcharts );

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );

// ----------------------------------------------------------------------------
// Tile Map class

class TileMap {
  constructor( { el, description, data, metadata, title } ) {
    // console.log(data);
    data = processMapData(data);

    const colors = [
      'rgba(247, 248, 249, 0.5)',
      'rgba(212, 231, 230, 0.5)',
      'rgba(180, 210, 209, 0.5)',
      'rgba(137, 182, 181, 0.5)',
      'rgba(86, 149, 148, 0.5)',
      'rgba(37, 116, 115, 0.5)'
    ];
    const bins = getBins( data, colors );
    const localize = true;

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
        pointFormatter: function() {
          const product = this.product ? '<div class="row u-clearfix">' +
            '<p class="u-float-left">Product with highest complaint volume</p>' +
            '<p class="u-right">' + this.product + '</p>' +
            '</div>' : '';

          const issue = this.issue ? '<div class="row u-clearfix">' +
            '<p class="u-float-left">Issue with highest complaint volume</p>' +
            '<p class="u-right">' + this.issue + '</p>' +
            '</div>' : '';

          const value = localize ? this.value.toLocaleString() : this.value;
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
        },
        useHTML: true
      },
      plotOptions: {
        series: {
          dataLabels: {
            enabled: true,
            formatter: function() {
              const valKey = this.point.displayValue ? 'displayValue' : 'value';

              // are we using perCapita or value?
              const value = localize ? this.point[valKey].toLocaleString() : this.point[valKey];
              return '<div class="highcharts-data-label-state">' +
                '<span class="abbr">' + this.point.name + '</span>' +
                '<br />' +
                '<span class="value">' + value + '</span>' +
                '</div>';
            },
            useHTML: true
          }
        }
      },

      series: [ {
        type: 'map',
        clip: false,
        name: title,
        data: data
      } ]
    };

    return Highcharts.mapChart( el, options, _drawLegend );
  }
}

export default TileMap;
