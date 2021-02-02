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
  colors: [ '#20aa3f' ],
  legend: {
    enabled: false
  },
  scrollbar: {
    enabled: false
  },
  plotOptions: {
    series: {
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
    shared: true,
    split: false,
    style: {
      pointerEvents: 'auto',
      fontSize: '16px'
    },
    useHTML: true
  },
  xAxis: {
    lineColor: '#d2d3d5',
    xAxis: {
      title: {
        margin: 10
      }
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
            spacingTop: 40,
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
