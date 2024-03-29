// Map of CFPB brand colors to their hex values that are used in this file.
const colorMap = {
  'var(--gray)': '#5a5d61',
  'var(--gray-20)': '#d2d3d5',
  'var(--gray-40)': '#b4b5b6',
  'var(--gray-60)': '#919395',
  'var(--green)': '#20aa3f',
  'var(--navy)': '#254b87',
  'var(--pacific-60)': '#7eb7e8',
  'var(--gold-80)': '#ffb858',
  'var(--purple-80)': '#c55998',
};

const styles = {
  accessibility: {},
  chart: {
    height: 500,
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: '16px',
      color: colorMap['var(--gray)'],
      lineHeight: 1.375,
    },
    events: {
      render: function () {
        const zoomText = this.container.querySelector(
          '.highcharts-range-selector-buttons > text',
        );
        if (zoomText && zoomText.textContent !== 'Select time range')
          zoomText.textContent = 'Select time range';
      },
    },
  },
  credits: false,
  colors: [
    colorMap['var(--green)'],
    colorMap['var(--navy)'],
    colorMap['var(--pacific-60)'],
    colorMap['var(--gold-80)'],
    colorMap['var(--purple-80)'],
  ],
  scrollbar: {
    enabled: false,
  },
  legend: {
    enabled: true,
    symbolWidth: 30,
    floating: true,
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'top',
    itemMarginBottom: 4,
    itemStyle: {
      color: colorMap['var(--gray)'],
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: 16,
    },
    itemHiddenStyle: {
      color: '#ccc !important',
    },
    itemHoverStyle: {
      color: '#000 !important',
    },
  },
  plotOptions: {
    series: {
      animation: {
        duration: 500,
      },
      states: {
        hover: {
          enabled: false,
        },
      },
    },
  },
  tooltip: {
    animation: false,
    borderColor: colorMap['var(--gray-60)'],
    distance: 15,
    padding: 15,
    shadow: { color: colorMap['var(--gray-40)'], opacity: 0.2 },
    shared: false,
    split: false,
    style: {
      pointerEvents: 'auto',
      fontSize: '16px',
    },
    useHTML: true,
  },
  xAxis: {
    lineColor: colorMap['var(--gray-20)'],
    minRange: 3 * 30 * 24 * 3600 * 1000,
    title: {
      margin: 10,
    },
  },
  yAxis: {
    title: {
      x: -16,
      y: 0,
      align: 'middle',
      reserveSpace: true,
      rotation: 270,
      textAlign: 'center',
      style: {
        color: colorMap['var(--gray)'],
      },
    },
    lineColor: colorMap['var(--gray-20)'],
    labels: {
      style: {
        color: colorMap['var(--gray)'],
        fontSize: '16px',
      },
      formatter: function () {
        /* If chart data is above 1 billion return "B" in y-axis.
         If chart data is above 1 million return "M" in y-axis.
         If chart data is above 1 thousand return "K" in y-axis */
        if (this.value >= 1000000000) {
          return this.value / 1000000000 + 'B';
        } else if (this.value >= 1000000) {
          return this.value / 1000000 + 'M';
        } else if (this.value >= 1000) {
          return this.value / 1000 + 'K';
        }
        return this.value;
      },
    },
  },
  responsive: {
    rules: [
      {
        condition: {
          maxWidth: 540,
        },
        chartOptions: {
          chart: {
            spacingLeft: 0,
            marginRight: 15,
          },
          legend: {
            align: 'left',
            margin: 0,
            padding: 0,
          },
          yAxis: {
            title: {
              x: 0,
              y: -25,
              align: 'high',
              reserveSpace: false,
              rotation: 0,
              textAlign: 'left',
            },
          },
        },
      },
    ],
  },
};

export default styles;
