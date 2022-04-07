/* eslint-disable complexity */
/* eslint max-statements: ["error", 30] */
/* eslint max-params: ["error", 9] */
import chartHooks from './chart-hooks.js';
import { extractSeries, overrideStyles } from './utils.js';

/**
 * Generates a list of options for the select filters
 * @param {object} filter Object with a filter key and possible label
 * @param {object} data The raw chart data
 * @param {boolean} isDate Whether the data should be stored as JS dates
 * @returns {array} List of options for the select
 */
function getSelectOptions( filter, data, isDate ) {
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
 * @param {number} option The JS-date formatted option
 * @returns {string} Specially formatted date
 */
function processDate( option ) {
  const [ quarter, year ] = chartHooks.cci_dateToQuarter( option );
  return `${ quarter } ${ year }`;
}

/**
 * @param {string} title The title to be case adjusted
 * @returns {string} The case adjusted title
 */
function titleCase( title ) {
  if ( title[0].match( /[A-Z]/ ) && !title[1].match( /[A-Z]/ ) ) {
    return title[0].toLowerCase() + title.slice( 1 );
  }
  return title;
}


/**
 * @param {object} chartNode The DOM node of the current chart
 * @returns {object} the built select DOM node
 */
function makeSelectHeaderDOM( chartNode ) {
  const attachPoint = chartNode.getElementsByClassName( 'o-simple-chart_selects' )[0];
  const selectHeader = document.createElement( 'h3' );
  selectHeader.innerText = 'Total ' + titleCase( attachPoint.dataset.title );
  attachPoint.appendChild( selectHeader );

  return selectHeader;
}


/**
 * @param {array} options List of options to build for the select component
 * @param {object} chartNode The DOM node of the current chart
 * @param {object} filter key and possible label to filter on
 * @param {string} selectLabel Optional label for the select element
 * @returns {object} the built select DOM node
 */
function makeFilterDOM( options, chartNode, filter, selectLabel ) {
  const name = filter.label ? filter.label : filter.key;
  const id = Math.random() + name;
  const attachPoint = chartNode.getElementsByClassName( 'o-simple-chart_selects' )[0];

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

  /* Explicitly pass "all" key as part of filter */
  if ( filter.all ) {
    const allOpt = document.createElement( 'option' );
    allOpt.value = '';
    allOpt.innerText = 'View all';
    select.appendChild( allOpt );
  }

  options.forEach( option => {
    const opt = document.createElement( 'option' );
    opt.value = option;

    if ( name === 'tilemap' ) opt.innerText = processDate( option );
    else opt.innerText = option;

    select.appendChild( opt );
  } );

  selectDiv.appendChild( select );
  wrapper.appendChild( label );
  wrapper.appendChild( selectDiv );
  attachPoint.appendChild( wrapper );

  return select;
}

/** Filters raw or transformed data by a select prop
  * @param {array} data Transformed or raw chart data
  * @param {object} filterProp Key on which to filter
  * @param {object} filterVal Value of the selectNode against which we're filtering
  * @returns {array} Filtered chart data
  *
  * */
function filterData( data, filterProp, filterVal ) {
  // For the 'all' filter, where value is set to ''
  if ( !filterVal ) return data;

  return data.filter( d => {
    const match = d[filterProp];
    if ( Array.isArray( match ) ) return match.indexOf( filterVal ) >= 0;
    return match === filterVal;
  } );
}

/** Wires up select filters, if present
  * @param {object} dataAttributes Data passed via data-* tags
  * @param {object} chartNode The DOM node of the current chart
  * @param {object} chart The initialized chart
  * @param {object} data The chart data object, {raw, series, transformed}
  * @param {function} transform The transform function for this chart
  * */
function initFilters( dataAttributes, chartNode, chart, data, transform ) {
  let filters = dataAttributes.filters;
  if ( !filters ) return;
  // Allow plain Wagtail strings
  if ( !filters.match( '{' ) && !filters.match( '"' ) ) {
    filters = `"${ filters }"`;
  }

  let rawOrTransformed = data.raw;
  if ( transform ) rawOrTransformed = data.transformed;

  try {
    filters = JSON.parse( filters );
    if ( !Array.isArray( filters ) ) filters = [ filters ];
    const selects = [];
    filters.forEach( filter => {
      const options = getSelectOptions( filter, rawOrTransformed );
      selects.push( makeFilterDOM( options, chartNode, filter ) );
    } );
    if ( selects.length ) {
      makeSelectHeaderDOM( chartNode );
      selects.forEach( ( selectNode, i ) => {
        attachFilter(
          selectNode, chartNode, chart, dataAttributes,
          filters[i], rawOrTransformed
        );
      } );
    }
  } catch ( err ) {
    /* eslint-disable-next-line */
    console.error( err, 'Bad JSON in chart filters ', filters );
  }
}


/**
 * @param {object} selectNode The DOM node of the select component
 * @param {object} chartNode The DOM node of the chart
 * @param {object} chart The Highcharts chart object
 * @param {object} dataAttributes Data passed via data-* tags
 * @param {object} filter The filter key and possible label
 * @param {object} data Chart data, either raw or transformed
 */
function attachFilter(
  selectNode, chartNode, chart, dataAttributes, filter, data
) {
  const attachPoint = chartNode.getElementsByClassName( 'o-simple-chart_selects' )[0];
  const selectHeader = attachPoint.querySelector( 'h3' );
  const { styleOverrides } = dataAttributes;
  const title = titleCase( attachPoint.dataset.title );

  /**
   * Filter data and update the chart on select
   **/
  function filterOnSelect() {
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
      filtered = filterData( filtered, curr.dataset.key, value );
    }

    selectHeader.innerHTML = headerText;

    const filteredSeries = extractSeries( filtered, dataAttributes );
    filteredSeries.forEach( dataSeries => {
      chart.series.forEach( chartSeries => {
        if ( dataSeries.name === chartSeries.name ) {
          chartSeries.setData( dataSeries.data, false );
        }
      } );
    } );


    const obj = {};

    if ( styleOverrides && styleOverrides.match( 'hook__' ) ) {
      overrideStyles( styleOverrides, obj, filtered );
    }

    chart.update( obj );
  }

  selectNode.addEventListener( 'change', filterOnSelect );

  // Filter initial view
  filterOnSelect();
}

export {
  initFilters,
  makeFilterDOM
};
