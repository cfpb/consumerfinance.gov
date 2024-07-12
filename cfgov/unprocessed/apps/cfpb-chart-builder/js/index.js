import createChartDir from './charts';
import documentReady from './utils/document-ready';
import fetchMapShapes from './utils/fetch-map-shapes';
import getData from './utils/get-data';

class Chart {

  constructor( chartOptions ) {
    this.chartOptions = chartOptions;
    getData( chartOptions.source ).then( data => {
      this.chartOptions.data = data;
      this.draw( this.chartOptions );
    } );
  }

  draw( chartOptions ) {
    switch ( chartOptions.type ) {
      case 'geo-map':
        fetchMapShapes( chartOptions.metadata ).then( shapes => {
          chartOptions.shapes = shapes[0];
          this.highchart = new createChartDir.GeoMap( chartOptions );
        } );
        break;
      case 'line-comparison':
        this.highchart = new createChartDir.LineChartComparison( chartOptions );
        break;
      case 'line-index':
        this.highchart = new createChartDir.LineChartIndex( chartOptions );
        break;
      case 'line':
        this.highchart = new createChartDir.LineChart( chartOptions );
        break;
      case 'bar':
        this.highchart = new createChartDir.BarChart( chartOptions );
        break;
      case 'tile_map':
        this.highchart = new createChartDir.TileMap( chartOptions );
        break;
      default:
    }
  }

  /**
   *
   * @param {Object} newOptions - Options to update the chart with.
   * @returns {Promise} A promise from the get data method.
   */
  update( newOptions ) {
    const needNewMapShapes = this.chartOptions.type === 'geo-map' &&
                             this.chartOptions.metadata !== newOptions.metadata;

    // Merge the old chart options with the new ones
    Object.assign( this.chartOptions, newOptions );

    let promiseError = '';

    /* If the source wasn't changed, we don't need to fetch new data and can
       immediately redraw the chart */
    if ( typeof newOptions.source === 'undefined' ) {
      this.highchart.update( this.chartOptions );
    } else {
      // Otherwise fetch the data and redraw once it arrives
      this.highchart.chart.hideLoading();

      getData( this.chartOptions.source ).then( data => {
        this.chartOptions.data = data;

        if ( needNewMapShapes ) {
          this.chartOptions.needNewMapShapes = true;
          fetchMapShapes( this.chartOptions.metadata ).then( shapes => {
            this.chartOptions.shapes = shapes[0];
            this.highchart.update( this.chartOptions );
          } ).catch( err => {
            promiseError = err;
          } );

          // We're in the fetch-map-shapes get-data promise call, so bail out.
          return;
        }

        this.highchart.update( this.chartOptions );
      } ).catch( err => {
        promiseError = err;
      } );
    }

    return new Promise( ( resolve, reject ) => {
      if ( promiseError !== '' ) {
        reject( promiseError );
      }

      const afterUpdateHandlerBinded = afterUpdateHandler.bind( this );
      this.highchart.addEventListener( 'afterUpdate', afterUpdateHandlerBinded );

      /**
       * Handle afterUpdate event for when the chart is updated.
       * @param {Object} event - Highcharts event object for chart state.
       */
      function afterUpdateHandler( event ) {
        this.highchart.removeEventListener( 'afterUpdate', afterUpdateHandlerBinded );
        resolve();
      }
    } );
  }

}

/**
 * Creates a chart
 * @param {Object} opts - Options to pass to highcharts when creating the chart.
 * @returns {Chart} A Chart instance.
 */
function createChart( opts ) {
  return new Chart( opts );
}

/**
 * Creates several charts at once.
 * @returns {Array} List of chart instances.
 */
function createCharts() {
  const elements = document.querySelectorAll( '.cfpb-chart' );
  const charts = [];

  // Ignore divs with a `data-chart-ignore` data attribute
  let element;
  let chart;
  for ( let i = 0, len = elements.length; i < len; i++ ) {
    if ( !elements[i].getAttribute( 'data-chart-ignore' ) ) {
      element = elements[i];
      chart = new Chart( {
        el: element,
        title: element.getAttribute( 'data-chart-title' ),
        yAxisLabel: element.getAttribute( 'data-chart-y-axis-label' ),
        type: element.getAttribute( 'data-chart-type' ),
        color: element.getAttribute( 'data-chart-color' ),
        metadata: element.getAttribute( 'data-chart-metadata' ),
        source: element.getAttribute( 'data-chart-source' )
      } );
      charts.push( chart );
    }
  }

  return charts;
}

/* *
   When the document is ready, the code for cfpb-chart-builder seeks out chart
   blocks and generates charts inside the designated elements. */
documentReady( createCharts );

export {
  createChart,
  createCharts
};
