/* eslint complexity: ["error", 10] */
/* eslint max-statements: ["error", 30] */
/* eslint max-params: ["error", 9] */
/* eslint consistent-return: [0] */
// Polyfill Promise for IE11
import 'core-js/features/promise';

import Highcharts from 'highcharts/highstock';
// import Highmaps from 'highcharts/highmaps';
import Papa from 'papaparse';
import accessibility from 'highcharts/modules/accessibility';
import chartHooks from './chart-hooks.js';
import cloneDeep from 'lodash.clonedeep';
import defaultBar from './bar-styles.js';
import defaultDatetime from './datetime-styles.js';
import defaultLine from './line-styles.js';
import defaultTilemap from './tilemap-styles.js';
import fetch from 'cross-fetch';

accessibility( Highcharts );

const dataCache = {};


/**
 * Fetches data from the global dataCache
 * @param {string} url The url to fetch data from
 * @returns {Promise | undefined} A promise that resolves to JSON data or undefined
 */
function fetchFromCache( url ) {
  const cached = dataCache[url];
  if ( cached ) return Promise.resolve( cached );
}

/**
 * Stores data in the global dataCache
 * @param {string} url The url to use for the key
 * @param {Object} data The JSON data to store
 */
function storeInCache( url, data ) {
  dataCache[url] = data;
}

/**
 * Fetches JSON data
 * @param {string} url The url to fetch data from
 * @param {Boolean} isCSV Whether the data to fetch is a CSV
 * @returns {Promise} Promise that resolves to JSON data
 */
function fetchData( url, isCSV ) {
  const data = fetchFromCache( url );
  if ( data ) return Promise.resolve( data );
  const p = fetch( url ).then( res => {
    let prom;
    if ( isCSV ) prom = res.text();
    else prom = res.json();

    return prom.then( d => {
      if ( isCSV ) {
        d = Papa.parse( d, {
          header: true, comments: true, skipEmptyLines: true
        } ).data;
      }
      storeInCache( url, d );
      return Promise.resolve( d );
    } );
  } );
  storeInCache( url, p );
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
    case 'tilemap':
      return defaultTilemap;
    default:
      throw new Error( 'Unknown chart type specified' );
  }
}

/**
 * Mutates a style object with entries from the style overrides field
 * @param {string} styleOverrides Stringified JSON style overrides
 * @param {object} obj The object to mutate
 * @param {object} data The data to provide to the chart
 */
function applyOverrides( styleOverrides, obj, data ) {
  const styles = JSON.parse( styleOverrides );
  Object.keys( styles ).forEach( key => {
    const override = resolveOverride( styles[key], data );
    key.split( '.' ).reduce( ( acc, curr, i, arr ) => {
      if ( i === arr.length - 1 ) return ( acc[curr] = override );
      if ( !acc[curr] ) acc[curr] = {};
      return acc[curr];
    }, obj );
  } );
}

/**
 * Pulls specified keys from the resolved data object
 * @param {array} rawData Array of data from JSON, CSV or directly entered
 * @param {string} series The keys for data to render into the chart
 * @param {string} x_axis_data Key or array of categories
 * @returns {array} Series data
 */
function extractSeries( rawData, { series, xAxisData, chartType } ) {
  if ( series ) {
    if ( series.match( /^\[/ ) ) {
      series = JSON.parse( series );
    } else {
      series = [ series ];
    }

    if ( chartType === 'datetime' ) {
      if ( !xAxisData ) xAxisData = 'x';
    }

    const seriesData = [];

    // array of {name: str, data: arr (maybe of obj)}
    series.forEach( currSeries => {
      let name = currSeries;
      let key = currSeries;
      if ( typeof currSeries === 'object' ) {
        name = name.label;
        key = key.key;
      }
      const currArr = [];
      const currObj = {
        name,
        data: currArr
      };

      rawData.forEach( obj => {
        let d = Number( obj[key] );
        if ( chartType === 'datetime' ) {
          d = {
            x:  Number( new Date( obj[xAxisData] ) ),
            y: d
          };
        }
        currArr.push( d );
      } );
      seriesData.push( currObj );
    } );
    return seriesData;
  }
  return null;
}

/**
 * Formats processed series data as expected by Highcharts
 * @param {object} data Series data in various acceptable formats
 * @returns {object} Correctly formatted series object
 */
function formatSeries( data ) {
  const { series } = data;
  if ( series ) {
    if ( !isNaN( series[0] ) ) {
      return [ { data: series } ];
    }
    return series;
  }
  if ( data.transformed ) {
    if ( Array.isArray( data.transformed ) ) {
      return [ { data: data.transformed } ];
    }
    return data.transformed;
  }
  return [ { data: data.raw } ];
}

/**
 * Makes a tooltip formatter function
 * @param {string} yAxisLabel Label for the yAxis
 * @returns {function} The formatter function
 */
function makeFormatter( yAxisLabel ) {
  return function() {
    let x = this.x;
    if ( Number.isInteger( x ) && String( x ).length === 13 ) {
      x = new Date( x );
    }
    if ( x instanceof Date ) {
      x = x.toLocaleDateString( 'en-US', {
        dateStyle: 'medium',
        timeZone: 'UTC'
      } );
    }
    let str = `<b>${ x }</b><br/>${ yAxisLabel }: <b>${ this.y }</b>`;
    if ( this.series && this.series.name ) {
      str = `<b>${ this.series.name }</b><br/>` + str;
    }
    return str;
  };
}

/**
 * Overrides default chart options using provided Wagtail configurations
 * @param {object} data The data to provide to the chart
 * @param {object} dataProps (destructured) data-* props attached to the chart HTML
 * @returns {object} The configured style object
 */
function makeChartOptions(
  data,
  { chartType, styleOverrides, description, xAxisData, xAxisLabel,
    yAxisLabel, filters }
) {
  const defaultObj = cloneDeep( getDefaultChartObject( chartType ) );

  if ( styleOverrides ) {
    applyOverrides( styleOverrides, defaultObj, data );
  }

  if ( xAxisData && chartType !== 'datetime' ) {
    defaultObj.xAxis.categories = resolveKey( data.raw, xAxisData );
  }
  /* eslint-disable-next-line */
  defaultObj.title = { text: undefined };
  defaultObj.series = formatSeries( data );
  defaultObj.accessibility.description = description;
  defaultObj.yAxis.title.text = yAxisLabel;
  if ( xAxisLabel ) defaultObj.xAxis.title.text = xAxisLabel;
  if ( !defaultObj.tooltip.formatter ) {
    defaultObj.tooltip.formatter = makeFormatter( yAxisLabel );
  }
  if ( isDateFilter( filters, xAxisData ) ) {
    defaultObj.navigator.enabled = false;
    defaultObj.xAxis.min = defaultObj.series[0].data[0].x;
  }
  if ( defaultObj.series.length > 1 ) {
    const len = defaultObj.series.length;
    let marg = ( len * 23 ) + 35;
    let y = 0;
    if ( marg < 100 ) {
      marg = 100;
      y = 19;
    }
    defaultObj.legend.enabled = true;
    defaultObj.chart.marginTop = marg;
    defaultObj.legend.y = y;
  }

  return defaultObj;
}

/**
 * Resolves provided x axis or series data
 * @param {array} rawData Data provided to the chart
 * @param {string} key Key to resolve from data, or categories provided directly
 * @returns {array} Resolved array of data
 */
function resolveKey( rawData, key ) {
  // Array provided directly
  if ( key.match( /^\[/ ) ) {
    return JSON.parse( key );
  }
  return rawData.map( d => d[key] );
}

/**
 * Mechanism for passing functions or applied functions to the chart style object
 * @param {string} override Prefixed refered to a function in chart-hooks.js
 * @param {object} data Data provided to chart
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
  if ( source.match( /^http/i ) || source.match( /^\// ) ) {
    const isCSV = Boolean( source.match( /csv$/i ) );
    return fetchData( source, isCSV );
  }
  return Promise.resolve( JSON.parse( source ) );
}

/**
 * Wires up select filters, if present
 * @param {object} filter Object with a filter key and possible label
 * @param {object} data The raw chart data
 * @param {boolean} isDate Whether the data should be stored as JS dates
 * @returns {array} List of options for the select
 */
function getOptions( filter, data, isDate ) {
  const vals = {};
  const key = filter.key ? filter.key : filter;
  data.forEach( d => {
    let item = d[key];
    if ( !Array.isArray( item ) ) item = [ item ];
    item.forEach( v => {
      vals[v] = 1;
    } );
  } );

  const options = Object.keys( vals );
  if ( isDate ) return options.map( v => Number( new Date( v ) ) );
  return options;
}

/**
 * @param {array} options List of options to build for the select component
 * @param {object} chartNode The DOM node of the current chart
 * @param {object} filter key and possible label to filter on
 * @param {string} selectLabel Optional label for the select element
 * @param {boolean} selectLast Whether to select the last element
 * @returns {object} the built select DOM node
 */
function makeFilterDOM( options, chartNode, filter, selectLabel, selectLast ) {
  const name = filter.label ? filter.label : filter.key;
  const id = Math.random() + name;
  const attachPoint = chartNode.getElementsByClassName( 'chart-selects' )[0];

  const wrapper = document.createElement( 'div' );
  wrapper.className = 'select-wrapper m-form-field m-form-field__select';

  const label = document.createElement( 'label' );
  label.className = 'a-label a-label__heading';
  label.innerText = selectLabel ? selectLabel : 'Select ' + name;
  label.htmlFor = id;

  const selectDiv = document.createElement( 'div' );
  selectDiv.className = 'a-select';

  const select = document.createElement( 'select' );
  select.id = id;
  select.dataset.key = filter.key;

  if ( !selectLabel ) {
    const allOpt = document.createElement( 'option' );
    allOpt.value = '';
    allOpt.innerText = 'View all';
    select.appendChild( allOpt );
  }

  options.forEach( option => {
    const opt = document.createElement( 'option' );
    opt.value = option;
    if ( selectLabel ) opt.innerText = processDate( option );
    else opt.innerText = option;
    select.appendChild( opt );
  } );

  if ( selectLast ) {
    select.value = options[options.length - 1];
  }

  selectDiv.appendChild( select );
  wrapper.appendChild( label );
  wrapper.appendChild( selectDiv );
  attachPoint.appendChild( wrapper );

  return select;
}

/**
 * @param {number} option The JS-date formatted option
 * @returns {string} Specially formatted date
 */
function processDate( option ) {
  const d = new Date( option );
  return d.toLocaleDateString( 'en-US', {
    dateStyle: 'medium',
    timeZone: 'UTC'
  } );
}

/**
 * @param {string} title The title to be case adjusted
 * @returns {string} The case adjusted title
 */
function titleCase( title ) {
  if ( title[0].match( /[A-Z]/ ) && !title[1].match( /[A-Z]/ ) ) {
    return title[0].toLowerCase() + title.slice( 1 );
  }
}

/**
 * @param {object} chartNode The DOM node of the current chart
 * @returns {object} the built select DOM node
 */
function makeSelectHeaderDOM( chartNode ) {
  const attachPoint = chartNode.getElementsByClassName( 'chart-selects' )[0];
  const selectHeader = document.createElement( 'h3' );
  selectHeader.innerText = 'Total ' + titleCase( attachPoint.dataset.title );
  attachPoint.appendChild( selectHeader );

  return selectHeader;
}

/**
 * @param {object} selectNode The DOM node of the select component
 * @param {object} chartNode The DOM node of the chart
 * @param {object} chart The Highcharts chart object
 * @param {object} dataset Data passed via data-* tags
 * @param {object} filter The filter key and possible label
 * @param {object} data The raw chart data, untransformed
 * @param {function} transform The transform function for this chart
 */
function attachFilter(
  selectNode, chartNode, chart, dataset, filter, data, transform
) {
  const attachPoint = chartNode.getElementsByClassName( 'chart-selects' )[0];
  const selectHeader = attachPoint.querySelector( 'h3' );
  const { styleOverrides } = dataset;
  const title = titleCase( attachPoint.dataset.title );
  selectNode.addEventListener( 'change', () => {
    // filter on all selects
    const selects = chartNode.querySelectorAll( '.a-select > select' );
    let filtered = data;
    let headerText = 'Total ' + title;
    let isFirst = true;

    for ( let i = 0; i < selects.length; i++ ) {
      const curr = selects[i];
      const { value } = curr;
      if ( value ) {
        if ( isFirst ) {
          headerText = attachPoint.dataset.title + ' for <b>' + value + '</b>';
          isFirst = false;
        } else {
          headerText = headerText + ' and <b>' + value + '</b>';
        }
      }

      filtered = chartHooks.filter(
        filtered, curr.dataset.key, value );
    }

    if ( transform ) {
      filtered = transform( filtered );
    }

    selectHeader.innerHTML = headerText;
    const applyHooks = styleOverrides && styleOverrides.match( 'hook__' );

    // TODO filter everything
    chart.series[0].setData( filtered, !applyHooks );

    if ( applyHooks ) {
      const obj = {};
      applyOverrides( styleOverrides, obj, filtered );
      chart.update( obj );
    }
  } );
}

/**
 * @param {string} filters The filters data key
 * @param {string} xAxisData The xAxis data key
 * @returns {boolean} Whethere the filter is data-based or date-based
 */
function isDateFilter( filters, xAxisData ) {
  return xAxisData && filters && filters.match( xAxisData );
}

/**
 * @param {object} startNode The DOM node of the select component
 * @param {object} endNode The DOM node of the select component
 * @param {object} chart The Highcharts chart object
 */
function attachDateFilters( startNode, endNode, chart ) {
  startNode.addEventListener( 'change', () => {
    if ( startNode.value < endNode.value ) {
      chart.xAxis[0].setExtremes(
        new Date( Number( startNode.value ) ),
        new Date( Number( endNode.value ) )
      );
    }
  } );

  endNode.addEventListener( 'change', () => {
    if ( startNode.value < endNode.value ) {
      chart.xAxis[0].setExtremes(
        new Date( Number( startNode.value ) ),
        new Date( Number( endNode.value ) )
      );
    }
  } );
}

/** Wires up select filters, if present
  * @param {object} dataset Data passed via data-* tags
  * @param {object} chartNode The DOM node of the current chart
  * @param {object} chart The initialized chart
  * @param {object} data The raw chart data, untransformed
  * @param {function} transform The transform function for this chart
  * */
function initFilters( dataset, chartNode, chart, data, transform ) {
  let filters = dataset.filters;
  if ( !filters ) return;
  // Allow plain Wagtail strings
  if ( !filters.match( '{' ) && !filters.match( '"' ) ) {
    filters = `"${ filters }"`;
  }

  if ( transform ) data = data.transformed;
  else data = data.raw;

  try {

    filters = JSON.parse( filters );

    if ( isDateFilter( filters, dataset.xAxisData ) ) {
      const options =
        getOptions( filters, data, 1 );
      const startNode = makeFilterDOM( options, chartNode,
        { key: filters, label: filters }, 'Start date'
      );
      const endNode = makeFilterDOM( options, chartNode,
        { key: filters, label: filters }, 'End date', 1
      );
      attachDateFilters( startNode, endNode, chart );
    } else {
      if ( !Array.isArray( filters ) ) filters = [ filters ];
      const selects = [];
      filters.forEach( filter => {
        const options = getOptions( filter, data );
        selects.push( makeFilterDOM( options, chartNode, filter ) );
      } );
      if ( selects.length ) {
        makeSelectHeaderDOM( chartNode );
        selects.forEach( ( selectNode, i ) => {
          attachFilter(
            selectNode, chartNode, chart, dataset, filters[i], data, transform
          );
        } );
      }
    }
  } catch ( err ) {
    /* eslint-disable-next-line */
    console.error( err, 'Bad JSON in chart filters ', filters );
  }
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
  const target = chartNode.getElementsByClassName( 'simple-chart-target' )[0];
  const { source, transform } = target.dataset;

  resolveData( source.trim() ).then( raw => {
    const series = extractSeries( raw, target.dataset );
    const transformed = transform && chartHooks[transform] ?
      chartHooks[transform]( raw ) :
      null;

    const data = {
      raw,
      series,
      transformed
    };

    const chart = Highcharts.chart(
      target,
      makeChartOptions( data, target.dataset )
    );
    const mediaQueryList = window.matchMedia( 'print' );
    mediaQueryList.addListener( function() {
      chart.reflow();
    } );

    initFilters(
      target.dataset, chartNode, chart, data, transform && chartHooks[transform]
    );
  } );
}

buildCharts();
