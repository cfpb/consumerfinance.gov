import styles from './common-styles.js'

const line = {
  ...styles,
  xAxis: {
    lineColor: '#d2d3d5',
    crosshair: true,
    labels: {
      y: 30,
      style: {
        fontSize: '16px'
      }
    }
  }
}

export default line
