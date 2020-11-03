import styles from './common-styles.js'

const bar = {
  ...styles,
  chart: {
    ...styles.chart,
    type: 'column'
  },
  xAxis: {
    categories: ['a', 'b', 'c'],
    crosshair: true,
    labels: {
      y: 30,
      style: {
        fontSize: '16px'
      }
    }
  }
}

export default bar
