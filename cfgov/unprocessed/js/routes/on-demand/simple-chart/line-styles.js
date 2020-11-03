import styles from './common-styles.js'

const line = {
  ...styles,
  xAxis: {
    type: 'datetime',
    crosshair: true,
    startOnTick: true,
    labels: {
      format: 'Jan<br/>{value:%Y}',
      y: 30,
      style: {
        fontSize: '16px'
      }
    },
    tickInterval: 365 * 24 * 3600 * 1000
  }
}
export default line
