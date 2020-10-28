const styles = {
  chart: {
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      lineHeight: 1.5
    }
  },
  credits: false,
  colors: ['#20aa3f'],
  legend: {
    enabled: false
  },
  scrollbar: {
    enabled: false
  },
  plotOptions: {
    series: {
      lineWidth: 1.5,
      states: {
        hover: {
          enabled: false
        }
      }
    }
  },
  tooltip: {
    animation: false,
    shape: 'square',
    shared: true,
    split: false,
    padding: 10,
    useHTML: true,
    style: {
      pointerEvents: 'auto'
    }
  },
  xAxis: {
    type: 'datetime',
    crosshair: true,
    labels: {
      format: '{value:%Y}'
    },
    tickInterval: 365 * 24 * 3600 * 1000
  },
  yAxis: {
    title: {
      text: '',
      margin: 25
    }
  }
}

export default styles
