import styles from './line-styles.js';

const datetime = {
  ...styles,
  xAxis: {
    ...styles.xAxis,
    type: 'datetime',
    startOnTick: true,
    labels: {
      ...styles.xAxis.labels,
      format: 'Jan<br/>{value:%Y}'
    },
    tickInterval: 365 * 24 * 3600 * 1000
  }
};

export default datetime;
