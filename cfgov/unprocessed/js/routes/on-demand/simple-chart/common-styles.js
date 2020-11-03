const styles = {
  chart: {
    style: {
      fontFamily: '"Avenir Next", Arial, sans-serif',
      fontSize: '16px',
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
      lineWidth: 2,
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
    borderColor: '#b4b5b6',
    borderRadius: 3,
    padding: 10,
    shadow: { color: '#b4b5b6', opacity: 0.2 },
    shared: true,
    split: false,
    followPointer: true,
    style: {
      pointerEvents: 'auto',
      fontSize: '16px'
    },
    useHTML: true
  },
  yAxis: {
    title: {
      text: '',
      margin: 25
    },
    labels: {
      style: {
        fontSize: '16px'
      }
    }
  }
}

export default styles
