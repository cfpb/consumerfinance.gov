const styles = {
  chart: {
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: '16px',
      color: '#5a5d61',
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
      lineWidth: 3,
      states: {
        hover: {
          enabled: false
        }
      },
      color: '#20aa3f'
    }
  },
  tooltip: {
    animation: false,
    backgroundColor: '#f7f8f9',
    borderColor: '#919395',
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
    lineColor: '#d2d3d5'
  },
  yAxis: {
    title: {
      x: -16
    },
    lineColor: '#d2d3d5',
    labels: {
      style: {
        fontSize: '16px'
      }
    }
  }
}

export default styles
