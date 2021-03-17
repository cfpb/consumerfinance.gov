/* eslint complexity: ["error", 10] */
import styles from './line-styles.js';

const datetime = {
  ...styles,
  chart: {
    ...styles.chart,
    spacingTop: 0,
    spacingBottom: 0,
    marginTop: 70
  },
  xAxis: {
    ...styles.xAxis,
    type: 'datetime',
    minRange: 30 * 24 * 3600 * 1000,
    startOnTick: true,
    labels: {
      ...styles.xAxis.labels,
      format: 'Jan<br/>{value:%Y}'
    },
    tickInterval: 365 * 24 * 3600 * 1000,
    events: {
      afterSetExtremes: function( evt ) {
        const selects = document.querySelectorAll( '.o-simple-chart .select-wrapper select' );
        if ( !selects.length || !evt.userMin ) return;
        const min = Number( evt.userMin < evt.dataMin ?
          evt.dataMin : evt.userMin );
        const max = Number( evt.userMax > evt.dataMax ?
          evt.dataMax : evt.userMax );
        selects[0].value = Number( min );
        selects[1].value = Number( max );
      }
    }
  },
  legend: {
    enabled: false,
    symbolWidth: 45,
    floating: true,
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'top'
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
      type: 'year',
      count: 1,
      text: '1y',
      title: 'View 1 year'
    },
    {
      type: 'year',
      count: 3,
      text: '3y',
      title: 'View 3 year'
    },
    {
      type: 'year',
      count: 5,
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
            marginTop: 100
          },
          rangeSelector: {
            buttonPosition: {
              x: -24,
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
