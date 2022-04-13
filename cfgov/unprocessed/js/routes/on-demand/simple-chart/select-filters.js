/* eslint-disable complexity */
/* eslint max-statements: ["error", 30] */
/* eslint max-params: ["error", 9] */
import chartHooks from './chart-hooks.js';
import { overrideStyles } from './utils.js';

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
 * @param {string} filters The filters data key
 * @param {string} xAxisSource The xAxis data key
 * @returns {boolean} Whethere the filter is data-based or date-based
 */
function isDateFilter( filters, xAxisSource ) {
  return xAxisSource && filters && filters.match( xAxisSource );
}

/**
 * @param {number} option The JS-date formatted option
 * @param {object} filter The filter object
 * @returns {string} Specially formatted date
 */
function processDate( option, filter ) {
  if ( filter && filter.key === 'tilemap' ) {
    const [ quarter, year ] = chartHooks.cci_dateToQuarter( option );
    return `${ quarter } ${ year }`;
  }
  const d = new Date( option );
  return chartHooks.getDateString( d );
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
 * @param {boolean} selectLast Whether to select the last element
 * @returns {object} the built select DOM node
 */
function makeFilterDOM( options, chartNode, filter, selectLabel, selectLast ) {
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

  if ( !selectLabel ) {
    const allOpt = document.createElement( 'option' );
    allOpt.value = '';
    allOpt.innerText = 'View all';
    select.appendChild( allOpt );
  }

  options.forEach( option => {
    const opt = document.createElement( 'option' );
    opt.value = option;
    if ( selectLabel ) opt.innerText = processDate( option, filter );
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

/** Wires up select filters, if present
  * @param {object} dataAttributes Data passed via data-* tags
  * @param {object} chartNode The DOM node of the current chart
  * @param {object} chart The initialized chart
  * @param {object} data The raw chart data, untransformed
  * @param {function} transform The transform function for this chart
  * */
function initFilters( dataAttributes, chartNode, chart, data, transform ) {
  let filters = dataAttributes.filters;
  if ( !filters ) return;
  // Allow plain Wagtail strings
  if ( !filters.match( '{' ) && !filters.match( '"' ) ) {
    filters = `"${ filters }"`;
  }

  if ( transform ) data = data.transformed;
  else data = data.raw;

  try {

    filters = JSON.parse( filters );

    if ( isDateFilter( filters, dataAttributes.xAxisSource ) ) {
      const options =
        getSelectOptions( filters, data, 1 );
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
        const options = getSelectOptions( filter, data );
        selects.push( makeFilterDOM( options, chartNode, filter ) );
      } );
      if ( selects.length ) {
        makeSelectHeaderDOM( chartNode );
        selects.forEach( ( selectNode, i ) => {
          attachFilter(
            selectNode, chartNode, chart, dataAttributes,
            filters[i], data, transform
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
 * @param {object} selectNode The DOM node of the select component
 * @param {object} chartNode The DOM node of the chart
 * @param {object} chart The Highcharts chart object
 * @param {object} dataAttributes Data passed via data-* tags
 * @param {object} filter The filter key and possible label
 * @param {object} data The raw chart data, untransformed
 * @param {function} transform The transform function for this chart
 */
function attachFilter(
  selectNode, chartNode, chart, dataAttributes, filter, data, transform
) {
  const attachPoint = chartNode.getElementsByClassName( 'o-simple-chart_selects' )[0];
  const selectHeader = attachPoint.querySelector( 'h3' );
  const { styleOverrides } = dataAttributes;
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

    /* TODO filter everything instead of just the first series
       Currently this assumes filters only apply to single series charts */
    chart.series[0].setData( filtered, !applyHooks );

    if ( applyHooks ) {
      const obj = {};
      overrideStyles( styleOverrides, obj, filtered );
      chart.update( obj );
    }
  } );
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

export {
  initFilters,
  isDateFilter,
  makeFilterDOM
};
