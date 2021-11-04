import styles from './common-styles.js';

const tilemap = {
  ...styles,
  accessibility: {},
  plotOptions: {
    tilemap: {
      tileShape: 'square',
      pointRange: 0.8,
      pointPadding: 3,
      states: {
        hover: {
          enabled: false
        }
      },
      dataLabels: {
        enabled: true,
        formatter: function() { return `<span style="font-weight:900">${ this.point.state }</span><br/><span style="font-weight:100">${ Math.round( this.point.value ) }</span>`; },
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
  tooltip: {
    style: {
      fontFamily: 'Avenir Next',
      fontSize: '16px'
    }
  },
  legend: {
    enabled: false
  },
  chart: {
    animation: false,
    maxWidth: 670,
    height: 450,
    marginLeft: -48,
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
            marginLeft: -19,
            spacingBottom: -240
          },

          plotOptions: {
            tilemap: {
              pointRange: 0
            }
          }
        }
      }
    ]
  }
};

export default tilemap;
