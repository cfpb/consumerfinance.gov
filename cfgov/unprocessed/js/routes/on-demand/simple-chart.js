/* eslint-disable */
// Polyfill Promise for IE11
import 'core-js/features/promise'

import Highcharts from 'highcharts/highstock'
/* eslint-disable-next-line */
import accessibility from 'highcharts/modules/accessibility'
import fetch from 'cross-fetch'

const yAxis = {
  label: 'Dollars in billions'
}

fetch('https://files.consumerfinance.gov/data/enforcement/relief.json')
  .then(res => res.json())
  .then(d => buildChart(d))

function buildChart(data) {
  const hook = document.getElementsByClassName('simple-chart')[0]
  Highcharts.chart(hook, {
    chart: {
      style: {
        fontFamily: '"Avenir Next", Arial, sans-serif',
        lineHeight: 1.5
      }
    },
    title: {
      text: undefined
    },
    description: 'Something',
    credits: false,
    colors: ['#20aa3f'],
    legend: {
      enabled: false
    },
    scrollbar: {
      enabled: false
    },
    plotOptions: {
      series: {
        lineWidth: 1.5,
        states: {
          hover: {
            enabled: false
          }
        }
      }
    },
    tooltip: {
      animation: false,
      shape: 'square',
      shared: true,
      split: false,
      padding: 10,
      useHTML: true,
      style: {
        pointerEvents: 'auto'
      },
      formatter: function() {
        const { x, y, name, relief, url } = this.points[0].point.options
        const total =
          y > 1e9
            ? `${(y / 1e9).toFixed(1)} billion`
            : `${(y / 1e6).toFixed(1)} million`
        return (
          `<div style="margin-bottom: 0.5em;"><span style="font-weight: 500">${new Date(
            x
          ).toLocaleDateString('en-US')}</span><br/>` +
          `Total relief to date: <span style="font-weight: 500">$${total}</span></div>` +
          `<a rel="noopener noreferrer" target="_blank" href="${url}" style="display: block; max-width: 200px; text-decoration-style: dotted; text-overflow: ellipsis; overflow:hidden;">${name}</a>` +
          `Relief from action: <span style="font-weight: 500">$${relief}</span>`
        )
      }
    },
    xAxis: {
      type: 'datetime',
      crosshair: true,
      labels: {
        format: '{value:%Y}'
      },
      tickInterval: 365 * 24 * 3600 * 1000
    },
    yAxis: {
      title: {
        text: yAxis.label,
        margin: 25
      },
      labels: {
        formatter: function() {
          return `$${Math.round(this.value / 1e9)}`
        }
      }
    },
    series: [
      {
        name: 'Consumer Relief',
        data
      }
    ],
    responsive: {
      rules: [
        {
          condition: {
            maxWidth: 600
          },
          chartOptions: {
            subtitle: {
              widthAdjust: 0
            }
          }
        }
      ]
    }
  })
}
