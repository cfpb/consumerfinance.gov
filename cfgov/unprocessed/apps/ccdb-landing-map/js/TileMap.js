// import TileMap from 'cfpb-chart-builder/src/js/charts/TileMap';

import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import getTileMapState from 'cfpb-chart-builder/src/js/utils/get-tile-map-state';

// ----------------------------------------------------------------------------
// Utility Functions

/**
 * helper function to get max value
 * @param data array of data
 */
function getMax( data ) {
  return Object.values( data ).reduce( ( a, b ) => Math.max( a, b ), 0 );
}

/**
 * helper function to get the bins for legend and colors, etc.
 * @param data
 * @returns {[]|Array}
 */
function getBins( data ) {
  const binCount = 6;
  const max = getMax( data );
  const min = 0;

  // Early exit
  if ( max === 0 ) return [];

  const bins = [];
  const step = ( max - min ) / binCount;

  for ( let i = 0, curr = min; i < binCount; i++, curr += step ) {
    bins.push( { color: '#000000', index: i, min: Math.round( curr ) } );
  }

  return bins;
}

/**
 * Returns color given a data value.
 * @param   {number} value A numerical data value.
 * @param   {array} bins different buckets for values.
 * @param   {array} colors contains the input colors for the tile map
 * @returns {string} A color hex string.
 */
function getColorByValue( value, bins, colors ) {
  if ( parseInt( value, 10 ) === 0 ) {
    return '#fff';
  }

  let color = '#fff';
  for ( let i = 0; i < colors.length; i++ ) {
    if ( value > bins[ i ].min ) {
      color = colors[ i ];
    }
  }

  return color;
}

// ----------------------------------------------------------------------------
// Utility Functions 2

/**
 * @param {Object} data - Data to process.
 * @returns {Object} The processed data.
 */
function processMapData( data, colors ) {

  if ( typeof data !== 'object' ) {
    return data;
  }

  // Filter out any empty values just in case
  data = data.filter( function( row ) {
    return Boolean( row.name );
  } );

  const bins = getBins( data.map( o => Math.round( Math.abs(parseFloat( o.value ) ) ) ) );
  data = data.map( function( obj, i ) {
    const state = getTileMapState[obj.name];
    return {
      ...obj,
      abbr: state.abbr,
      // fullName: state.fullName,
      path: state.path,
      color: getColorByValue( obj.value, bins, colors )
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
  // do we use the value or perCapita ?
  const valKey = chart.options.series[0].data[0].displayValue ? 'displayValue' : 'value';
  const d = chart.options.series[ 0 ].data.map( o => o[valKey] );
  const colors = chart.options.colors;
  const bins = getBins(d);
  const marginTop = chart.margin[0] || 0;
  const localize = chart.options.localize;

  /**
   * @param {string} color hex color code.
   * @returns {Object} Return a hash of box fill and stroke styles.
   */
  function _boxStyle( color ) {
    return {
      'stroke-width': 1,
      'stroke': '#75787b',
      'fill': color
    };
  }

  // args: (str, x, y, shape, anchorX, anchorY, useHTML, baseline, className)
  const labelTx = 'Map shading: Complaints';
  chart.renderer
    .label( labelTx, 5, 5, null, null, null, true, false, 'label__tile-map' )
    .add();

  const legend = chart.renderer.g( 'legend__tile-map' )
    .translate(10, marginTop)
    .add();
  const g1 = chart.renderer.g( 'g1' ).translate(0,0).add(legend);
  const g2 = chart.renderer.g( 'g2' ).translate(70,0).add(legend);
  const g3 = chart.renderer.g( 'g3' ).translate(140,0).add(legend);
  const g4 = chart.renderer.g( 'g4' ).translate(210,0).add(legend);
  const g5 = chart.renderer.g( 'g5' ).translate(280,0).add(legend);
  const g6 = chart.renderer.g( 'g6' ).translate(350,0).add(legend);
  const g7 = chart.renderer.g( 'g7' ).translate(420,0).add(legend);

  if ( localize ) {
    bins[5].min = bins[5].min.toLocaleString();
    bins[4].min = bins[4].min.toLocaleString();
    bins[3].min = bins[3].min.toLocaleString();
    bins[2].min = bins[2].min.toLocaleString();
    bins[1].min = bins[1].min.toLocaleString();
    bins[0].min = bins[0].min.toLocaleString();
  }

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[5] ) )
    .add( g7 );
  chart.renderer
    .text( '>' + bins[5].min, 0, 14 )
    .add( g7 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[4] ) )
    .add( g6 );
  chart.renderer
    .text( '>' + bins[4].min, 0, 14 )
    .add( g6 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[3] ) )
    .add( g5 );
  chart.renderer
    .text( '>' + bins[3].min, 0, 14 )
    .add( g5 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[2] ) )
    .add( g4 );
  chart.renderer
    .text( '>' + bins[2].min, 0, 14 )
    .add( g4 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[1] ) )
    .add( g3 );
  chart.renderer
    .text( '>' + bins[1].min, 0, 14 )
    .add( g3 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( colors[0] ) )
    .add( g2 );
  chart.renderer
    .text( '>' + bins[0].min, 0, 14 )
    .add( g2 );

  chart.renderer
    .rect( 0, 0, 65, 15 )
    .attr( _boxStyle( '#fff' ) )
    .add( g1 );
  chart.renderer
    .text( 'N/A', 0, 14 )
    .add( g1 );

}

// ----------------------------------------------------------------------------
// Tile Map class

accessibility( Highcharts );

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );


class TileMap {
  constructor( { el, description, data, metadata, title } ) {
    const bins = getBins( data );
    const colors = [
      'rgba(247, 248, 249, 0.5)',
      'rgba(212, 231, 230, 0.5)',
      'rgba(180, 210, 209, 0.5)',
      'rgba(137, 182, 181, 0.5)',
      'rgba(86, 149, 148, 0.5)',
      'rgba(37, 116, 115, 0.5)'
    ];
    const localize = true;

    data = processMapData( data[0], colors );

    const options = {
      bins,
      chart: {
        marginTop: 40,
        styledMode: true
      },
      colors,
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
              return '<div class="highcharts-data-label-state ' + this.point.className + '">' +
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