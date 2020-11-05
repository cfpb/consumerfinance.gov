import styles from './common-styles.js'

const bar = {
  ...styles,
  chart: {
    ...styles.chart,
    type: 'column'
  },
  plotOptions: {
    series: {
      lineWidth: 3,
      states: {
        hover: {
          color: '#addc91'
        }
      },
      color: '#20aa3f'
    }
  },
  xAxis: {
    crosshair: false,
    labels: {
      y: 30,
      style: {
        fontSize: '16px'
      }
    },
    lineColor: '#d2d3d5'
  }
}

export default bar
