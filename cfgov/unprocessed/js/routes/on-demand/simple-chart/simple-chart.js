/* eslint-disable */
// Polyfill Promise for IE11
import 'core-js/features/promise'

import Highcharts from 'highcharts/highstock'
/* eslint-disable-next-line */
import accessibility from 'highcharts/modules/accessibility'
import fetch from 'cross-fetch'
import chartHooks from './chart-hooks.js'
import defaultLine from './line-styles.js'
import defaultDatetime from './datetime-styles.js'
import defaultBar from './bar-styles.js'

accessibility(Highcharts)

function fetchData(url) {
  return fetch(url).then(res => res.json())
}

function getDefaultChartObject(type) {
  switch (type) {
    case 'bar':
      return defaultBar
    case 'datetime':
      return defaultDatetime
    case 'line':
      return defaultLine
  }
  throw new Error('Unknown chart type specified')
}

function makeChartOptions(
  data,
  { chartType, styleOverrides, description, xAxisLabel, yAxisLabel }
) {
  const defaultObj = JSON.parse(
    JSON.stringify(getDefaultChartObject(chartType))
  )

  if (styleOverrides) {
    const styles = JSON.parse(styleOverrides)
    Object.keys(styles).forEach(key => {
      const override = resolveOverride(styles[key], data)
      key.split('.').reduce((acc, curr, i, arr) => {
        if (i === arr.length - 1) return (acc[curr] = override)
        if (!acc[curr]) acc[curr] = {}
        return acc[curr]
      }, defaultObj)
    })
  }

  defaultObj.title = { text: undefined }
  defaultObj.series = [{ data }]
  defaultObj.description = description
  defaultObj.yAxis.title.text = yAxisLabel
  if (xAxisLabel) defaultObj.xAxis.title.text = xAxisLabel

  return defaultObj
}

function resolveOverride(override, data) {
  if (typeof override === 'string') {
    if (override.match(/^fn__/)) {
      return chartHooks[override.replace('fn__', '')]
    } else if (override.match(/^hook__/)) {
      return chartHooks[override.replace('hook__', '')](data)
    }
  }
  return override
}

function resolveData(source) {
  if (source.match(/^http/i)) {
    return fetchData(source)
  } else {
    return Promise.resolve(JSON.parse(source))
  }
}

function buildCharts() {
  const charts = [...document.getElementsByClassName('simple-chart-target')]
  charts.forEach(buildChart)
}

function buildChart(chart) {
  const { source, transform } = chart.dataset

  resolveData(source.trim()).then(d => {
    const data =
      transform && chartHooks[transform] ? chartHooks[transform](d) : d

    Highcharts.chart(chart, makeChartOptions(data, chart.dataset))
  })
}

buildCharts()
