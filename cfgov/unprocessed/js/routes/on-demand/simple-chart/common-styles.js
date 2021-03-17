const styles = {
  accessibility: {},
  chart: {
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: '16px',
      color: '#5a5d61',
      lineHeight: 1.375
    }
  },
  credits: false,
  // CFPB Green, Navy, Pacific 60, Gold 80, Purple 80
  colors: [ '#20aa3f', '#254b87', '#7eb7e8', '#ffb858', '#c55998' ],
  scrollbar: {
    enabled: false
  },
  legend: { enabled: false },
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
            spacingLeft: 0
          },
          xAxis: {
            labels: {
              step: 2
            }
          },
          yAxis: {
            title: {
              x: 0,
              y: -28,
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
