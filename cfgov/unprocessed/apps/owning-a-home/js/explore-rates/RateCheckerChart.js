import {
  chartTooltip
} from './template-loader';
import Highcharts from 'highcharts';
import RateCheckerChartMenu from './RateCheckerChartMenu';
import { applyThemeTo } from './highcharts-theme';
import highchartsExport from 'highcharts/modules/exporting';

/**
 * RateCheckerChart
 * @class
 * @classdesc Creates the left-hand side chart on /owning-a-home/explore-rates/
 * @returns {RateCheckerChart} An instance.
 */
function RateCheckerChart() {
  let _highChart;
  let _containerDom;

  // References to alert HTML.
  let _resultAlertDom;
  let _failAlertDom;

  let _chartDom;
  let _dataLoadedDom;

  let _currentState = 0;

  // Set some properties for the histogram.
  let isInitialized = false;

  /**
   * Initialize the chart variables and set the loading appearance.
   */
  function init() {
    // Load and style highCharts library. https://www.highCharts.com/docs.
    highchartsExport( Highcharts );
    applyThemeTo( Highcharts );

    _containerDom = document.querySelector( '#chart-section' );
    _resultAlertDom = _containerDom.querySelector( '#chart-result-alert' );
    _failAlertDom = _containerDom.querySelector( '#chart-fail-alert' );
    _chartDom = _containerDom.querySelector( '#chart' );
    _dataLoadedDom = _containerDom.querySelector( '.data-enabled' );

    startLoading();
  }

  /**
   * Initialize and create highcharts-related instances.
   * @returns {RateCheckerChartMenu} A menu instance.
   */
  function _createHighcharts() {
    _highChart = new Highcharts.Chart( {
      chart: {
        renderTo: _chartDom,
        type: 'column',
        animation: false
      },
      title: {
        text: ''
      },
      xAxis: {
        categories: [ 1, 2, 3, 4, 5 ]
      },
      yAxis: [ {
        title: {
          text: ''
        },
        labels: {
          formatter: function() {
            return this.value > 9 ? this.value + '+' : this.value;
          }
        },
        max: 10,
        min: 0
      }, {
        title: {
          text: 'Number of lenders offering rate'
        }
      } ],
      series: [ {
        name: 'Number of Lenders',
        data: [ 1, 1, 1, 1, 1 ],
        showInLegend: false,
        dataLabels: {
          enabled:   true,
          useHTML:   true,
          crop:      false,
          overflow:  'none',
          defer:     true,
          color:     '#919395',
          x:         2,
          y:         2,
          formatter: function() {
            const point = this.point;
            window.setTimeout( function() {
              if ( point.y > 9 ) {
                point.dataLabel.attr( {
                  y: -32,
                  x: point.plotX - 24
                } );
              }
            } );
            return '<div class="data-label"><span class="data-label_number">' + this.x + '</span><br>|</div>';
          }
        }
      } ],
      credits: {
        text: ''
      },
      tooltip: {
        useHTML: true,
        formatter: function() {
          return chartTooltip( this );
        },
        positioner: function( boxWidth, boxHeight, point ) {
          let x, y;
          if ( point.plotY < 0 ) {
            x = point.plotX - 74;
            y = this.chart.plotTop - 74;
          } else {
            x = point.plotX - 54;
            y = point.plotY - 66;
          }
          return {
            x: x,
            y: y
          };
        }
      }
    } );

    return new RateCheckerChartMenu( _highChart );
  }

  /**
   * Render (or update) the _highCharts chart.
   * @param  {Object} data Data processed from the API.
   */
  function render( data ) {
    if ( isInitialized ) {
      _highChart.update( {
        xAxis: {
          categories: data.labels
        },
        series: {
          data: data.vals
        }
      } );
      _containerDom.classList.remove( 'geolocating' );
    } else {
      _containerDom.classList.add( 'geolocating' );
      _createHighcharts();
      isInitialized = true;
    }
  }

  /**
   * Set the state of the slider.
   * @param {number} state 0 = okay, 1 = warning state.
   */
  function setStatus( state ) {
    if ( state === RateCheckerChart.STATUS_OKAY ) {
      _chartDom.classList.remove( 'warning' );
      _resultAlertDom.classList.remove( 'm-notification__visible' );
      _failAlertDom.classList.add( 'u-hidden' );
    } else if ( state === RateCheckerChart.STATUS_WARNING ) {
      _chartDom.classList.add( 'warning' );
      _resultAlertDom.classList.add( 'm-notification__visible' );
    } else if ( state === RateCheckerChart.STATUS_ERROR ) {
      _failAlertDom.classList.remove( 'u-hidden' );
    } else {
      throw new Error( `Status ${ state } set in chart is not supported!` );
    }

    _currentState = state;
  }

  /**
   * Set the loading apperance of the chart.
   */
  function startLoading() {
    setStatus( RateCheckerChart.STATUS_OKAY );
    _dataLoadedDom.classList.add( 'loading' );
    _dataLoadedDom.classList.remove( 'loaded' );
  }

  /**
   * Show an error alert.
   * @param {[number]} state
   *   Pass RateCheckerChart.STATUS_WARNING or RateCheckerChart.STATUS_ERROR.
   */
  function finishLoading( state ) {
    _containerDom.classList.remove( 'geolocating' );

    if ( state ) {
      setStatus( state );
    } else {
      _dataLoadedDom.classList.remove( 'loading' );
      _dataLoadedDom.classList.add( 'loaded' );
    }
  }

  this.setStatus = setStatus;
  this.startLoading = startLoading;
  this.finishLoading = finishLoading;
  this.currentState = _currentState;
  this.render = render;
  this.init = init;

  return this;
}

RateCheckerChart.STATUS_OKAY = 0;
RateCheckerChart.STATUS_WARNING = 1;
RateCheckerChart.STATUS_ERROR = 2;

export default RateCheckerChart;
