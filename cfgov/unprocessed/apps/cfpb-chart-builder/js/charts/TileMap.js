import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import getTileMapColor from '../utils/get-tile-map-color';
import { processMapData } from '../utils/process-json';

accessibility( Highcharts );

/**
 * Draw a legend on a chart.
 * @param {Object} chart A highchart chart.
 */
function _drawLegend( chart ) {

  /**
   * @param {string} color hex color code.
   * @returns {Object} Return a hash of box fill and stroke styles.
   */
  function _boxStyle( color ) {
    return {
      'stroke-width': 1,
      'stroke': getTileMapColor.gray80,
      'fill': color
    };
  }

  // args: (str, x, y, shape, anchorX, anchorY, useHTML, baseline, className)
  const labelTx = 'Year-over-year change (rounded to the nearest whole number)';
  chart.renderer
    .label( labelTx, 5, 5, null, null, null, true, false, 'label__tile-map' )
    .add();

  const legend = chart.renderer.g( 'legend__tile-map ' ).add();

  chart.renderer
    .rect( 10, 48, 15, 15 )
    .attr( _boxStyle( getTileMapColor.green50 ) )
    .add( legend );
  chart.renderer
    .rect( 10, 71, 15, 15 )
    .attr( _boxStyle( getTileMapColor.green20 ) )
    .add( legend );
  chart.renderer
    .rect( 10, 94, 15, 15 )
    .attr( _boxStyle( getTileMapColor.gray5 ) )
    .add( legend );
  chart.renderer
    .rect( 10, 117, 15, 15 )
    .attr( _boxStyle( getTileMapColor.pacific20 ) )
    .add( legend );
  chart.renderer
    .rect( 10, 140, 15, 15 )
    .attr( _boxStyle( getTileMapColor.pacific50 ) )
    .add( legend );

  chart.renderer.text( '16% or greater', 32, 61 ).add( legend );
  chart.renderer.text( '6% to 15%', 32, 84 ).add( legend );
  chart.renderer.text( '-5% to 5%', 32, 107 ).add( legend );
  chart.renderer.text( '-15% to -6%', 32, 130 ).add( legend );
  chart.renderer.text( '-16% or less', 32, 153 ).add( legend );

}

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );

class TileMap {
  constructor( { el, description, data, metadata, title } ) {
    data = processMapData( data[0], metadata );

    const options = {
      chart: {
        marginTop: 150,
        styledMode: true
      },
      title: false,
      description: description,
      credits: false,
      legend: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      series: [ {
        type: 'map',
        clip: false,
        dataLabels: {
          enabled: true,
          formatter: function() {
            return '<div class="highcharts-data-label-state-abbr">' +
                   this.point.name +
                   '<br /><span class=highcharts-data-label-state-value>' +
                   this.point.value + '%</span></div>';
          },
          useHTML: true
        },
        name: title,
        data: data
      } ]
    };

    return Highcharts.mapChart( el, options, _drawLegend );
  }
}

export default TileMap;
