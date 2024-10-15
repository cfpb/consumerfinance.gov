import chartHooks from './chart-hooks.js';

/**
 * Adjusts legend alignment based on series length.
 * @param {object} defaultObj - A default object to be decorated.
 * @param {string} chartType - The current chart type.
 */
function alignMargin(defaultObj, chartType) {
  const len = defaultObj.series.length;
  let marg = len * 23 + 35;
  let y = 0;
  if (chartType === 'tilemap') {
    marg = 100;
    y = -15;
  } else {
    if (marg < 100) {
      marg = 100;
      y = 40 / len;
    }
    if (window.innerWidth <= 660) {
      marg = len * 23 + 60;
      y = 0;
    }
  }
  if (!defaultObj.chart.marginTop) defaultObj.chart.marginTop = marg;
  if (!defaultObj.legend.y) defaultObj.legend.y = y;
}

/**
 * Mechanism for passing functions or applied functions to the chart style object
 * @param {string} override - Prefixed refered to a function in chart-hooks.js
 * @param {object} data - Data provided to chart
 * @returns {Function | string} Result of the override or the provided unmatched style
 */
function resolveOverride(override, data) {
  if (typeof override === 'string') {
    if (override.match(/^fn__/)) {
      return chartHooks[override.replace('fn__', '')];
    } else if (override.match(/^hook__/)) {
      return chartHooks[override.replace('hook__', '')](data);
    }
  }
  return override;
}

/**
 * Mutates a style object with entries from the style overrides field
 * @param {object} styles - JSON style overrides
 * @param {object} obj - The object to mutate
 * @param {object} data - The data to provide to the chart
 */
function overrideStyles(styles, obj, data) {
  Object.keys(styles).forEach((key) => {
    const override = resolveOverride(styles[key], data);
    key.split('.').reduce((acc, curr, i, arr) => {
      if (i === arr.length - 1) return (acc[curr] = override);
      if (!acc[curr]) acc[curr] = {};
      return acc[curr];
    }, obj);
  });
}

/**
 * Formats processed series data as expected by Highcharts
 * @param {object} data - Series data in various acceptable formats
 * @returns {object} Correctly formatted series object
 */
function formatSeries(data) {
  const { series } = data;
  if (series) {
    if (!isNaN(series[0])) {
      return [{ data: series }];
    }
    return series;
  }
  if (data.transformed) {
    if (Array.isArray(data.transformed)) {
      return [{ data: data.transformed }];
    }
    return data.transformed;
  }
  return [{ data: data.raw }];
}

/**
 * Makes a tooltip formatter function
 * @param {string} yAxisLabel - Label for the yAxis
 * @returns {Function} The formatter function
 */
function makeFormatter(yAxisLabel) {
  return function () {
    let x = this.x;
    if (Number.isInteger(x) && String(x).length === 13) {
      x = new Date(x);
    }
    if (x instanceof Date) {
      x = chartHooks.getDateString(x);
    }
    let str = `<b>${x}</b><br/>${yAxisLabel}: <b>${this.y.toLocaleString()}</b>`;
    if (this.series && this.series.name) {
      str = `<b>${this.series.name}</b><br/>` + str;
    }
    return str;
  };
}

/**
 * Pulls specified keys from the resolved data object
 * @param {Array} rawData - Array of data from JSON, CSV or directly entered
 * @param {object} meta - The employee who is responsible for the project.
 * @param {string} meta.series - The keys for data to render into the chart.
 * @param {string} meta.xAxisSource - Key or array of categories.
 * @param {string} meta.chartType - The current chart type.
 * @returns {Array} Series data.
 */
function extractSeries(rawData, { series, xAxisSource, chartType }) {
  if (series) {
    if (series.match(/^\[/)) {
      series = JSON.parse(series);
    } else {
      series = [series];
    }

    if (chartType === 'datetime') {
      if (!xAxisSource) xAxisSource = 'x';
    }

    const seriesData = [];

    // array of {name: str, data: arr (maybe of obj)}
    series.forEach((currSeries) => {
      let name = currSeries;
      let key = currSeries;
      if (typeof currSeries === 'object') {
        name = name.label;
        key = key.key;
      }
      const currArr = [];
      const currObj = {
        name,
        data: currArr,
      };
      rawData.forEach((obj) => {
        let d = Number(obj[key]);
        if (chartType === 'datetime') {
          d = {
            x: Number(new Date(obj[xAxisSource])),
            y: d,
          };
        }
        currArr.push(d);
      });
      seriesData.push(currObj);
    });
    return seriesData;
  }
  return null;
}

/**
 * Converts to human readable date from Epoch format.
 * @param {number} date - UNIX timestamp (seconds since Epoch).
 * @returns {string|null} Human readable date string,
 *   or null if supplied timestamp is invalid.
 */
function convertEpochToDateString(date) {
  let humanFriendly = null;
  let month = null;
  let year = null;
  const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  if (
    typeof date === 'number' &&
    date.toString().length >= 12 &&
    date.toString().length <= 13
  ) {
    month = new Date(date).getUTCMonth();
    month = months[month];
    year = new Date(date).getUTCFullYear();

    humanFriendly = month + ' ' + year;
  }

  return humanFriendly;
}

export {
  alignMargin,
  formatSeries,
  makeFormatter,
  overrideStyles,
  extractSeries,
  convertEpochToDateString,
};
