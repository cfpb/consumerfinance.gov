import styles from './common-styles.js';

const line = {
  ...styles,
  plotOptions: {
    ...styles.plotOptions,
    series: {
      marker: {
        enabled: false
      },
      states: {
        hover: {
          halo: null
        }
      }
    }
  },
  xAxis: {
    title: {
      margin: 10,
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
