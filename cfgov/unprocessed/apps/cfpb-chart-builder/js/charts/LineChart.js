import Highcharts from 'highcharts/highstock';
import accessibility from 'highcharts/modules/accessibility';
import { getFirstNumber } from '../utils/calculation';
import { processNumOriginationsData } from '../utils/process-json';

accessibility(Highcharts);

Highcharts.setOptions({
  lang: {
    rangeSelectorZoom: '',
    thousandsSep: ',',
  },
});

/**
 * _getYAxisLabel - Get the text of the y-axis title.
 * @param {Array} chartData - An array of values to check.
 * @param {string} yAxisLabel - A string to use for the y-axis label.
 * @returns {string} Appropriate y-axis title.
 */
function _getYAxisLabel(chartData, yAxisLabel) {
  if (yAxisLabel) {
    return yAxisLabel;
  }

  let term = 'Number';
  let unit = 'millions';
  const firstChartNumber = getFirstNumber(chartData);

  if (!firstChartNumber) {
    return firstChartNumber;
  }

  if (firstChartNumber % 1000000000 < firstChartNumber) {
    term = 'Volume';
    unit = 'billions';
  }

  return term + ' of originations (in ' + unit + ')';
}

/**
 * _getTickValue - Convert the data point's unit to M or B.
 * @param {number} value - Data point's value
 * @returns {number} Data point's value over million or billion.
 */
function _getTickValue(value) {
  // If it's 0 or borked data gets passed in, return it.
  if (!value) {
    return value;
  }

  if (value % 1000000000 < value) {
    return value / 1000000000 + 'B';
  } else if (value % 10000 < value) {
    return value / 1000000 + 'M';
  }

  return value;
}

class LineChart {
  constructor({ el, description, data, metadata, yAxisLabel }) {
    data = processNumOriginationsData(data[0], metadata);

    const options = {
      chart: {
        className: 'cfpb-chart__small',
        marginTop: 142,
        marginBottom: 100,
        marginLeft: 60,
        marginRight: 20,
        styledMode: true,
        zoomType: 'none',
      },
      description: description,
      credits: false,
      rangeSelector: {
        floating: true,
        selected: 'all',
        height: 35,
        inputEnabled: false,
        verticalAlign: 'bottom',
        buttonPosition: {
          align: 'center',
          x: -64,
        },
        buttonSpacing: 30,
        buttonTheme: {
          // border radius.
          r: 5,
          width: 45,
          height: 45,
        },
        buttons: [
          {
            type: 'year',
            count: 1,
            text: '1y',
          },
          {
            type: 'year',
            count: 3,
            text: '3y',
          },
          {
            type: 'year',
            count: 5,
            text: '5y',
          },
          {
            type: 'all',
            text: 'All',
          },
        ],
      },
      legend: {
        align: 'left',
        enabled: true,
        floating: true,
        layout: 'vertical',
        verticalAlign: 'top',
        useHTML: true,
        x: -16,
        y: -16,
      },
      plotOptions: {
        series: {
          states: {
            hover: {
              enabled: false,
            },
          },
        },
      },
      scrollbar: {
        enabled: false,
      },
      navigator: {
        maskFill: 'rgba(0, 0, 0, 0.05)',
        series: {
          lineWidth: 2,
        },
      },
      xAxis: {
        startOnTick: true,
        tickLength: 5,
        type: 'datetime',
        dateTimeLabelFormats: {
          month: '%b<br/>%Y',
          year: '%b<br/>%Y',
        },
        labels: {
          useHTML: true,
        },
        plotLines: [
          {
            value: data.projectedDate.timestamp,
            label: {
              text:
                'Values after ' + data.projectedDate.label + ' are projected',
              rotation: 0,
              useHTML: true,
              x: -300,
              y: -126,
            },
          },
        ],
      },
      yAxis: {
        showLastLabel: true,
        opposite: false,
        title: {
          text: _getYAxisLabel(data.adjusted, yAxisLabel),
          align: 'high',
          // useHTML true value is needed to set width beyond chart marginTop.
          useHTML: true,
          rotation: 0,
          offset: 0,
          reserveSpace: false,
          x: 300,
          y: -33,
        },
        labels: {
          formatter: function () {
            return _getTickValue(this.value);
          },
          y: 4,
        },
      },
      tooltip: {
        animation: false,
        useHTML: true,
        shape: 'square',
        shared: true,
        split: false,
        padding: 10,
      },
      series: [
        {
          name: 'Seasonally adjusted',
          data: data.adjusted,
          legendIndex: 1,
          tooltip: {
            valueDecimals: 0,
          },
          zoneAxis: 'x',
          zones: [
            {
              value: data.projectedDate.timestamp,
            },
          ],
        },
        {
          name: 'Unadjusted',
          data: data.unadjusted,
          legendIndex: 2,
          tooltip: {
            valueDecimals: 0,
          },
          zoneAxis: 'x',
          zones: [
            {
              value: data.projectedDate.timestamp,
            },
          ],
        },
      ],
      responsive: {
        rules: [
          {
            condition: {
              // Chart width, not window width.
              minWidth: 650,
            },
            // Add more left margin space for vertical label on large screens.
            chartOptions: {
              chart: {
                className: 'cfpb-chart__large',
                marginTop: 135,
                marginBottom: 60,
                marginLeft: 80,
              },
              xAxis: {
                labels: {
                  y: 26,
                },
                plotLines: [
                  {
                    value: data.projectedDate.timestamp,
                    label: {
                      text:
                        'Values after ' +
                        data.projectedDate.label +
                        ' are projected',
                      rotation: 0,
                      useHTML: true,
                      x: -300,
                      y: -20,
                    },
                  },
                ],
              },
              yAxis: {
                title: {
                  align: 'middle',
                  rotation: 270,
                  x: -40,
                  y: 0,
                },
              },
              rangeSelector: {
                verticalAlign: 'top',
                buttonPosition: {
                  align: 'left',
                  x: -40,
                  y: -104,
                },
                buttonSpacing: 10,
                buttonTheme: {
                  // border radius.
                  r: 5,
                  width: 45,
                  height: 28,
                },
                x: 0,
                y: 0,
              },
              legend: {
                align: 'center',
                x: 200,
                y: -16,
              },
            },
          },
        ],
      },
    };

    this.chart = Highcharts.stockChart(el, options, function (chart) {
      // label(str, x, y, shape, anchorX, anchorY, useHTML, baseline, className)
      chart.renderer
        .label(
          'Select time range',
          null,
          null,
          null,
          null,
          null,
          true,
          null,
          'range-selector-label',
        )
        .add();
    });

    return this.chart;
  }
}

export default LineChart;
