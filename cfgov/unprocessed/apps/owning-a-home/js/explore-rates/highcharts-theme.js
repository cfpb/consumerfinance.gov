const HIGHCHARTS_SETTINGS = {
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
  },
  exporting: {
    buttons: {
      contextButton: {
        symbol: 'download',
        text:   'Download'
      }
    }
  }
};

/**
 * Apply theme settings to a Highcharts instance.
 * @param {Object} highcharts - A Highcharts instance.
 */
function applyThemeTo( highcharts ) {
  highcharts.SVGRenderer.prototype.symbols.download =
    function download( x, y, w, h ) {
      return [
        // Arrow stem
        'M', x + w * 0.5, y,
        'L', x + w * 0.5, y + h * 0.7,
        // Arrow head
        'M', x + w * 0.3, y + h * 0.5,
        'L', x + w * 0.5, y + h * 0.7,
        'L', x + w * 0.7, y + h * 0.5,
        // Box
        'M', x, y + h * 0.9,
        'L', x, y + h,
        'L', x + w, y + h,
        'L', x + w, y + h * 0.9
      ];
    };

  highcharts.theme = HIGHCHARTS_SETTINGS;

  // Apply the theme
  highcharts.setOptions( highcharts.theme );
}

module.exports = { applyThemeTo: applyThemeTo };
