'use strict';

var Highcharts = require( 'highcharts' );

Highcharts.theme = {
  colors: [ '#ADDC91' ],
  style: {
    fontFamily: '"Avenir Next", Arial, Helvetica, sans-serif',
    fontSize:   '13px'
  },
  chart: {
    backgroundColor: '#FFFFFF',
    marginRight:     25
  },
  yAxis: {
    labels: {
      style: {
        color: '#BABBBD'
      }
    },
    minorTickInterval: null,
    gridLineColor:     '#E3E4E5',
    tickWidth:         0,
    title: {
      style: {
        color:      '#101820',
        fontSize:   '16px',
        fontWeight: 'normal',
        fontFamily: '"Avenir Next", Arial, sans-serif'
      }
    },
    plotLines: [ {
      color:  '#919395',
      width:  1,
      value:  0,
      zIndex: 100
    } ]
  },
  xAxis: {
    labels: {
      enabled: false
    },
    minorTickInterval: null,
    tickWidth: 0,
    title: {
      style: {
        color:      '#BABBBD',
        fontSize:   '12px',
        fontWeight: 'normal',
        fontFamily: '"Avenir Next", Arial, sans-serif'
      }
    }
  },
  tooltip: {
    backgroundColor: 'transparent',
    borderColor:     'none',
    shadow:          false
  },
  plotOptions: {
    series: {
      groupPadding: 0.08
    }
  }
};

// Apply the theme
Highcharts.setOptions( Highcharts.theme );
