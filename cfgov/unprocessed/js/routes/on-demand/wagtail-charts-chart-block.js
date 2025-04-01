/* eslint-disable no-undef */
import pattern from 'patternomaly';

const white60 = 'rgba(255, 255, 255, 0.6)';
// This is the gray from the CFPB DS.
const gray = '#5a5d61';

/**
 * Set default text color to a dark gray.
 *
 * https://www.chartjs.org/docs/latest/general/colors.html
 */
Chart.defaults.color = gray;

/**
 * Takes an array of Chart.js datasets and returns a new array
 * with a different line pattern assigned to each dataset's
 * borderDash property.
 *
 * The first line pattern is solid, the second is dashed,
 * the third is dotted and all subsequent patterns are dashed
 * with an increasingly thicker line.
 * @param {Array} datasets - Array of Chart.js datasets
 * @returns {Array} Array of Chart.js datasets with borderDash property set
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
 * Takes an array of Chart.js datasets and returns a new array
 * with a different pattern assigned to each dataset's
 * backgroundColor property.
 *
 * Patterns are from the patternomaly library.
 * @param {Array} datasets - List of Chart.js datasets.
 * @returns {Array} List of Chart.js datasets with backgroundColor property set.
 *
 * https://www.chartjs.org/docs/latest/general/colors.html#patterns-and-gradients
 * https://github.com/ashiguruma/patternomaly
 */
const patternizeChartBars = (datasets) => {
  const patterns = [
    'dot',
    'diagonal',
    'dash',
    'cross-dash',
    'zigzag-vertical',
    'dot-dash',
    'plus',
    'cross',
    'disc',
    'ring',
    'line',
    'line-vertical',
    'weave',
    'zigzag',
    'diagonal-right-left',
    'square',
    'box',
    'triangle',
    'triangle-inverted',
    'diamond',
    'diamond-box',
  ];
  return datasets.map((dataset, i) => {
    dataset.backgroundColor = dataset.data.map(() => {
      // First pattern is just the solid color.
      if (i === 0)
        return Array.isArray(dataset.backgroundColor)
          ? dataset.backgroundColor[0]
          : dataset.backgroundColor;
      return pattern.draw(
        patterns[i - 1],
        dataset.backgroundColor,
        white60,
        10,
      );
    });
    return dataset;
  });
};

/**
 * Change the default Chart.js tooltip options.
 */
const tooltipOptions = {
  yAlign: 'bottom',
  displayColors: false,
};

/**
 * Define a Chart.js plugin for our CFPB customizations.
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

    if (chart.config.type === 'bar') {
      patternizeChartBars(chart.config.data.datasets);
    }

    chart.update();
  },
};

Chart.register(ChartjsPluginStacked100.default);
Chart.register({ ChartjsPluginCFPB });
