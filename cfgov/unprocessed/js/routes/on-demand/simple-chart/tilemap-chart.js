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
 * @param {string } legendTitle - The legend title
 */
function updateTilemapLegend(node, data, legendTitle) {
  const classes = data.colorAxis.dataClasses;
  console.log('c', classes);
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
  console.log(dataMin);
  //get precision and round
  // floor, to string length to get digits
  // start of step one is  pow(10, digits -1)

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
  min = Math.floor(min);
  max = Math.ceil(max);

  const precision = Math.floor(min).toString().length;
  const divisor = Math.pow(10, precision - 1);

  /**
   *
   * @param a
   */
  function r(a) {
    return Math.round(a / divisor) * divisor;
  }

  const trimTenth = (v) => Math.round((v - 0.1) * 10) / 10;

  /**
   *
   * @param v
   */
  function mLabel(v) {
    if (v >= 1e6) {
      return [v / 1e6, 'M'];
    }
    return [v, ''];
  }
  /**
   *
   * @param s1
   * @param s2
   * @param isLast
   */
  function formatLegendValues(s1, s2, isLast) {
    const f1 = mLabel(s1);
    const f2 = mLabel(s2);
    return `${f1[0]}${f1[1]} - ${isLast ? f2[0] : trimTenth(f2[0])}${f2[1]}`;
  }

  /**
   *
   * @param s1
   * @param s2
   * @param color
   * @param isLast
   */
  function makeDataClass(s1, s2, color, isLast = 0) {
    return {
      from: s1,
      to: s2,
      color,
      name: formatLegendValues(s1, s2, isLast),
    };
  }

  min = r(min);
  max = r(max);
  const step = Math.round((max - min) / 5);

  console.log(step, min, max);

  const step1 = r(min + step);
  const step2 = r(step1 + step);
  const step3 = r(step2 + step);
  const step4 = r(step3 + step);
  console.log(step1, step2, step3, step4);
  return {
    colorAxis: {
      dataClasses: [
        makeDataClass(min, step1, '#addc91'),
        makeDataClass(step1, step2, '#e2efd8'),
        makeDataClass(step2, step3, '#ffffff'),
        makeDataClass(step3, step4, '#d6e8fa'),
        makeDataClass(step4, max, '#7eb7e8', 1),
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
