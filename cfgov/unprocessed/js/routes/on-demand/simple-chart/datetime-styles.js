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
        const selects = document.querySelectorAll( '.o-simple-chart .select-wrapper select' );
        if ( !selects.length || !evt.userMin || evt.trigger !== 'rangeSelectorButton' ) return;
        const options = selects[0].querySelectorAll( 'option' );
        const min = Number( evt.userMin <= evt.dataMin ?
          evt.dataMin : evt.userMin );
        const max = Number( evt.userMax > evt.dataMax ?
          evt.dataMax : evt.userMax );

        let minOptionVal,
            minGap = Infinity,
            maxGap = Infinity,
            maxOptionVal;

        options.forEach( opt => {
          const nGap = Math.abs( Number( opt.value ) - min );
          const xGap = Math.abs( Number( opt.value ) - max );
          if ( nGap < minGap ) {
            minGap = nGap;
            minOptionVal = opt.value;
          }
          if ( xGap < maxGap ) {
            maxGap = xGap;
            maxOptionVal = opt.value;
          }
        } );

        selects[0].value = minOptionVal;
        selects[1].value = maxOptionVal;
      }
    }
  },

  rangeSelector: {
    inputEnabled: false,
    floating: true,
    dropdown: 'never',
    enabled: true,
    allButtonsEnabled: true,
    buttonPosition: {
      x: -60,
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
    height: 45,
    series: {
      data: []
    },
    xAxis: {
      tickInterval: msYear * 2,
      labels: {
        style: {
          color: '#4f5257'
        }
      }
    },
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
          chart: {
            marginTop: 150,
            spacingBottom: 60
          },
          xAxis: {
            labels: {
              step: 2
            }
          },
          rangeSelector: {
            verticalAlign: 'bottom',
            buttonSpacing: 30,
            buttonPosition: {
              align: 'center',
              x: -70,
              y: 95
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
