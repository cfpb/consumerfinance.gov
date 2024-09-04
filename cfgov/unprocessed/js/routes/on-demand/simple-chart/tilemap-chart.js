import Highmaps from 'highcharts/highmaps';
import tilemap from 'highcharts/modules/tilemap';
import cloneDeep from 'lodash.clonedeep';
import defaultTilemap from './tilemap-styles.js';
import usLayout from './us-layout.js';
import { alignMargin, formatSeries, overrideStyles } from './utils.js';

tilemap(Highmaps);

/**
 * Overrides default chart options using provided Wagtail configurations
 * @param {object} data - The data to provide to the chart
 * @param {object} dataAttributes - Data attributes passed to the chart target node
 * @returns {object} The configured style object
 */
function makeTilemapOptions(data, dataAttributes) {
  const { chartType, styleOverrides, description, yAxisLabel } = dataAttributes;

  let defaultObj = cloneDeep(defaultTilemap);

  if (styleOverrides) {
    overrideStyles(styleOverrides, defaultObj, data);
  }

  const formattedSeries = formatSeries(data);

  if (formattedSeries.length !== 1) {
    /* eslint-disable-next-line no-console */
    return console.error('Tilemap only supports a single data series.');
  }

  defaultObj = {
    ...defaultObj,
    ...getMapConfig(formattedSeries),
  };

  if (!defaultObj.tooltip.formatter) {
    defaultObj.tooltip.formatter = function () {
      const label = yAxisLabel ? yAxisLabel + ': ' : '';
      return `<span style="font-weight:600">${
        this.point.label
      }</span><br/>${label}<span style="font-weight:600">${
        Math.round(this.point.value * 10) / 10
      }</span>`;
    };
  }

  defaultObj.title = { text: undefined };
  defaultObj.accessibility.description = description;
  defaultObj.yAxis.title.text = yAxisLabel;

  alignMargin(defaultObj, chartType);

  return defaultObj;
}

/**
 * Makes a legend for the tilemap
 * @param {object} node - The chart node
 * @param {object} data - The data object
 * @param {string} legendTitle - The legend title
 */
function updateTilemapLegend(node, data, legendTitle) {
  const classes = data.colorAxis.dataClasses;
  const legend = node.parentNode.getElementsByClassName(
    'o-simple-chart__tilemap-legend',
  )[0];
  legend.innerHTML = '';
  const colors = [];
  const labels = [];
  classes.forEach((v) => {
    const color = document.createElement('div');
    const label = document.createElement('div');
    color.className = 'legend-color';
    label.className = 'legend-label';
    color.style.backgroundColor = v.color;
    label.innerText = v.name;
    colors.push(color);
    labels.push(label);
  });
  if (legendTitle) {
    const title = document.createElement('p');
    title.className = 'legend-title';
    title.innerText = legendTitle;
    legend.appendChild(title);
  }
  colors.forEach((v) => legend.appendChild(v));
  labels.forEach((v) => legend.appendChild(v));
}

/**
 *
 * @param {number} v - A given step min or max
 * @returns {Array} - An array with the step adjusted to label with a millions value or not
 */
function mLabel(v) {
  if (v >= 1e6) {
    return [v / 1e6, 'M'];
  }
  return [v, ''];
}

/**
 *
 * @param {number} v - Upper end of a given step
 * @returns {number} - The step trimmed so the bins don't overlap
 */
function trimTenth(v) {
  return Math.round((v - 0.1) * 10) / 10;
}

/**
 *
 * @param {number} s1 - step min
 * @param {number} s2 - step max
 * @param {boolean} isLast - whether we're operating on the last data class
 * @returns {string} formatted legend label
 */
function formatLegendValues(s1, s2, isLast) {
  const f1 = mLabel(s1);
  const f2 = mLabel(s2);
  return `${f1[0]}${f1[1]} - ${isLast ? f2[0] : trimTenth(f2[0])}${f2[1]}`;
}

/**
 *
 * @param {number} s1 - step min
 * @param {number} s2 - step max
 * @param {string} color - hex color for legend class
 * @param {boolean} isLast - whether we're operating on the last data class
 * @returns {object} - dataClass object for highcharts
 */
function makeDataClass(s1, s2, color, isLast = 0) {
  return {
    from: s1,
    to: s2,
    color,
    name: formatLegendValues(s1, s2, isLast),
  };
}

/**
 *
 * @param {number} v - The raw number to get the divisor for
 * @returns {number} a divisor which can round the number to its largest digit
 */
function makeDivisor(v) {
  const precision = Math.floor(v).toString().length;
  return Math.pow(10, precision - 1);
}

/**
 * Generates a config object to be added to the chart config
 * @param {Array} series - The formatted series data
 * @returns {Array} series data with a geographic component added
 */
function getMapConfig(series) {
  let min = Infinity;
  let max = -Infinity;
  let dataMin = Infinity;
  const data = series[0].data;

  data.forEach((v) => {
    if (v.value < dataMin) dataMin = v.value;
  });

  const added = data.map((v) => {
    const val = Math.round(Number(v.value) * 100) / 100;
    if (val <= min) min = val;
    if (val >= max) max = val;
    return {
      ...usLayout[v.name],
      ...v,
      value: val,
    };
  });

  const divisor = makeDivisor(min);
  min = Math.floor(min / divisor) * divisor;
  max = Math.ceil(max / divisor) * divisor;

  let step = (max - min) / 5;
  const stepDivisor = makeDivisor(step);
  step = Math.round(step / stepDivisor) * stepDivisor;

  const step1 = Math.round(min + step);
  const step2 = Math.round(step1 + step);
  const step3 = Math.round(step2 + step);
  const step4 = Math.round(step3 + step);

  return {
    colorAxis: {
      dataClasses: [
        makeDataClass(min, step1, '#f1f9ed'),
        makeDataClass(step1, step2, '#d4eac6'),
        makeDataClass(step2, step3, '#addc91'),
        makeDataClass(step3, step4, '#48b753'),
        makeDataClass(step4, max, '#1e9642', 1),
      ],
    },
    series: [{ clip: false, data: added }],
  };
}

/**
 * Initializes a tilemap chart
 * @param {object} chartNode - The DOM node of the current chart
 * @param {object} target - The node to initialize the chart in
 * @param {object} data - The data to provide to the chart
 * @param {object} dataAttributes - Data attributes passed to the chart target node
 * @returns {object} The initialized chart object
 */
function init(chartNode, target, data, dataAttributes) {
  const { yAxisLabel } = dataAttributes;
  const tilemapOptions = makeTilemapOptions(data, dataAttributes);
  const chart = Highmaps.mapChart(target, tilemapOptions);

  const legend = target.parentNode.getElementsByClassName(
    'o-simple-chart__tilemap-legend',
  )[0];
  legend.style.display = 'block';
  updateTilemapLegend(target, tilemapOptions, yAxisLabel);

  /**
   * Fixes tilemap clipping
   */
  function fixViewbox() {
    const chartSVG = target.getElementsByClassName('highcharts-root')[0];
    const width = chartSVG.width.animVal.value;
    const height = chartSVG.height.animVal.value;
    chartSVG.setAttribute('viewBox', `-4 0 ${width + 8} ${height + 1}`);
  }

  window.addEventListener('resize', fixViewbox);
  fixViewbox();
  setTimeout(fixViewbox, 500);

  return chart;
}

const tilemapChart = { init };

export default tilemapChart;
