/* eslint-disable */
// Polyfill Promise for IE11
import 'core-js/features/promise'

import Highcharts from 'highcharts/highstock'
/* eslint-disable-next-line */
import accessibility from 'highcharts/modules/accessibility'
import fetch from 'cross-fetch'
import chartHooks from './chart-hooks.js'
import defaultObject from './chart-styles.js'

function fetchData(url) {
  return fetch(url).then(res => res.json())
}

function makeChartOptions(data, styleOverrides, description, yAxisLabel) {
  const defaultObj = JSON.parse(JSON.stringify(defaultObject))

  if (styleOverrides) {
    const styles = JSON.parse(styleOverrides)
    Object.keys(styles).forEach(key => {
      const override = resolveOverride(styles[key])
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

  return defaultObj
}

function resolveOverride(override) {
  if (typeof override === 'string' && override.match(/^hook__/)) {
    return chartHooks[override.replace('hook__', '')]
  }
  return override
}

function buildCharts() {
  const charts = [...document.getElementsByClassName('simple-chart-target')]
  charts.forEach(buildChart)
}

function buildChart(chart) {
  const {
    source,
    transform,
    styleOverrides,
    description,
    yAxisLabel
  } = chart.dataset

  fetchData(source).then(d => {
    const data =
      transform && chartHooks[transform] ? chartHooks[transform](d) : d

    Highcharts.chart(
      chart,
      makeChartOptions(data, styleOverrides, description, yAxisLabel)
    )
  })
}

buildCharts()
