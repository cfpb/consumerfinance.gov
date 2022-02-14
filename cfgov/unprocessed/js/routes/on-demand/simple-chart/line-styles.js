import styles from './common-styles.js';
import trackChartEvent from './util.js';

const line = {
  ...styles,
  plotOptions: {
    ...styles.plotOptions,
    series: {
      events: {
        legendItemClick: function( evt ) {
          trackChartEvent(
            evt,
            'Legend Clicked',
            `${ evt.target.name }: ${ evt.target.visible ? 'hide' : 'show' }`
          );
        }
      },
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
