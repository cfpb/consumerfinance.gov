/* eslint complexity: ["error", 10] */
import styles from './line-styles.js';
const msYear = 365 * 24 * 60 * 60 * 1000;

const datetime = {
  ...styles,
  chart: {
    ...styles.chart,
    spacingTop: 0,
    spacingBottom: 0,
    marginTop: 100
  },
  xAxis: {
    ...styles.xAxis,
    type: 'datetime',
    startOnTick: true,
    labels: {
      ...styles.xAxis.labels
    },
    events: {
      afterSetExtremes: function( evt ) {
        const dayOffset = evt.trigger === 'rangeSelectorButton' ?
          86400000 :
          0;
        const selects = document.querySelectorAll( '.o-simple-chart .select-wrapper select' );
        if ( !selects.length || !evt.userMin ) return;
        const min = Number( evt.userMin <= evt.dataMin ?
          evt.dataMin + dayOffset : evt.userMin );
        const max = Number( evt.userMax > evt.dataMax ?
          evt.dataMax : evt.userMax );

        selects[0].value = Number( min ) - dayOffset;
        selects[1].value = Number( max );
      }
    }
  },

  rangeSelector: {
    inputEnabled: false,
    floating: true,
    dropdown: 'never',
    enabled: true,
    buttonPosition: {
      x: -35,
      y: -70

    },
    buttonSpacing: 10,
    buttonTheme: {
      height: 30,
      width: 45,
      r: 5
    },
    buttons: [ {
      type: 'millisecond',
      count: msYear,
      text: '1y',
      title: 'View 1 year'
    },
    {
      type: 'millisecond',
      count: 3 * msYear,
      text: '3y',
      title: 'View 3 year'
    },
    {
      type: 'millisecond',
      count: ( 5 * msYear ) + 86400000,
      text: '5y',
      title: 'View 5 years'
    },
    {
      type: 'all',
      text: 'All',
      title: 'View all'
    } ]
  },
  navigator: {
    enabled: true,
    outlineColor: '#b4b5b6',
    height: 45,
    maskFill: 'black',
    series: { color: '#b4b5b6' },
    handles: {
      height: 20,
      width: 10
    }
  },
  responsive: {
    rules: [
      ...styles.responsive.rules,
      {
        condition: {
          maxWidth: 600
        },
        chartOptions: {
          xAxis: {
            labels: {
              step: 2
            }
          },
          rangeSelector: {
            buttonPosition: {
              x: -23,
              y: -85
            }
          },
          navigator: {
            enabled: false
          }
        }
      }
    ]
  }
};

export default datetime;
