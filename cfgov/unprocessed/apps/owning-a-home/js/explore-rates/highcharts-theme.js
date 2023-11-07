const HIGHCHARTS_SETTINGS = {
  colors: ['#ADDC91'],
  style: {
    fontFamily: '"Avenir Next", Arial, sans-serif',
    fontSize: '13px',
  },
  chart: {
    backgroundColor: '#FFFFFF',
    marginRight: 25,
  },
  title: {
    text: '',
  },
  credits: {
    enabled: false,
  },
  yAxis: {
    labels: {
      formatter: function () {
        return this.value > 9 ? this.value + '+' : this.value;
      },
      style: {
        color: '#BABBBD',
      },
    },
    max: 10,
    min: 0,
    minorTickInterval: null,
    gridLineColor: '#E3E4E5',
    tickWidth: 0,
    title: {
      text: 'Number of lenders offering rate',
      style: {
        color: '#101820',
        fontSize: '16px',
        fontWeight: 'normal',
        fontFamily: '"Avenir Next", Arial, sans-serif',
      },
    },
    plotLines: [
      {
        color: '#919395',
        width: 1,
        value: 0,
        zIndex: 100,
      },
    ],
  },
  xAxis: {
    minorTickInterval: null,
    labels: {
      rotation: -90,
    },
    title: {
      style: {
        color: '#BABBBD',
        fontSize: '12px',
        fontWeight: 'normal',
        fontFamily: '"Avenir Next", Arial, sans-serif',
      },
    },
  },
  tooltip: {
    backgroundColor: 'transparent',
    borderColor: 'none',
    shadow: false,
  },
  plotOptions: {
    series: {
      groupPadding: 0.08,
    },
  },
  exporting: {
    enabled: false,
  },
};

/**
 * Apply theme settings to a Highcharts instance.
 * @param {object} highcharts - A Highcharts instance.
 */
function applyThemeTo(highcharts) {
  highcharts.theme = HIGHCHARTS_SETTINGS;

  // Apply the theme
  highcharts.setOptions(highcharts.theme);
}

export { applyThemeTo };
