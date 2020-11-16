// Polyfill Promise for IE11
import 'core-js/features/promise';

import Highcharts from 'highcharts/highstock';
import accessibility from 'highcharts/modules/accessibility';
import chartHooks from './chart-hooks.js';
import defaultBar from './bar-styles.js';
import defaultDatetime from './datetime-styles.js';
import defaultLine from './line-styles.js';
import fetch from 'cross-fetch';

accessibility( Highcharts );

/**
 * Fetches JSON data
 * @param {string} url The url to fetch data from
 * @returns {Promise} Promise that resolves to JSON data
 */
function fetchData( url ) {
  return fetch( url ).then( res => res.json() );
}

/**
 * Selects appropriate chart import style
 * @param {string} type The chart type as defined in the organism
 * @returns {object} The appropriately loaded style object
 */
function getDefaultChartObject( type ) {
  switch ( type ) {
    case 'bar':
      return defaultBar;
    case 'datetime':
      return defaultDatetime;
    case 'line':
      return defaultLine;
    default:
      throw new Error( 'Unknown chart type specified' );
  }
}

/**
 * Overrides default chart options using provided Wagtail configurations
 * @param {object} data The data to provide to the chart
 * @param {object} dataProps (destructured) data-* props attached to the chart HTML
 * @returns {object} The configured style object
 */
function makeChartOptions(
  data,
  { chartType, styleOverrides, description, xAxisLabel, yAxisLabel }
) {
  const defaultObj = JSON.parse(
    JSON.stringify( getDefaultChartObject( chartType ) )
  );

  if ( styleOverrides ) {
    const styles = JSON.parse( styleOverrides );
    Object.keys( styles ).forEach( key => {
      const override = resolveOverride( styles[key], data );
      key.split( '.' ).reduce( ( acc, curr, i, arr ) => {
        if ( i === arr.length - 1 ) return ( acc[curr] = override );
        if ( !acc[curr] ) acc[curr] = {};
        return acc[curr];
      }, defaultObj );
    } );
  }

  /* eslint-disable-next-line */
  defaultObj.title = { text: undefined };
  defaultObj.series = [ { data } ];
  defaultObj.description = description;
  defaultObj.yAxis.title.text = yAxisLabel;
  if ( xAxisLabel ) defaultObj.xAxis.title.text = xAxisLabel;

  return defaultObj;
}

/**
 * Mechanism for passing functions or applied functions to the chart style object
 * @param {string} override Prefixed refered to a function in chart-hooks.js
 * @param {string} data Data provided to chart
 * @returns {function|string} Result of the override or the provided unmatched style
 */
function resolveOverride( override, data ) {
  if ( typeof override === 'string' ) {
    if ( override.match( /^fn__/ ) ) {
      return chartHooks[override.replace( 'fn__', '' )];
    } else if ( override.match( /^hook__/ ) ) {
      return chartHooks[override.replace( 'hook__', '' )]( data );
    }
  }
  return override;
}

/**
 * Selects whether to use inline data or fetch data that matches a url
 * @param {string} source Source provided from wagtail
 * @returns {Promise} Promise resolving to either fetched JSON or parsed inline JSON
 */
function resolveData( source ) {
  if ( source.match( /^http/i ) ) {
    return fetchData( source );
  }
  return Promise.resolve( JSON.parse( source ) );

}

/**
 * Initializes every chart on the page
 */
function buildCharts() {
  const charts = document.getElementsByClassName( 'simple-chart-target' );
  for ( let i = 0; i < charts.length; i++ ) {
    buildChart( charts[i] );
  }
}

/**
 * Initializes a chart
 * @param {object} chart The DOM node of the current chart
 */
function buildChart( chart ) {
  const { source, transform } = chart.dataset;

  resolveData( source.trim() ).then( d => {
    const data =
      transform && chartHooks[transform] ? chartHooks[transform]( d ) : d;

    Highcharts.chart( chart, makeChartOptions( data, chart.dataset ) );
  } );
}

buildCharts();
