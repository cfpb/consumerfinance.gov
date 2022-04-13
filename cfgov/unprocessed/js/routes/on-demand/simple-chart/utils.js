/* eslint-disable complexity */

import chartHooks from './chart-hooks.js';

/**
 * Adjusts legend alignment based on series length
 * @param {object} defaultObj default object to be decorated
 * @param {string} chartType current chart type
 */
function alignMargin( defaultObj, chartType ) {
  const len = defaultObj.series.length;
  let marg = ( len * 23 ) + 35;
  let y = 0;
  if ( chartType === 'tilemap' ) {
    marg = 100;
    y = -15;
  } else {
    if ( marg < 100 ) {
      marg = 100;
      y = 40 / len;
    }
    if ( window.innerWidth <= 660 ) {
      marg = ( len * 23 ) + 60;
      y = 0;
    }
  }
  if ( !defaultObj.chart.marginTop ) defaultObj.chart.marginTop = marg;
  if ( !defaultObj.legend.y ) defaultObj.legend.y = y;
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
 * Mutates a style object with entries from the style overrides field
 * @param {string} styleOverrides Stringified JSON style overrides
 * @param {object} obj The object to mutate
 * @param {object} data The data to provide to the chart
 */
function overrideStyles( styleOverrides, obj, data ) {
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
      x = chartHooks.getDateString( x );
    }
    let str = `<b>${ x }</b><br/>${ yAxisLabel }: <b>${ this.y }</b>`;
    if ( this.series && this.series.name ) {
      str = `<b>${ this.series.name }</b><br/>` + str;
    }
    return str;
  };
}

export {
  alignMargin,
  formatSeries,
  makeFormatter,
  overrideStyles
};
