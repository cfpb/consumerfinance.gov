import styles from './common-styles.js';

const tilemap = {
  ...styles,
  accessibility: {},
  plotOptions: {
    tilemap: {
      tileShape: 'square',
      pointRange: 0.8,
      pointPadding: 3,
      dataLabels: {
        enabled: true,
        formatter: function() { return `${ this.point.state }<br/><span style="font-weight:100">${ Math.round( this.point.value ) }</span>`; },
        color: '#101820',
        style: {
          textOutline: false,
          fontSize: '12px'
        }
      },
      states: {
        hover: {
          color: 'rgba(100,210,100,.3)'
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
  tooltip: { formatter: function() { return `${ this.point.name }<br/>Index value: <b>${ Math.round( this.point.value * 10 ) / 10 }</b>`; } },
  legend: {
    enabled: false,
    title: 'Index value'
  },
  chart: {
    maxWidth: 670,
    height: 550,
    marginLeft: 0,
    marginRight: 0,
    marginTop: -1,
    spacingBottom: -290,
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
            animation: false,
            height: 450,
            spacingBottom: -240
          }
        }
      }
    ]
  }
};

export default tilemap;
