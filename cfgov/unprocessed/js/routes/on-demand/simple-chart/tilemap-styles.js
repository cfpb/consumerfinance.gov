import styles from './common-styles.js';

const tilemap = {
  ...styles,
  accessibility: {},
  plotOptions: {
    tilemap: {
      tileShape: 'square',
      pointRange: 0.8,
      dataLabels: {
        enabled: true,
        format: '{point.state}',
        color: '#101820',
        style: {
          textOutline: false
        }
      }
    }
  },
  xAxis: {
    visible: false,
    tickAmount: 15,
    title: {}
  },
  yAxis: {
    visible: false,
    tickAmount: 15,
    title: {}
  },
  tooltip: { formatter: function() { return `${ this.point.name }<br/>Index value: <b>${ this.point.value }</b>`; } },
  legend: {
    ...styles.legend
  },
  chart: {
    maxWidth: 670,
    height: 550,
    spacingBottom: -325,
    type: 'tilemap'
  },
  responsive: {
    rules: [
      {
        condition: {
          maxWidth: 660
        },
        chartOptions: {
          chart: {
            height: 450,
            spacingBottom: -275
          }
        }
      }
    ]
  }
};

export default tilemap;
