import Highmaps from 'highcharts/highmaps';
import tilemap from 'highcharts/modules/tilemap';
import cloneDeep from 'lodash.clonedeep';
import defaultTilemap from './tilemap-styles.js';
import usLayout from './us-layout.js';
import populations from './populations.js';
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

  let styles = {};
  if (styleOverrides) {
    styles = JSON.parse(styleOverrides);
    overrideStyles(styles, defaultObj, data);
  }

  const formattedSeries = formatSeries(data);

  if (formattedSeries.length !== 1) {
    /* eslint-disable-next-line no-console */
    return console.error('Tilemap only supports a single data series.');
  }

  defaultObj = {
    ...defaultObj,
    ...getMapConfig(formattedSeries, defaultObj, styles.perCapita),
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
  if (data.perCapita) {
    labels[0].innerText = 'Less';
    labels[labels.length - 1].innerText = 'More';
    for (let i = 1; i < labels.length - 1; i++) {
      labels[i].innerText = '\xa0';
    }
  }
  const grid = document.createElement('div');
  grid.className = 'legend-grid';
  grid.style.gridTemplateColumns = `repeat(${classes.length}, 1fr)`;
  legend.appendChild(grid);

  colors.forEach((v) => grid.appendChild(v));
  labels.forEach((v) => grid.appendChild(v));
  legend.style.display = 'block';
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
  return `${f1[0]}${f1[1]} to ${isLast ? f2[0] : trimTenth(f2[0])}${f2[1]}`;
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
 * @returns {number} a divisor which can round the number to its largest digit
 */
function makeDivisor() {
  return 10;
}

/**
 * Generates a config object to be added to the chart config
 * @param {Array} series - The formatted series data
 * @param {object} defaultObj - The style object with overrides applied
 * @param {boolean} perCapita - Whether data should be perCapita
 * @returns {Array} series data with a geographic component added
 */
function getMapConfig(series, defaultObj, perCapita) {
  let min = Infinity;
  let max = -Infinity;
  let dataMin = Infinity;
  let data = series[0].data;
  if (perCapita) {
    data = data.map((v) => {
      return {
        ...v,
        perCapita: v.value / populations[v.name],
      };
    });
  }

  data.forEach((v) => {
    const val = perCapita ? v.perCapita : v.value;
    if (val < dataMin) dataMin = val;
  });

  const added = data.map((v) => {
    const val =
      Math.round(Number(perCapita ? v.perCapita : v.value) * 100) / 100;
    if (val <= min) min = val;
    if (val >= max) max = val;
    return {
      ...usLayout[v.name],
      ...v,
      value: val,
    };
  });

  const divisor = makeDivisor();
  min = Math.floor(min / divisor) * divisor;
  max = Math.ceil(max / divisor) * divisor;

  let step = (max - min) / 5;
  const stepDivisor = makeDivisor();
  step = Math.round(step / stepDivisor) * stepDivisor;

  const step1 = Math.round(min + step);
  const step2 = Math.round(step1 + step);
  const step3 = Math.round(step2 + step);
  const step4 = Math.round(step3 + step);

  return {
    colorAxis: {
      dataClasses: defaultObj.dataClasses
        ? defaultObj.dataClasses
        : [
            makeDataClass(min, step1, '#7eb7e8'),
            makeDataClass(step1, step2, '#d6e8fa'),
            makeDataClass(step2, step3, '#ffffff'),
            makeDataClass(step3, step4, '#e2efd8'),
            makeDataClass(step4, max, '#addc91', 1),
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
