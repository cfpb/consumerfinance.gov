import Highcharts from 'highcharts/highstock';
import Papa from 'papaparse';
import accessibility from 'highcharts/modules/accessibility';
import cloneDeep from 'lodash.clonedeep';
import chartHooks from './chart-hooks.js';
import defaultBar from './bar-styles.js';
import defaultDatetime from './datetime-styles.js';
import defaultLine from './line-styles.js';
import tilemapChart from './tilemap-chart.js';
import {
  alignMargin,
  convertEpochToDateString,
  extractSeries,
  formatSeries,
  makeFormatter,
  overrideStyles,
} from './utils.js';
import { initFilters } from './data-filters.js';

accessibility(Highcharts);

Highcharts.setOptions({
  lang: {
    numericSymbols: ['K', 'M', 'B'],
  },
});

const msInDay = 24 * 60 * 60 * 1000;
const promiseCache = {};

/**
 * Fetches JSON data.
 * @param {string} url - The url to fetch data from.
 * @param {boolean} isCSV - Whether the data to fetch is a CSV.
 * @returns {Promise} Promise that resolves to JSON data.
 */
function fetchData(url, isCSV) {
  const promise = promiseCache[url];
  if (promise) return promise;

  const p = fetch(url).then((res) => {
    let prom;
    if (isCSV) prom = res.text();
    else prom = res.json();

    return prom.then((d) => {
      if (isCSV) {
        /* Excel can put quotes at the start of our # or // comments
           This strips those quotes */
        d = d.replace(/^"(#|\/\/)|(\n)"(#|\/\/)/g, '$1$2$3');
        d = Papa.parse(d, {
          header: true,
          comments: true,
          skipEmptyLines: true,
        }).data;
      }
      return Promise.resolve(d);
    });
  });

  promiseCache[url] = p;
  return p;
}

/**
 * Selects appropriate chart import style.
 * @param {string} type - The chart type as defined in the organism.
 * @returns {object} The appropriately loaded style object.
 */
function getDefaultChartObject(type) {
  switch (type) {
    case 'bar':
      return defaultBar;
    case 'datetime':
      return defaultDatetime;
    case 'line':
      return defaultLine;
    default:
      throw new Error('Unknown chart type specified');
  }
}

/**
 * Overrides default chart options using provided Wagtail configurations.
 * @param {object} data - The data to provide to the chart.
 * @param {object} dataAttributes - Data attributes passed to the chart target node.
 * @returns {object} The configured style object.
 */
function makeChartOptions(data, dataAttributes) {
  const {
    chartType,
    styleOverrides,
    description,
    xAxisSource,
    xAxisLabel,
    yAxisLabel,
    projectedMonths,
    defaultSeries,
  } = dataAttributes;
  let defaultObj = cloneDeep(getDefaultChartObject(chartType));

  if (styleOverrides) {
    overrideStyles(JSON.parse(styleOverrides), defaultObj, data);
  }

  if (xAxisSource && chartType !== 'datetime') {
    defaultObj.xAxis.categories = getCategoriesFromXAxisSource(
      data.raw,
      xAxisSource,
    );
  }

  defaultObj.series = formatSeries(data);

  defaultObj.title = { text: undefined };
  defaultObj.accessibility.description = description;
  defaultObj.yAxis.title.text = yAxisLabel;

  if (!yAxisLabel && chartType === 'datetime') {
    defaultObj.rangeSelector.buttonPosition.x = -50;
  }

  if (xAxisLabel) defaultObj.xAxis.title.text = xAxisLabel;

  if (!defaultObj.tooltip.formatter && yAxisLabel) {
    defaultObj.tooltip.formatter = makeFormatter(yAxisLabel);
  }

  if (defaultObj.series.length === 1) {
    defaultObj.plotOptions.series = {
      ...defaultObj.plotOptions.series,
      events: {
        legendItemClick: function () {
          return false;
        },
      },
    };
  } else {
    defaultObj.legend.title = {
      text: '(Click to show/hide data)',
      style: {
        fontStyle: 'italic',
        fontWeight: 'normal',
        fontSize: '14px',
        color: '#666',
      },
    };
  }

  if (projectedMonths > 0) {
    defaultObj = addProjectedMonths(defaultObj, projectedMonths);
    defaultObj.legend.y = -10;
    defaultObj.chart.marginTop = 180;
  }

  if (defaultSeries === 'False') {
    defaultObj.series = defaultObj.series.map((singluarSeries, i) => {
      // Skip the first series
      if (i > 0) {
        singluarSeries.visible = false;
      }
      return singluarSeries;
    });
  }

  alignMargin(defaultObj, chartType);

  return defaultObj;
}

/**
 * Adds projected months to config object for Highcharts.
 * @param {object} chartObject - The config object for Highcharts.
 * @param {number} numMonths - The number of months input into wagtail field.
 * @returns {object} The config object with projected months.
 */
function addProjectedMonths(chartObject, numMonths) {
  // Convert the number of projected months into a timestamp
  const lastChartDate = chartObject.series[0].data.at(-1).x;

  // Convert lastChartDate from months to milliseconds for Epoch format
  const convertedProjectedDate = lastChartDate - numMonths * 30 * msInDay;
  const projectedDate = {
    humanFriendly: convertEpochToDateString(convertedProjectedDate),
    timestamp: convertedProjectedDate,
  };

  /* Add a vertical line and some explanatory text at the starting
     point of the projected data */
  chartObject.xAxis.plotLines = [
    {
      value: projectedDate.timestamp,
    },
  ];

  // Save a reference to the common styles render event
  const commonRenderCallback = chartObject.chart.events.render;

  // Add a new render event that will draw the projected data label
  chartObject.chart.events.render = function () {
    commonRenderCallback.apply(this, arguments);

    if (this.projectedMonthsLabel) this.projectedMonthsLabel.destroy();
    this.projectedMonthsLabel = this.renderer
      .text(
        `Values after ${projectedDate.humanFriendly} are projected`,
        this.plotWidth - 218,
        this.plotWidth < 450 ? 120 : 165,
      )
      .css({
        fontSize: '15px',
      })
      .add();
  };

  /* Add a zone to each series with a dotted line starting
     at the projected data starting point */
  chartObject.series = chartObject.series.map((singluarSeries) => {
    let projectedStyle = { dashStyle: 'dot' };
    if (chartObject.chart?.type === 'column') {
      projectedStyle = { color: '#addc91' };
    }
    singluarSeries.zoneAxis = 'x';
    singluarSeries.zones = [
      {
        value: projectedDate.timestamp,
      },
      projectedStyle,
    ];
    return singluarSeries;
  });
  return chartObject;
}

/**
 * Resolves provided x axis or series data
 * @param {Array} rawData - Data provided to the chart
 * @param {string} key - Key to resolve from data, or categories provided directly
 * @returns {Array} Resolved array of data
 */
function getCategoriesFromXAxisSource(rawData, key) {
  // Array provided directly
  if (key.match(/^\[/)) {
    return JSON.parse(key);
  }
  return rawData.map((d) => d[key]);
}

/**
 * Selects whether to use inline data or fetch data that matches a url
 * @param {string} source - Source provided from wagtail
 * @returns {Promise} Promise resolving to either fetched JSON or parsed inline JSON
 */
function resolveData(source) {
  if (source.match(/^http/i) || source.match(/^\//)) {
    const isCSV = Boolean(source.match(/csv$/i));
    return fetchData(source, isCSV);
  }
  return Promise.resolve(JSON.parse(source));
}

/**
 * Initializes every chart on the page
 */
function buildCharts() {
  const charts = document.getElementsByClassName('o-simple-chart');
  for (let i = 0; i < charts.length; i++) {
    buildChart(charts[i]);
  }
}

/**
 *
 * @param {string} rawTransform - The string input into the transform field
 * @returns {object} transform object with function and args
 */
function getTransformObject(rawTransform = '') {
  const parsed = rawTransform.split('___');
  return {
    transformMethod: parsed[0],
    args: parsed.slice(1),
  };
}

/**
 * Initializes a chart
 * @param {object} chartNode - The DOM node of the current chart.
 */
function buildChart(chartNode) {
  const target = chartNode.getElementsByClassName('o-simple-chart__target')[0];
  const dataAttributes = target.dataset;
  const { source, transform, chartType } = dataAttributes;

  resolveData(source.trim()).then((raw) => {
    const { transformMethod, args } = getTransformObject(transform);
    const transformed =
      transformMethod && chartHooks[transformMethod]
        ? chartHooks[transformMethod](raw, ...args)
        : null;

    const series = extractSeries(transformed || raw, dataAttributes);

    const data = {
      raw,
      series,
      transformed,
    };

    let chart;

    if (chartType === 'tilemap') {
      chart = tilemapChart.init(chartNode, target, data, dataAttributes);
    } else {
      chart = Highcharts.chart(target, makeChartOptions(data, dataAttributes));

      initFilters(dataAttributes, chartNode, chart, data);
    }
    // Make sure chart is displayed properly on print
    window.matchMedia('print').addListener(function () {
      chart.reflow();
    });
  });
}

buildCharts();
