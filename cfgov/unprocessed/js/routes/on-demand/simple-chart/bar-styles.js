import styles from './common-styles.js';

const bar = {
  ...styles,
  chart: {
    ...styles.chart,
    type: 'column'
  },
  plotOptions: {
    series: {
      states: {
        hover: {
          color: '#addc91'
        }
      },
      color: '#20aa3f'
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
    crosshair: false,
    labels: {
      y: 30,
      style: {
        color: '#5a5d61',
        fontSize: '16px'
      }
    },
    lineColor: '#d2d3d5'
  }
};

export default bar;
