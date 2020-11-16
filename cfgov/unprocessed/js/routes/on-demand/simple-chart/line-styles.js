import styles from './common-styles.js';

const line = {
  ...styles,
  xAxis: {
    title: {
      y: 12,
      style: {
        color: '#5a5d61'
      }
    },
    lineColor: '#d2d3d5',
    crosshair: true,
    labels: {
      y: 30,
      style: {
        color: '#5a5d61',
        fontSize: '16px'
      }
    }
  }
};

export default line;
