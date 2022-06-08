const styles = {
  accessibility: {},
  chart: {
    height: 500,
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: '16px',
      color: '#5a5d61',
      lineHeight: 1.375
    },
    events: {
      render: function() {
        const zoomText = this.container.querySelector( '.highcharts-range-selector-buttons > text' );
        if ( zoomText && zoomText.textContent !== 'Select time range' ) zoomText.textContent = 'Select time range';
      }
    }
  },
  credits: false,
  // CFPB Green, Navy, Pacific 60, Gold 80, Purple 80
  colors: [ '#20aa3f', '#254b87', '#7eb7e8', '#ffb858', '#c55998' ],
  scrollbar: {
    enabled: false
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
      color: '#5a5d61',
      fontFamily: '"AvenirNextLTW01-Regular", Arial, sans-serif',
      fontSize: 16
    },
    itemHiddenStyle: {
      color: '#ccc !important'
    },
    itemHoverStyle: {
      color: '#000 !important'
    }
  },
  plotOptions: {
    series: {
      animation: {
        duration: 500
      },
      states: {
        hover: {
          enabled: false
        }
      }
    }
  },
  tooltip: {
    animation: false,
    borderColor: '#919395',
    distance: 15,
    padding: 15,
    shadow: { color: '#b4b5b6', opacity: 0.2 },
    shared: false,
    split: false,
    style: {
      pointerEvents: 'auto',
      fontSize: '16px'
    },
    useHTML: true
  },
  xAxis: {
    lineColor: '#d2d3d5',
    minRange: 3 * 30 * 24 * 3600 * 1000,
    title: {
      margin: 10
    }
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
        color: '#5a5d61'
      }
    },
    lineColor: '#d2d3d5',
    labels: {
      style: {
        color: '#5a5d61',
        fontSize: '16px'
      },
      formatter: function() {
        /* If chart data is above 1 billion return "B" in y-axis.
         If chart data is above 1 million return "M" in y-axis.
         If chart data is above 1 thousand return "K" in y-axis */
        if ( this.value >= 1000000000 ) {
          return this.value / 1000000000 + 'B';
        } else if ( this.value >= 1000000 ) {
          return this.value / 1000000 + 'M';
        } else if ( this.value >= 1000 ) {
          return this.value / 1000 + 'K';
        }
        return this.value;
      }
    }
  },
  responsive: {
    rules: [
      {
        condition: {
          maxWidth: 600
        },
        chartOptions: {
          chart: {
            spacingLeft: 0,
            marginRight: 15
          },
          legend: {
            align: 'left',
            margin: 0,
            padding: 0
          },
          yAxis: {
            title: {
              x: 0,
              y: -25,
              align: 'high',
              reserveSpace: false,
              rotation: 0,
              textAlign: 'left'
            }
          }
        }
      }
    ]
  }
};

export default styles;
