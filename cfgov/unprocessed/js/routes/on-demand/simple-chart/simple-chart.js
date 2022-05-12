/* eslint-disable complexity */
/* eslint max-statements: ["error", 30] */
/* eslint max-lines-per-function: ["error", 75] */
/* eslint consistent-return: [0] */
import Highcharts from 'highcharts/highstock';
import Papa from 'papaparse';
import accessibility from 'highcharts/modules/accessibility';
import cloneDeep from 'lodash.clonedeep';
import chartHooks from './chart-hooks.js';
import defaultBar from './bar-styles.js';
import defaultDatetime from './datetime-styles.js';
import defaultLine from './line-styles.js';
import tilemapChart from './tilemap-chart.js';
import { alignMargin, extractSeries, formatSeries, makeFormatter, overrideStyles } from './utils.js';
import { initFilters } from './data-filters.js';
import { getProjectedDate } from './utils';

accessibility( Highcharts );

const msInDay = 24 * 60 * 60 * 1000;
const promiseCache = {};

/**
 * Fetches JSON data
 * @param {string} url The url to fetch data from
 * @param {Boolean} isCSV Whether the data to fetch is a CSV
 * @returns {Promise} Promise that resolves to JSON data
 */
function fetchData( url, isCSV ) {
  const promise = promiseCache[url];
  if ( promise ) return promise;

  const p = fetch( url ).then( res => {
    let prom;
    if ( isCSV ) prom = res.text();
    else prom = res.json();

    return prom.then( d => {
      if ( isCSV ) {
        /* Excel can put quotes at the start of our # or // comments
           This strips those quotes */
        d = d.replace( /^"(#|\/\/)|(\n)"(#|\/\/)/g, '$1$2$3' );
        d = Papa.parse( d, {
          header: true, comments: true, skipEmptyLines: true
        } ).data;
      }
      return Promise.resolve( d );
    } );
  } );

  promiseCache[url] = p;
  return p;
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
 * @param {object} dataAttributes Data attributes passed to the chart target node
 * @returns {object} The configured style object
 */
function makeChartOptions( data, dataAttributes ) {
  const { chartType, styleOverrides, description, xAxisSource, xAxisLabel,
    yAxisLabel, projectedMonths, defaultSeries } = dataAttributes;
  let defaultObj = cloneDeep( getDefaultChartObject( chartType ) );

  if ( styleOverrides ) {
    overrideStyles( styleOverrides, defaultObj, data );
  }

  if ( xAxisSource && chartType !== 'datetime' ) {
    defaultObj.xAxis.categories = getCategoriesFromXAxisSource(
      data.raw, xAxisSource
    );
  }

  defaultObj.series = formatSeries( data );

  /* eslint-disable-next-line */
  defaultObj.title = { text: undefined };
  defaultObj.accessibility.description = description;
  defaultObj.yAxis.title.text = yAxisLabel;

  if ( !yAxisLabel && chartType === 'datetime' ) {
    defaultObj.rangeSelector.buttonPosition.x = -50;
  }

  if ( xAxisLabel ) defaultObj.xAxis.title.text = xAxisLabel;

  if ( !defaultObj.tooltip.formatter && yAxisLabel ) {
    defaultObj.tooltip.formatter = makeFormatter( yAxisLabel );
  }

  if ( defaultObj.series.length === 1 ) {
    defaultObj.plotOptions.series = {
      ...defaultObj.plotOptions.series,
      events: {
        legendItemClick: function() {
          return false;
        }
      }
    };
  } else {
    defaultObj.legend.title = {
      text: '(Click to show/hide data)',
      style: {
        fontStyle: 'italic',
        fontWeight: 'normal',
        fontSize: '14px',
        color: '#666'
      }
    };
  }

  if ( projectedMonths > 0 ) {
    defaultObj = addProjectedMonths( defaultObj, projectedMonths );
    defaultObj.legend.y = -10;
    defaultObj.chart.marginTop = 180;

  }

  if ( defaultSeries === 'False' ) {
    defaultObj.series = defaultObj.series.map( ( singluarSeries, i ) => {
      // Skip the first series
      if ( i > 0 ) {
        singluarSeries.visible = false;
      }
      return singluarSeries;
    } );
  }

  alignMargin( defaultObj, chartType );

  return defaultObj;
}

/**
 * Adds projected months to config object for Highcharts
 * @param {object} chartObject The config object for Highcharts
 * @param {integer} numMonths The number of months input into wagtail field
 * @returns {object} The config object with projected months
 */
function addProjectedMonths( chartObject, numMonths ) {

  // Convert the number of projected months into a timestamp
  const lastChartDate = chartObject.series[0].data.at( -1 ).x;

  // Convert lastChartDate from months to milliseconds for Epoch format
  const convertedProjectedDate = lastChartDate - ( numMonths * 30 * msInDay );
  const projectedDate = getProjectedDate( convertedProjectedDate );

  /* Add a vertical line and some explanatory text at the starting
     point of the projected data */
  chartObject.xAxis.plotLines = [ {
    value: projectedDate.timestamp,
    label: {
      text: `Values after ${ projectedDate.humanFriendly } are projected`,
      rotation: 0,
      x: -260,
      y: -10
    }
  } ];

  /* Add a zone to each series with a dotted line starting
     at the projected data starting point */
  chartObject.series = chartObject.series.map( singluarSeries => {
    singluarSeries.zoneAxis = 'x';
    singluarSeries.zones = [ {
      value: projectedDate.timestamp
    }, {
      dashStyle: 'dot'
    } ];
    return singluarSeries;
  } );
  return chartObject;
}

/**
 * Resolves provided x axis or series data
 * @param {array} rawData Data provided to the chart
 * @param {string} key Key to resolve from data, or categories provided directly
 * @returns {array} Resolved array of data
 */
function getCategoriesFromXAxisSource( rawData, key ) {
  // Array provided directly
  if ( key.match( /^\[/ ) ) {
    return JSON.parse( key );
  }
  return rawData.map( d => d[key] );
}

/**
 * Selects whether to use inline data or fetch data that matches a url
 * @param {string} source Source provided from wagtail
 * @returns {Promise} Promise resolving to either fetched JSON or parsed inline JSON
 */
function resolveData( source ) {
  if ( source.match( /^http/i ) || source.match( /^\// ) ) {
    const isCSV = Boolean( source.match( /csv$/i ) );
    return fetchData( source, isCSV );
  }
  return Promise.resolve( JSON.parse( source ) );
}

/**
 * Initializes every chart on the page
 */
function buildCharts() {
  const charts = document.getElementsByClassName( 'o-simple-chart' );
  for ( let i = 0; i < charts.length; i++ ) {
    buildChart( charts[i] );
  }
}

/**
 * Initializes a chart
 * @param {object} chartNode The DOM node of the current chart
 */
function buildChart( chartNode ) {
  const target = chartNode.getElementsByClassName( 'o-simple-chart_target' )[0];
  const dataAttributes = target.dataset;
  const { source, transform, chartType } = dataAttributes;

  resolveData( source.trim() ).then( raw => {
    const transformed = transform && chartHooks[transform] ?
      chartHooks[transform]( raw ) :
      null;

    const series = extractSeries( transformed || raw, dataAttributes );

    const data = {
      raw,
      series,
      transformed
    };

    let chart;

    if ( chartType === 'tilemap' ) {
      chart = tilemapChart.init( chartNode, target, data, dataAttributes );
    } else {
      chart = Highcharts.chart(
        target,
        makeChartOptions( data, dataAttributes )
      );

      initFilters(
        dataAttributes, chartNode, chart, data
      );
    }

    // Make sure chart is displayed properly on print
    window.matchMedia( 'print' ).addListener( function() {
      chart.reflow();
    } );

  } );
}

buildCharts();
