/* eslint-disable no-undef */

/**
 * Set default text color to a dark gray
 *
 * https://www.chartjs.org/docs/latest/general/colors.html
 */
Chart.defaults.color = '#5a5d61';

/**
 * Takes an array of Chart.js datasets and returns a new array
 * with a different line pattern for each dataset.
 *
 * The first line pattern is solid, the second is dashed,
 * the third is dotted and all subsequent patterns are dashed
 * with an increasingly thicker line.
 *
 * @param {array} datasets - Array of Chart.js datasets
 * @returns {array} Array of Chart.js datasets with borderDash property set
 *
 * https://www.chartjs.org/docs/latest/samples/line/styling.html
 * https://www.chartjs.org/docs/latest/configuration/#dataset-configuration
 * https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/setLineDash
 */
const patternizeChartLines = (datasets) => {
  const DASH_THICKNESS = 5;
  const DASH_PATTERNS = [
    [0, 0], // solid
    [DASH_THICKNESS, 2], // dashed
    [2, 1], // dotted
  ];
  return datasets.map((dataset, i) => {
    dataset.borderDash = DASH_PATTERNS[i] || [DASH_THICKNESS * i, 2];
    return dataset;
  });
};

/**
 * Change the default Chart.js tooltip options
 */
const tooltipOptions = {
  yAlign: 'bottom',
  displayColors: false,
};

/**
 * Define a Chart.js plugin for our CFPB customizations
 *
 * https://www.chartjs.org/docs/latest/developers/plugins.html
 */
const ChartjsPluginCFPB = {
  id: 'cfpb-charts',
  beforeInit: (chart) => {
    chart.config.options.plugins.tooltip = tooltipOptions;

    if (chart.config.type === 'line') {
      patternizeChartLines(chart.config.data.datasets);
    }

    chart.update();
  },
};

Chart.register(ChartjsPluginStacked100.default);
Chart.register({ ChartjsPluginCFPB });
