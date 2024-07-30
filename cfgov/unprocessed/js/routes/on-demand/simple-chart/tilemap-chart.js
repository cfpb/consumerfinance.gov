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

  defaultObj.tooltip.formatter = function () {
    const label = yAxisLabel ? yAxisLabel + ': ' : '';
    return `<span style="font-weight:600">${
      this.point.name
    }</span><br/>${label}<span style="font-weight:600">${
      Math.round(this.point.value * 10) / 10
    }</span>`;
  };

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
  const data = series[0].data;
  const added = data.map((v) => {
    const val = Math.round(Number(v.value) * 100) / 100;
    if (val <= min) min = val;
    if (val >= max) max = val;
    return {
      ...usLayout[v.name],
      state: v.name,
      value: val,
    };
  });
  min = Math.floor(min);
  max = Math.ceil(max);
  const step = Math.round((max - min) / 5);
  const step1 = min + step;
  const step2 = step1 + step;
  const step3 = step2 + step;
  const step4 = step3 + step;
  const trimTenth = (v) => Math.round((v - 0.1) * 10) / 10;
  return {
    colorAxis: {
      dataClasses: [
        {
          from: min,
          to: step1,
          color: '#addc91',
          name: `${min} - ${trimTenth(step1)}`,
        },
        {
          from: step1,
          to: step2,
          color: '#e2efd8',
          name: `${step1} - ${trimTenth(step2)}`,
        },
        {
          from: step2,
          to: step3,
          color: '#ffffff',
          name: `${step2} - ${trimTenth(step3)}`,
        },
        {
          from: step3,
          to: step4,
          color: '#d6e8fa',
          name: `${step3} - ${trimTenth(step4)}`,
        },
        { from: step4, color: '#7eb7e8', name: `${step4} - ${max}` },
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
